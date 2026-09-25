# this film is its own source code
D=r'''q="'"*3;S="# this film is its own source code\nD=r"+q+D+q+";exec(D)\n# pause here. copy me. run me. you will get this film again.\n"
import numpy as np,sys,io,base64,keyword as K,tokenize as T,subprocess as P;"--src"in sys.argv and sys.exit(print(S,end=""))
F=np.unpackbits(np.frombuffer(base64.b64decode("""AAAAAAAAAH0AAABwAHAAFH8UfxQSKn8qJGJkCBMjNklVIgUAAHAAAAAcIkEAAEEiHAAUCD4IFAgIPggIAAUGAAAICAgICAADAwAAAgQIE
CA+RUlRPhEhfwEBIUNFSTFCQVFpRgwUJH8EclFRUU4eKUlJBkBHSFBgNklJSTYwSUlKPAA2NgAAADU2AAAIFCJBABQUFBQUAEEiFAggQEVIMCZJT0E+P0hISD9/SUlJNj5BQUEif0FBIhx/SUlJQX9ISEhA
PkFJSS9/CAgIfwBBf0EAAgFBfkB/CBQiQX8BAQEBfyAYIH9/EAgEfz5BQUE+f0hISDA+QUVCPX9ITEoxMUlJSUZAQH9AQH4BAQF+fAIBAnx+AQ4BfmMUCBRjYBAPEGBDRUlRYQB/QUEAIBAIBAIAQUF/ABA
gQCAQAQEBAQEAQCAQAAIVFRUPfwkREQ4OERERAg4REQl/DhUVFQwIP0hAIAgVFRUefwgQEA8AEV8BAAIBEV4AfwQKEQAAQH4BAR8QDxAPHwgQEA8OERERDh8UFBQICBQUFB8fCBAQCAkVFRUSEH4RAQIeAQ
ECHxwCAQIcHgEGAR4RCgQKERgFBQUeERMVGREACDZBQQAAfwAAQUE2CAAIEAgECA=="""),np.uint8)).reshape(95,5,8)[...,1:].swapaxes(1,2);W,H,C0=960,540,480+270j
a=np.array([*S.encode()]);x=np.arange(len(a));n=a==10;e=np.r_[0,0,x[n]+1];r=np.cumsum(n)-n;c=x-e[r+1];k=0*x;U=np.uint64(x+1+len(a)*np.c_[:10])
for y,w,(i,j),(m,n),_ in T.generate_tokens(io.StringIO(S.replace(q,"'';")).readline):k[e[i]+j:e[m]+n]="ATUOP".find(T.tok_name[y][1])+5*K.iskeyword(w)
v=a>32;N=v.sum();I=np.arange(N);f=I/N;G=a[v]-32;cu=I[G==63][-1];hc=(W+1-6*c.max())//2+6*c+1j*((H-7-9*r.max())//2+9*r);h=hc[v]
Y=(np.array([*bytes.fromhex("E8E6F09BE38FFFC86B6B73857FD3FFFF7AB6")]).reshape(6,3)/255)[k[v]]**2.2;tk=np.interp(x,[0,35,len(a)],[.8,2,4.1]);tp=tk[v]
U=U*0x9E3779B97F4A7C15;U=(U^U>>30)*0xBF58476D1CE4E5B9;U=(U^U>>27)*0x94D049BB133111EB  # our tiny deterministic random generator: splitmix64
U=((U^U>>31)>>11)[:,v]/2**53;Q=U[7]**.5*np.exp(6.3j*U[8]);rk=lambda x:np.argsort(np.lexsort([x]));ei=lambda x:np.exp(1j*x)
gr=lambda w,*c:np.array([np.interp(w,np.linspace(0,1,len(c)),k)for k in zip(*c)]).T;dust=lambda t:12+930*U[3]+12j+510j*U[4]+6*ei(.3*t+7*U[5])
def home(t):  # the code: typed in out of the dust behind a blinking cursor; at rest in the finale
    e=np.clip((t-tp)/.15+1,0,1);e[cu]=1-.7*(t%.6>.35 and t<4.4);z=dust(t)*(1-e)+h*e;z[cu]=hc[np.searchsorted(tk[:-1],t)]if t<4.4 else h[cu]
    return z,Y*e[:,None]+np.outer(1-e,[.004,.005,.008])
def vortex(t):r=30+220*f**.6;return C0+r*ei(.9*(I%7)+.4*U[1]+(t-4)*90/(r+40)),None  # the code lifts off and swirls into a slow vortex
def sunrise(t):  # a sun rises from behind the sea, its rays turning slowly in a violet sky
    s=480+1j*(420-190*np.clip((t-8.2)/7,0,1)**.7);x=4+950*U[3];m=I%7;w=x+1j*(380+13*m+1.4*m*m+4*np.sin(.025*x+1.3*t+m)+2*np.sin(.07*x-.9*t))
    z=np.choose(p:=np.digitize(f,[.2,.38,.74]),[s+72*np.sqrt(f/.2)*ei(2.4*I),s+(84+(40+50*(I%2))*U[6])*ei(np.pi*(I%16)/8+.1*t),w,x+12j+350j*U[4]])
    z-=1j*np.maximum(z.imag-374,0)*(p<2);return z,gr(np.exp(-abs(z-s)/140),(.3,.12,.55),(1,.4,.15),(1,.8,.35))*np.array([1.2,.9,.7,.12])[p,None]
def bird(t):  # a gull beats its jointed wings along a loop, trailing a stream of fading characters
    p=(t-16)/10;B=lambda p:C0+230*np.sin(6.3*p)-1j*(20+80*np.cos(6.3*p));a=.3+.55*np.sin(7.5*t);b=a-.55-.5*np.sin(7.5*t-1.1);s=1-U[6]**.5;l=(f-.45)*.75
    w=8-4j+90*np.clip(s/.4,0,1)*ei(-a)+120*np.clip(s/.6-2/3,0,1)*ei(-b)+1j*U[7]*(40*(1-s)**.8+4);g=np.digitize(f,[.08,.45,.85])
    z=np.choose(g,[B(p)+10*Q.real+22j*Q.imag,B(p)+np.where(I%2,w,-w.conj()),B(p-l)+l*(150*Q+120j*l),dust(t)])+180*(Q+.5j)*np.clip(t-25.8,0,.5)**.5
    return z,np.array([(.3,.3,.32),(.25,.25,.28),(.3,.4,.6),(.04,.05,.08)])[g]*np.clip(1-2.8*l,.1,1)[:,None]
def rain(t):  # the bird bursts into a cloud; streaks of rain fall from it and pile up into a rolling sea
    n=N//192+1;c=I*67%192;k=I//192;g=c+192*(k//6);A=(k/n)**2;x=5*c;ys=532-5*k+A*(16*np.sin(.02*x-1.4*t)+6*np.sin(.05*x+.9*t))
    yc=15+U[7]*(50+25*np.sin(.013*x));y=np.minimum(np.maximum(yc,15+(160+200*U[2][g])*(t-26.8-28.8*(k//6)/n-.9*U[1][g])-9*(k%6)),ys);p=(y>yc)*1+(y>=ys)
    return x+4*A*np.cos(.02*x-1.4*t)+1j*y,np.where(p[:,None]>1,gr(k/n,(.04,.1,.36),(.16,.6,.64)),np.array([(.03,.04,.06),(.6,.85,1)])[p%2])
def face(t):  # a friendly face: it blinks twice, looks left, right, then at you
    y=408+144*(I%2)+16*np.interp(t,[38.8,39.2,39.9,40.4,41,41.4],[0,-1,-1,1,1,0])+208j+15*Q.real+24j*Q.imag*(1-.9*max(0,1-abs(t%.6-.3)*10)*(37.2<t<38.4))
    z=np.choose(p:=np.digitize(f,[.36,.5,.66]),[C0-8j+(205+7*U[1])*ei(17.5*f),y,C0-20j+(115+9*U[1])*ei(.6+1.9*U[2]),dust(t)])
    return z,np.array([(.9,.74,.56),(1.3,1.25,1.15),(1,.7,.5),(.004,.004,.003)])[p]
def galaxy(t):  # a two-armed spiral galaxy, brighter at the core; in the end it collapses
    s=1-.8*np.clip((t-48)/6,0,1)**2;r=np.where(c:=f<.2,45*U[1]**1.5,340*f-40);z=r*ei(np.where(c,6.3*U[2],np.pi*I+3.6*np.log(r/28))+.3*t+3*(1-s))
    return C0+s*(.85*z+.15*z.conj()+Q*(5+.25*r*U[3]))*ei(-.3),gr(r/300,(1,.9,.7),(.5,.6,1),(.8,.45,.9))*(.4+1.5*np.exp(-r/40))[:,None]
O=lambda z:np.lexsort((z.imag,rk(z.real)*40//N));SC=[];gp,mp=home,I  # O orders points in space: 40 vertical strips, top to bottom within each
for T0,w,d,g in(-1,0,1,home),(4.8,1.4,1.6,vortex),(7,1.5,2,sunrise),(16,1,2,bird),(26,.4,1.2,rain),(34,1.4,2,face),(42,1,2,galaxy),(48,5.4,1.1,home):
    q=g(T0+w/2+d/2)[0];m=I if g==home else O(q)[np.argsort(O(gp(T0)[0][mp]))];SC+=[(T0,w,d,g,m,rk(f if g==home else abs(q-C0))[m]/N)];gp,mp=g,m
def cl(z,t):return 25*sum(-1j*k*np.cos((z*k.conjugate()).real+w*t+p)for k,w,p in((.013+.006j,.9,0),(-.007+.011j,-.7,2),(.004-.016j,.5,4)))
def st(t,z=0,c=0):  # every particle's position (complex) and colour at time t: the scenes, blended in turn
    for T0,w,d,g,m,y in[s for s in SC if s[0]<t]:
        e=np.clip((t-T0-w*y)/d,0,1);Z,C=g(t);E=1+2.70158*(e-1)**3+1.70158*(e-1)**2 if g==home else np.where(e<.5,4*e**3,1-4*(1-e)**3)
        z=z*(1-E)+(Z[m]+(g!=home)*1.3*ei(2*t+6.3*U[0]))*E+300*e*(1-e)*cl(z,t);c=c*(1-e[:,None])+(Y if C is None else C[m])*e[:,None]
    return np.rint(955-abs(955-abs(z.real))+1j*(533-abs(533-abs(z.imag)))),c  # whole pixels; bounce off the edges, so every glyph stays on screen
pi,oy,ox=np.nonzero(F[G]);o=oy*W+ox;L=((1-np.exp(-1.8*(np.arange(4096)/512)**2))**(1/2.2)*255+.5).astype(np.uint8);BG=np.array([7,8,12],np.uint8)
def bl(a,w,n=6):s=(np.pad(a,[(3*w+3>>1,3*w-3>>1)]*2+[(0,0)])if n>5 else a).cumsum(0);a=(s[w:]-s[:-w]).swapaxes(0,1);return bl(a,w,n-1)if n>1 else a/w**6
def draw(z,c):  # glyphs onto the canvas, add two glows; at 2x each canvas pixel becomes 4 screen pixels (glow interpolated); tone map
    A=np.zeros((H,W,3),"f");np.add.at(A.reshape(-1,3),np.int_(z.imag*W+z.real)[pi]+o,c[pi]);g=bl(A,3);g=.5*g+.25*bl(g[::2,::2],7).repeat(2,0).repeat(2,1)
    p=np.pad(g,((1,1),(1,1),(0,0)),"edge");x=np.array([[A+(9*g+3*p[i:i+H,1:-1]+3*p[1:-1,j:j+W]+p[i:i+H,j:j+W])/16 for j in(0,2)]for i in(0,2)])
    return np.maximum(L.take(np.minimum(np.sqrt(x)*512,4095).astype(np.uint16)),BG).transpose(2,0,3,1,4).reshape(2*H,2*W,3)
with P.Popen("ffmpeg -y -f rawvideo -pix_fmt rgb24 -s hd1080 -r 30 -i - -c:v libx264 -preset slow -crf 16 -pix_fmt yuv420p self.mp4".split(),stdin=-1)as p:
    for n in range(1890):p.stdin.write(draw(*st(n/30)).tobytes())
''';exec(D)
# pause here. copy me. run me. you will get this film again.
