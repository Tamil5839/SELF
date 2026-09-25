# SELF

`self.py` is a one-minute film made of its own source code. It is a *quine*: a program that reproduces its own source text without reading it from disk (no `open`, no `__file__`, no `inspect`). Most of the file is a string `D` that the program both executes and uses to rebuild itself exactly, so `python self.py --src` prints `self.py` byte for byte. The film contains nothing but the characters of that source. Every character is on screen in every frame; nothing is created or destroyed, only moved and recoloured. The characters type themselves in out of a field of dust, lift off into a vortex, and become a sunrise, a bird, rain falling into a sea, a face and a galaxy. Finally they fly home, and the last eight seconds show the complete, readable source: copy it, run it, and you get the film again. Run `python self.py` to render `self.mp4` (1920×1080, 30 fps, H.264). It needs only Python 3.10+, NumPy and the `ffmpeg` command-line tool, and takes about 7 minutes (roughly 0.2 s per frame). The 5×7 font, the colours, the shapes and the random numbers (a small splitmix64 hash) all live inside the file, and there are no clocks or library RNGs. The rendered video frames are identical on any machine with the same NumPy version, though the bytes of the `.mp4` file may differ slightly between ffmpeg versions.

```
python self.py          # writes self.mp4
python self.py --src    # prints its own source
python test_self.py     # quine, no cheating, size, font, final frame, conservation, determinism
```
