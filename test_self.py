"""Tests for self.py, the film that is its own source code.

Run:  python test_self.py                    (all tests; the determinism test renders the whole film twice)
      SELF_QUICK=1 python test_self.py       (determinism on every 10th frame only)
      SELF_FRAME=last.ppm python test_self.py  (also save the final frame, for the manual readability check)

The film is rendered without ffmpeg: self.py is executed with a stand-in `subprocess` module whose
Popen swallows (or hashes) the raw RGB frames that would have been piped into ffmpeg.
"""
import base64
import hashlib
import os
import re
import subprocess
import sys
import textwrap
import types
import unittest

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "self.py")
with open(PATH, "rb") as fh:
    RAW = fh.read()
SRC = RAW.decode("ascii")
FPS, W, H = 30, 960, 540  # canvas in "font pixels"; the video is this upscaled 2x


def load_film():
    """Execute self.py in-process with rendering disabled; return its namespace."""
    class Stop(Exception):
        pass

    class Popen:  # replaces ffmpeg: refuses the first frame, which ends the render loop
        def __init__(self, cmd, stdin=None, **kw):
            self.cmd, self.stdin = cmd, self

        def write(self, data):
            raise Stop

        def __enter__(self):
            return self

        def __exit__(self, kind, value, tb):
            return kind is Stop

    fake = types.ModuleType("subprocess")
    fake.Popen, fake.PIPE = Popen, subprocess.PIPE
    real = sys.modules["subprocess"]
    sys.modules["subprocess"] = fake
    try:
        ns = {"__name__": "__film__"}
        exec(compile(SRC, PATH, "exec"), ns)
    finally:
        sys.modules["subprocess"] = real
    return ns


# A child process that runs self.py unmodified, except that frames go to sha256 instead of ffmpeg.
# It prints "frame size sha256" for every step-th frame, and "last frame size sha256" at the end.
HASHER = textwrap.dedent("""
    import hashlib, sys, types
    step = int(sys.argv[2])
    class Popen:
        def __init__(self, cmd, stdin=None, **kw):
            self.cmd, self.stdin, self.n, self.last = cmd, self, 0, None
        def write(self, data):
            self.last = "%d %d %s" % (self.n, len(data), hashlib.sha256(data).hexdigest())
            if self.n % step == 0:
                print(self.last, flush=True)
            self.n += 1
        def __enter__(self): return self
        def __exit__(self, *exc): print("last", self.last, flush=True)
    sys.modules["subprocess"] = types.SimpleNamespace(Popen=Popen, PIPE=-1)
    sys.argv = [sys.argv[1]]
    src = open(sys.argv[0]).read()
    exec(compile(src, sys.argv[0], "exec"), {"__name__": "__main__"})
""")


def render_hashes(step, seed):
    env = dict(os.environ, PYTHONHASHSEED=str(seed))
    return subprocess.Popen([sys.executable, "-c", HASHER, PATH, str(step)], stdout=subprocess.PIPE, env=env, text=True)


class TestSelf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ns = load_film()
        cls.lines = SRC.split("\n")[:-1]
        cls.visible = sum(not ch.isspace() for ch in SRC)

    # --- the quine -------------------------------------------------------------------------------
    def test_quine(self):
        out = subprocess.run([sys.executable, PATH, "--src"], capture_output=True, check=True).stdout
        self.assertEqual(out, RAW, "`python self.py --src` must print self.py byte for byte")

    def test_no_cheating(self):
        forbidden = [r"\bopen\(", r"__file__", r"\binspect\b", r"argv\[0\]", r"\burllib\b", r"\bsocket\b",
                     r"\brequests\b", r"\bimportlib\b", r"__import__", r"\blinecache\b", r"\bpathlib\b",
                     r"__loader__", r"__spec__", r"getsource", r"read_text", r"read_bytes", r"\bhttp"]
        for pattern in forbidden:
            self.assertIsNone(re.search(pattern, SRC), "self.py must not contain %r" % pattern)

    def test_size(self):
        self.assertTrue(SRC.endswith("\n"))
        self.assertLessEqual(len(self.lines), 60)
        self.assertLessEqual(max(map(len, self.lines)), 160)
        self.assertTrue(all(ch == "\n" or " " <= ch <= "~" for ch in SRC), "printable ASCII only")
        self.assertEqual(self.lines[0], "# this film is its own source code")
        self.assertIn("# pause here. copy me. run me. you will get this film again.", self.lines[-1])

    # --- the font --------------------------------------------------------------------------------
    def font(self):
        data = re.search(r'b64decode\("""(.*?)"""', SRC, re.S).group(1)
        cols = np.frombuffer(base64.b64decode(data), np.uint8).reshape(95, 5)  # one byte per column
        glyphs = (cols[:, None, :] >> (6 - np.arange(7))[None, :, None]) & 1  # bit 6-r = row r
        self.assertEqual(glyphs.shape, (95, 7, 5))
        return glyphs

    def test_font(self):
        g = self.font()
        np.testing.assert_array_equal(self.ns["F"], g)
        self.assertEqual(g[0].sum(), 0, "space is blank")
        shapes = {chr(32 + i): g[i].tobytes() for i in range(95)}
        self.assertEqual(len(set(shapes.values())), 95, "every glyph is distinct")
        for group in ("0Oo", "1lI|!", "5S", "2Z", "8B", ".,", ":;", "'`\"", "([{", "-_=", "gq9"):
            self.assertEqual(len({shapes[c] for c in group}), len(group), group)

    # --- the layout and the final frame ----------------------------------------------------------
    def layout(self):
        """Reference home layout: line i, column j -> cell (j, i), the text block centred on the canvas."""
        rows, cols = len(self.lines), max(map(len, self.lines))
        x0, y0 = (W - (6 * cols - 1)) // 2, (H - (9 * rows - 2)) // 2
        cells = [(x0 + 6 * j, y0 + 9 * i, ch) for i, line in enumerate(self.lines) for j, ch in enumerate(line) if ch != " "]
        return np.array([c[0] + 1j * c[1] for c in cells]), [c[2] for c in cells]

    def test_final_frame(self):
        ns = self.ns
        home, chars = self.layout()
        self.assertEqual(len(chars), self.visible)
        np.testing.assert_array_equal(ns["h"], home)  # the program's home cells are the reference layout
        n_frames = self.frame_count()
        z, c = ns["st"]((n_frames - 1) / FPS)
        # every particle is exactly at home, in its syntax colour
        np.testing.assert_array_equal(np.rint(z), home)
        np.testing.assert_array_equal(c, ns["Y"])
        # rasterise the final particles independently and read the text back, cell by cell
        g = self.font()
        canvas = np.zeros((H, W), int)
        for p, glyph in zip(np.rint(z), ns["G"]):
            x, y = int(p.real), int(p.imag)
            canvas[y:y + 7, x:x + 5] += g[glyph]
        for p, ch in zip(home, chars):
            x, y = int(p.real), int(p.imag)
            np.testing.assert_array_equal(canvas[y:y + 7, x:x + 5], g[ord(ch) - 32], "cell %r" % ch)
        self.assertEqual(canvas.sum(), sum(g[ord(ch) - 32].sum() for ch in chars), "nothing else is lit")
        # and the pixels of the last frame equal a static render of the source in its home layout
        last = ns["draw"](z, c)
        expected = ns["draw"](home, ns["Y"])
        self.assertEqual(last.shape, (2 * H, 2 * W, 3))
        self.assertEqual(last.dtype, np.uint8)
        np.testing.assert_array_equal(last, expected)
        if os.environ.get("SELF_FRAME"):
            with open(os.environ["SELF_FRAME"], "wb") as out:  # binary PPM: opens in most image viewers
                out.write(b"P6 1920 1080 255\n" + last.tobytes())
        # the hold is perfectly still: every frame of the last 8 seconds is the source at rest
        for frame in range(n_frames - 8 * FPS, n_frames):
            z2, c2 = ns["st"](frame / FPS)
            np.testing.assert_array_equal(np.rint(z2), home)
            np.testing.assert_array_equal(c2, ns["Y"])

    def frame_count(self):
        return int(re.search(r"for n in range\((\d+)\)", SRC).group(1))

    # --- conservation ----------------------------------------------------------------------------
    def test_conservation(self):
        ns = self.ns
        n_frames = self.frame_count()
        self.assertGreaterEqual(n_frames / FPS, 55 + 8)
        self.assertEqual(ns["N"], self.visible)
        self.assertEqual(sorted(chr(32 + int(g)) for g in ns["G"]), sorted(ch for ch in SRC if not ch.isspace()))
        for frame in list(range(0, n_frames, 11)) + [n_frames - 1]:
            z, c = ns["st"](frame / FPS)
            self.assertEqual(z.shape, (self.visible,), frame)
            self.assertEqual(c.shape, (self.visible, 3), frame)
            self.assertTrue(np.isfinite(z).all() and np.isfinite(c).all(), frame)
            x, y = np.rint(z.real), np.rint(z.imag)
            # the whole 5x7 glyph of every particle lies on the canvas...
            self.assertTrue(((x >= 0) & (x <= W - 5) & (y >= 0) & (y <= H - 7)).all(), frame)
            # ...and every particle is lit
            self.assertTrue((c.max(1) > 0).all() and (c >= 0).all(), frame)

    # --- determinism -----------------------------------------------------------------------------
    def test_determinism(self):
        step = 10 if os.environ.get("SELF_QUICK") else 1
        runs = [render_hashes(step, seed) for seed in (1, 2)]  # two processes, different hash seeds
        outs = [r.communicate()[0].split("\n") for r in runs]
        for r in runs:
            self.assertEqual(r.returncode, 0)
        a, b = ([line.split() for line in out if line] for out in outs)
        self.assertEqual(a, b, "the two renders differ")
        n_frames = self.frame_count()
        frames, last = a[:-1], a[-1]
        self.assertEqual([int(f[0]) for f in frames], list(range(0, n_frames, step)))
        self.assertTrue(all(int(size) == 1920 * 1080 * 3 for _, size, _ in frames), "1920x1080 RGB24 frames")
        # the last frame actually piped out of the film is the source, rendered at rest
        home, _ = self.layout()
        still = hashlib.sha256(self.ns["draw"](home, self.ns["Y"]).tobytes()).hexdigest()
        self.assertEqual(last, ["last", str(n_frames - 1), str(1920 * 1080 * 3), still])


if __name__ == "__main__":
    unittest.main(verbosity=2)
