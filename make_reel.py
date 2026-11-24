#!/usr/bin/env python3
"""make_reel.py spec.json [--stills]   ->  out/<slug>.mp4 + out/<slug>.caption.txt
Spec: {slug,bg,voice,scenes:[{type,lines:[..],...}],caption}
Needs: kokoro-onnx + models (kokoro-v1.0.onnx, voices-v1.0.bin in ./models), playwright+chrome, ffmpeg, numpy, soundfile."""
from icons import icon
import asyncio, json, os, re, subprocess, sys, shutil, math
import numpy as np, soundfile as sf
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import chars as C
import cine as CN
import promo as PR
spec=json.load(open(sys.argv[1])); STILLS="--stills" in sys.argv
OUT=os.path.join(HERE,"out"); TMP=os.path.join(HERE,"tmp_"+spec["slug"]); os.makedirs(OUT,exist_ok=True); os.makedirs(TMP,exist_ok=True)
BGS={"lavender":"#CDBBFF","sky":"#A9D8FF","peach":"#FFCBA6","lime":"#D6F25A","offwhite":"#F4F1EA","dark":"#141414"}
BG=BGS[spec.get("bg","peach")]; DARK=spec.get("bg")=="dark"
PADTOP=100
LIME="#D6F25A"; INK="#fff" if DARK else "#111"; RED="#E5322D"
PH=os.path.join(HERE,"photos")
def ph(n): return "file://"+os.path.join(PH,n)
def hl(s): return re.sub(r"\[\[(.+?)\]\]",lambda m:f"<span class=hl>{m.group(1)}</span>",s)
# ---------- voice
def tts():
    from kokoro_onnx import Kokoro
    k=Kokoro(os.path.join(HERE,"models","kokoro-v1.0.onnx"),os.path.join(HERE,"models","voices-v1.0.bin"))
    sr=24000; segs=[]; t=0.0; GAP=0.28; scenes=[]
    for sc in spec["scenes"]:
        st=t; tl=[]
        for ln in sc["lines"]:
            a,sr=k.create(ln,voice=spec.get("voice","af_heart"),speed=spec.get("speed",1.0),lang="en-us")
            a=np.asarray(a,dtype=np.float32); segs.append((t,a)); tl.append((t,len(a)/sr)); t+=len(a)/sr+GAP
        scenes.append({"start":st,"dur":t-st+0.15,"lines":tl}); 
    scenes[-1]["dur"]+=0.9
    total=scenes[-1]["start"]+scenes[-1]["dur"]
    v=np.zeros(int(total*sr)+sr,dtype=np.float32)
    for s,a in segs: i=int(s*sr); v[i:i+len(a)]+=a
    return v,sr,scenes,total
# ---------- scene html
CSS=f"""*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:720px;height:1280px;background:{BG};font-family:Inter,sans-serif;color:{INK};position:relative;overflow:hidden}}
.safe{{position:absolute;left:88px;top:167px;width:487px;height:833px;display:flex;flex-direction:column;padding-top:{PADTOP}px}}
h1{{font-weight:500;font-size:52px;line-height:1.12;letter-spacing:-1px}}
.hl{{background:{LIME};color:#111;padding:0 8px;border-radius:8px;box-decoration-break:clone;-webkit-box-decoration-break:clone}}
.card{{background:#fff;color:#111;border:2px solid #111;border-radius:22px}}
@keyframes fu{{from{{opacity:0;transform:translateY(34px)}}to{{opacity:1;transform:none}}}}
@keyframes pop{{0%{{opacity:0;transform:scale(.5)}}60%{{opacity:1;transform:scale(1.1)}}100%{{opacity:1;transform:scale(1)}}}}
@keyframes push{{from{{transform:scale(1.0)}}to{{transform:scale(1.09)}}}}
@keyframes sc{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:none}}}}
@keyframes inL{{from{{opacity:0;transform:translateX(-160px)}}to{{opacity:1;transform:none}}}}
@keyframes inR{{from{{opacity:0;transform:translateX(160px)}}to{{opacity:1;transform:none}}}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-4px)}}}}
@keyframes draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
@keyframes swingR{{0%,100%{{transform:rotate(-16deg)}}50%{{transform:rotate(16deg)}}}}
@keyframes swingL{{0%,100%{{transform:rotate(16deg)}}50%{{transform:rotate(-16deg)}}}}
@keyframes shake{{0%,100%{{transform:rotate(-7deg)}}50%{{transform:rotate(7deg)}}}}
@keyframes tap{{0%,100%{{transform:rotate(0deg)}}50%{{transform:rotate(-12deg)}}}}
@keyframes drip{{0%{{opacity:0;transform:translateY(0)}}25%{{opacity:1}}100%{{opacity:0;transform:translateY(24px)}}}}
@keyframes show{{to{{opacity:1}}}}
@keyframes hide{{to{{opacity:0}}}}
@keyframes pace{{from{{transform:translateX(-12px)}}to{{transform:translateX(12px)}}}}
@keyframes outR{{to{{opacity:0;transform:translateX(220px)}}}}
@keyframes outL{{to{{opacity:0;transform:translateX(-220px)}}}}
@keyframes floaty{{0%{{opacity:0;transform:translateY(0) scale(.6)}}30%{{opacity:1}}100%{{opacity:0;transform:translateY(-70px) scale(1.2)}}}}
@keyframes camera{{from{{transform:scale(1) translateY(0)}}to{{transform:scale(1.025) translateY(-6px)}}}}@keyframes grainmv{{0%{{transform:translate(0,0)}}25%{{transform:translate(-14px,9px)}}50%{{transform:translate(11px,-12px)}}75%{{transform:translate(-8px,-6px)}}100%{{transform:translate(6px,13px)}}}}@keyframes growY{{from{{transform:scaleY(0)}}to{{transform:scaleY(1)}}}}@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}@keyframes jolt{{0%{{transform:translate(0,0)}}15%{{transform:translate(-10px,6px)}}30%{{transform:translate(9px,-7px)}}45%{{transform:translate(-7px,5px)}}60%{{transform:translate(6px,-4px)}}80%{{transform:translate(-3px,2px)}}100%{{transform:none}}}}
@keyframes flash{{0%{{opacity:0}}12%{{opacity:.38}}100%{{opacity:0}}}}
@keyframes fall{{0%{{opacity:0;transform:translateY(-40px) rotate(0)}}15%{{opacity:1}}100%{{opacity:1;transform:translateY(420px) rotate(540deg)}}}}
@keyframes wob{{0%,100%{{transform:rotate(-5deg)}}50%{{transform:rotate(5deg)}}}}
@keyframes pulse2{{0%,100%{{opacity:1}}50%{{opacity:.45}}}}
@keyframes planeX{{from{{transform:translateX(-30px)}}to{{transform:translateX(90px)}}}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
@keyframes grey{{to{{filter:grayscale(1);opacity:.45}}}}
@keyframes pulse{{0%,100%{{box-shadow:0 0 0 0 rgba(31,168,85,.6)}}50%{{box-shadow:0 0 0 14px rgba(31,168,85,0)}}}}
"""
def A(name,dur,delay,ease="cubic-bezier(.2,.8,.2,1)"): return f"animation:{name} {dur}s {ease} {delay}s both"
def head(text,d=0.05):
    lines=text.split("|"); return "".join(f"<h1 style='margin-top:{0 if i==0 else 6}px;{A('fu',.45,d+i*.12)}'>{hl(l)}</h1>" for i,l in enumerate(lines))
CINE="""<div style='position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,.38) 100%)'></div><div style='position:absolute;inset:-20px;pointer-events:none;opacity:.16;mix-blend-mode:multiply;background-image:url(\"data:image/svg+xml;utf8,<svg xmlns=%27http://www.w3.org/2000/svg%27 width=%27160%27 height=%27160%27><filter id=%27n%27><feTurbulence type=%27fractalNoise%27 baseFrequency=%270.9%27 numOctaves=%272%27/></filter><rect width=%27160%27 height=%27160%27 filter=%27url(%23n)%27/></svg>\");animation:grainmv .5s steps(4) infinite'></div>"""
DNPTS='10,20 90,40 160,34 230,80 300,70 370,120 440,112 510,170 570,186'
UPPTS='10,186 90,170 160,176 230,130 300,140 370,90 440,98 510,40 570,20'
def scene_html(sc,dur):
    t=sc["type"]; body=""; BAD=sc.get("tone")=="bad"; TONE="#FF9B93" if BAD else LIME
    if t=="photo":
        chip=f"<div style='position:absolute;left:22px;bottom:22px;background:{TONE};color:#111;border:2px solid #111;border-radius:14px;padding:10px 20px;font-weight:700;font-size:30px;{A('pop',.5,.9)}'>{sc['chip']}</div>" if sc.get("chip") else ""
        bub=f"<div class=card style='position:absolute;right:22px;top:22px;padding:14px 20px;font-size:26px;font-weight:600;{A('pop',.5,1.4)}'>{sc['bubble']}<div style='font-size:18px;color:#c0392b;margin-top:4px'>⏱ Not delivered</div></div>" if sc.get("bubble") else ""
        body=head(sc["headline"])+f"<div style='position:relative;margin-top:28px;flex:1;max-height:600px;border-radius:26px;overflow:hidden;border:2px solid #111;{A('fu',.6,.25)}'><img src='{ph(sc['photo'])}' style='width:100%;height:100%;object-fit:cover;object-position:{sc.get('pos','50% 30%')};{A('push',dur,0,'linear')}'>{chip}{bub}</div>"
    elif t=="pills":
        rows="".join(f"<div class=card style='display:flex;align-items:center;justify-content:space-between;padding:26px 28px;margin-bottom:18px;{A('fu',.5,.4+i*.35)}'><div style='display:flex;align-items:center;gap:16px;font-size:38px;font-weight:600;{A('grey',.5,sc.get('dim',2.2)+i*.15)}'><span style='width:18px;height:18px;border-radius:50%;background:{RED}'></span>{x}</div><div style='font-size:26px;font-weight:700;background:{RED};color:#fff;border-radius:12px;padding:6px 16px;{A('pop',.4,sc.get('dim',2.2)+i*.15)}'>Down</div></div>" for i,x in enumerate(sc["items"]))
        body=head(sc["headline"])+f"<div style='margin-top:44px'>{rows}</div>"
    elif t=="stat" and sc.get("style") in ("receipt","bars","big"):
        stl=sc["style"]; col=RED if BAD else '#111'
        cnt=f"<span id=cnt data-to='{sc['to']}' data-pre='{sc.get('pre','')}' data-suf='{sc.get('suf','')}' data-dec='{sc.get('dec',0)}'>0</span>"
        if stl=="receipt":
            rws="".join(f"<div style='display:flex;justify-content:space-between;font-size:30px;padding:8px 0;border-bottom:2px dashed #bbb;{A('fu',.45,.5+i*.35)}'><span>{a}</span><b>{b}</b></div>" for i,(a,b) in enumerate(sc["rows"]))
            zig="<svg width='100%' height='22' viewBox='0 0 520 22' preserveAspectRatio='none' style='display:block;margin-top:-1px'><polygon points='"+" ".join(f"{i*20},0 {i*20+10},20 {i*20+20},0" for i in range(26))+"' fill='#fff' stroke='#111' stroke-width='2'/></svg>"
            body=head(sc["headline"])+f"<div style='margin-top:40px;width:487px;{A('fu',.6,.3)};transform-origin:top'><div style='background:#fff;border:2px solid #111;border-bottom:0;padding:26px 28px 14px;position:relative;font-family:ui-monospace,Menlo,monospace'><div style='display:flex;align-items:center;gap:10px;font-size:26px;font-weight:700;letter-spacing:2px;margin-bottom:12px'>{icon('receipt',30,'#111',2.2)}COST REPORT</div>{rws}<div style='display:flex;justify-content:space-between;align-items:baseline;margin-top:18px;{A('fu',.5,.5+len(sc['rows'])*.35)}'><span style='font-size:28px;font-weight:700'>{sc['sub']}</span></div><div style='font-size:112px;font-weight:700;letter-spacing:-4px;line-height:1.05;color:{col};{A('pop',.5,.5+len(sc['rows'])*.35)}'>{cnt}</div><div style='position:absolute;right:14px;bottom:34px;border:5px solid {RED};color:{RED};border-radius:10px;padding:2px 14px;font-size:44px;font-weight:700;transform:rotate(-12deg);{A('pop',.3,1.5)}'>{sc.get('stamp','LOSS')}</div></div>{zig}</div>"
        elif stl=="bars":
            br="".join(f"<div style='margin-top:26px;{A('fu',.45,.5+i*.4)}'><div style='font-size:30px;font-weight:600;margin-bottom:8px'>{a}</div><div style='height:46px;width:{w}%;background:{c};border:2px solid #111;border-radius:12px;transform-origin:left;animation:grow .9s ease-out {.8+i*.4}s both'></div></div>" for i,(a,w,c) in enumerate(sc["bars"]))
            body=head(sc["headline"])+f"<div style='margin-top:34px;font-size:130px;font-weight:700;letter-spacing:-5px;line-height:1;color:{col};{A('pop',.5,.4)}'>{cnt}</div><div style='font-size:30px;font-weight:600;margin-top:6px'>{sc['sub']}</div>{br}"
        else:
            body=head(sc["headline"])+f"<div style='margin-top:70px;font-size:165px;font-weight:700;letter-spacing:-7px;line-height:1;color:{col};{A('pop',.5,.4)}'>{cnt}</div><div style='height:12px;width:420px;background:{col};border-radius:6px;transform-origin:left;animation:grow .8s ease-out 1.2s both;margin-top:6px'></div><div style='font-size:36px;font-weight:600;margin-top:24px;{A('fu',.5,1.5)}'>{sc['sub']}</div>"
    elif t=="stat":
        body=head(sc["headline"])+f"<div class=card style='margin-top:36px;background:{'#fff' if BAD else LIME};padding:40px 30px;text-align:center;{A('pop',.6,.5)}{';animation:pop .6s cubic-bezier(.2,.8,.2,1) .5s both, jolt .5s linear 1.5s both' if BAD else ''}'><div id=cnt data-to='{sc['to']}' data-pre='{sc.get('pre','')}' data-suf='{sc.get('suf','')}' data-dec='{sc.get('dec',0)}' style='font-size:150px;font-weight:700;letter-spacing:-6px;line-height:1;color:{RED if BAD else '#111'}'>0</div><div style='font-size:30px;font-weight:600;margin-top:16px'>{sc['sub']}</div></div><svg viewBox='0 0 584 200' width='487' height='167' preserveAspectRatio='none' style='margin-top:6px;margin-bottom:-80px;overflow:visible;transform:scaleY(.5);transform-origin:top' class='stage'><g class='chk'><polyline points='{UPPTS if sc.get("up") else DNPTS}' fill='none' stroke='#d3382c' stroke-width='9' stroke-linecap='round' stroke-linejoin='round' pathLength='1' stroke-dasharray='1' style='animation:draw 1.6s ease-out .9s both'/><circle cx='570' cy='{20 if sc.get("up") else 186}' r='13' fill='#d3382c' style='animation:pop .4s ease 2.4s both;transform-box:fill-box;transform-origin:center'/></g></svg>"
    elif t=="chats":
        rows="".join(f"<div style='display:flex;align-items:center;gap:10px;padding:10px 12px;border-bottom:1px solid #eee;{A('fu',.45,.5+i*.3)}'><div style='width:44px;height:44px;border-radius:50%;overflow:hidden;flex:none'><img src='{ph(r['photo'])}' style='width:100%;height:100%;object-fit:cover;object-position:{r.get('pos','50% 25%')}'></div><div style='flex:1;min-width:0'><div style='font-size:16px;font-weight:700'>{r['name']}</div><div style='font-size:14px;color:#555;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>{r['msg']}</div></div><div style='min-width:24px;height:24px;border-radius:12px;background:#1FA855;color:#fff;font-weight:700;font-size:14px;display:flex;align-items:center;justify-content:center;{A('pop',.4,.9+i*.3)}'>{r['n']}</div></div>" for i,r in enumerate(sc["rows"]))
        body=head(sc["headline"])+f"<div style='margin:22px auto 0;width:272px;background:#0b0b0c;border-radius:42px;padding:9px;box-shadow:0 24px 50px rgba(0,0,0,.25);position:relative;{A('fu',.6,.2)}'><div style='position:absolute;left:50%;top:15px;width:70px;height:20px;margin-left:-35px;background:#0b0b0c;border-radius:12px;z-index:2'></div><div style='background:#fff;color:#111;border-radius:34px;overflow:hidden;height:520px;display:flex;flex-direction:column'><div style='height:40px;display:flex;justify-content:space-between;align-items:flex-end;padding:0 22px 4px;font-size:13px;font-weight:700'><span>9:41</span><span style='display:flex;gap:5px;align-items:center'>{icon('signal',14,'#111',2.4)}{icon('wifi-off',14,'#111',2.4)}{icon('battery-full',18,'#111',2.2)}</span></div><div style='display:flex;align-items:center;gap:8px;background:#fff3cd;padding:9px 12px;font-size:14px;font-weight:600'><span style='display:inline-flex;{A('spin',1,0,'linear')};animation-iteration-count:infinite'>{icon('loader-circle',16,'#111',2.6)}</span>Connecting…</div>{rows}<div style='margin-top:auto;padding:10px 12px;border-top:1px solid #eee;font-size:13px;color:#888;display:flex;align-items:center;gap:8px'>{icon('search',14,'#888',2.2)}Search</div></div></div>"
    elif t=="browser":
        body=head(sc["headline"])+f"<div style='margin-top:30px;border:2px solid #111;border-radius:22px;overflow:hidden;background:#fff;color:#111;{A('fu',.6,.25)}'><div style='background:#eee;padding:14px 18px;display:flex;align-items:center;gap:12px'><span style='display:flex;gap:7px'><i style='width:13px;height:13px;border-radius:50%;background:#ff5f57'></i><i style='width:13px;height:13px;border-radius:50%;background:#febc2e'></i><i style='width:13px;height:13px;border-radius:50%;background:#28c840'></i></span><div style='flex:1;background:#fff;border-radius:12px;padding:8px 16px;font-size:22px;display:flex;align-items:center;gap:8px'>{icon('lock',18,'#555',2.2)}<span>{sc['url']}</span></div></div><div style='position:relative;height:430px;overflow:hidden'><img src='{ph(sc['photo'])}' style='width:100%;height:100%;object-fit:cover;object-position:{sc.get('pos','50% 30%')};{A('push',dur,0,'linear')}'><div style='position:absolute;left:0;right:0;bottom:0;padding:26px;background:linear-gradient(transparent,rgba(0,0,0,.75));color:#fff'><div style='font-size:40px;font-weight:700;line-height:1.1'>{sc['site_title']}</div><div style='display:inline-block;margin-top:16px;background:#1FA855;border-radius:14px;padding:14px 30px;font-size:28px;font-weight:700;{A('pulse',1.2,1.2,'ease')};animation-iteration-count:infinite'>{sc['cta']}</div></div></div><div style='display:flex;gap:12px;padding:16px 18px'><span style='background:{LIME};border-radius:10px;padding:6px 14px;font-size:22px;font-weight:700;{A('pop',.4,2.0)}'>Open 24/7</span><span style='background:#eee;border-radius:10px;padding:6px 14px;font-size:22px;font-weight:700;{A('pop',.4,2.3)}'>You own it</span></div></div>"
    elif t=="stage":
        acts=""
        for ob in sc["objects"]:
            k=ob["k"]; d=ob.get("d",0.3); 
            if k=="person":
                ent={"L":f"animation:inL .6s cubic-bezier(.2,.8,.2,1) {d}s both","R":f"animation:inR .6s cubic-bezier(.2,.8,.2,1) {d}s both","pop":f"animation:pop .5s ease {d}s both"}[ob.get("enter","pop")]
                inner=C.person(ob.get("skin","a"),ob.get("shirt","lav"),ob.get("pose","stand"),ob.get("expr","smile"),ob.get("apron"),ob.get("hat",False),ob.get("hair","short"),False,ob.get("dress"),ob.get("anim"),ob.get("expr2"),ob.get("expr2_at",0),ob.get("sweat",False),ob.get("hairc"))
                if ob.get("exit"): ent+=f", {'outR' if ob.get('exit_dir','R')=='R' else 'outL'} .8s ease-in {ob['exit']}s forwards"
                body_in=f"<g style='animation:bob 1.6s ease-in-out {d+.6}s infinite'>{inner}</g>"
                if ob.get("pace"): body_in=f"<g style='animation:pace 1.8s ease-in-out infinite alternate'>{body_in}</g>"
                acts+=C.actor(ob["x"],ob["y"],ob.get("s",1),ent+";transform-box:fill-box",body_in,ob.get("flip",False))
            elif k=="float": acts+=f"<g class='chk'><text x='{ob['x']}' y='{ob['y']}' font-size='{ob.get('size',44)}' fill='{ob.get('color','#e5322d')}' style='animation:floaty 1.8s ease-out {ob.get('d',0)}s infinite;transform-box:fill-box;transform-origin:center'>{ob['text']}</text></g>"
            elif k=="prop": acts+=C.prop(ob)
            elif k=="counter": acts+=C.counter(ob["x"],ob["y"],ob["w"],ob.get("h",100))
            elif k=="awning": acts+=C.awning(ob["x"],ob["y"],ob["w"])
            elif k=="sign": acts+=C.sign(ob["x"],ob["y"],ob["text"],ob.get("color","#1FA855"),f"animation:pop .5s ease {d}s both;transform-box:fill-box;transform-origin:center top")
            elif k=="bubble": acts+=C.bubble(ob["x"],ob["y"],ob["text"],ob.get("w",84),ob.get("h",56),f"animation:pop .45s ease {d}s both;transform-box:fill-box;transform-origin:center bottom",ob.get("tail","left"))
            elif k=="phone": acts+=C.phone_prop(ob["x"],ob["y"],ob["w"],ob["h"],ob.get("lines",[]),ob.get("spinner",False),f"animation:pop .5s ease {d}s both;transform-box:fill-box;transform-origin:center")
        chip=f"<div style='position:absolute;left:0;top:410px;background:{TONE};color:#111;border:2px solid #111;border-radius:14px;padding:8px 18px;font-weight:700;font-size:28px;{A('pop',.5,.8)}'>{sc['chip']}</div>" if sc.get("chip") else ""
        body=head(sc["headline"])+f"<div style='position:relative;margin-top:34px;width:487px;height:434px'>{chip}<svg viewBox='0 0 584 520' width='487' height='434' style='position:absolute;left:0;top:0;overflow:visible' class='stage'>{acts}</svg></div>"
    elif t=="kinetic":
        ls="".join(f"<div style='font-size:{sc.get('size',96)}px;font-weight:700;letter-spacing:-3px;line-height:1.0;margin-top:10px;{A('pop',.45,.2+i*sc.get('gap',.5))}'>{hl(l)}</div>" for i,l in enumerate(sc["big"]))
        sub=f"<div style='font-size:32px;font-weight:600;margin-top:30px;{A('fu',.5,.4+len(sc['big'])*sc.get('gap',.5))}'>{sc['sub']}</div>" if sc.get("sub") else ""
        body=f"<div style='margin-top:{sc.get('top',120)}px'>{ls}{sub}</div>"
    elif t=="timeline":
        n=len(sc["events"]); H=n*104
        rows="".join(f"<div style='position:relative;padding-left:46px;height:104px;{A('fu',.45,.5+i*.55)}'><div style='position:absolute;left:0;top:6px;width:24px;height:24px;border-radius:50%;background:{TONE if i==n-1 else '#fff'};border:3px solid #111'></div><div style='font-size:22px;font-weight:700;opacity:.65;letter-spacing:.5px'>{a}</div><div style='font-size:34px;font-weight:600;line-height:1.1;margin-top:4px'>{b}</div></div>" for i,(a,b) in enumerate(sc["events"]))
        body=head(sc["headline"])+f"<div style='position:relative;margin-top:40px'><div style='position:absolute;left:10px;top:12px;width:4px;height:{H-30}px;background:#111;border-radius:2px;transform-origin:top;animation:growY {n*.55+.4}s linear .4s both'></div>{rows}</div>"
    elif t=="versus":
        def col(c,bad,delay):
            its="".join(f"<div style='display:flex;gap:8px;align-items:flex-start;font-size:25px;font-weight:600;line-height:1.15;margin-top:12px'>{icon('x' if bad else 'check',20,'#d3382c' if bad else '#1c8a4c',3)}<span>{x}</span></div>" for x in c["items"])
            return f"<div class=card style='flex:1;padding:20px 16px;background:{'#fff0ee' if bad else '#fff'};{A('pop',.5,delay)}{';animation:pop .5s ease '+str(delay)+'s both, jolt .5s linear '+str(delay+.9)+'s both' if bad else ''}'><div style='display:flex;align-items:center;gap:8px;font-size:22px;font-weight:700;letter-spacing:1px;text-transform:uppercase'>{icon(c['icon'],26,'#111',2.4)}{c['title']}</div>{its}</div>"
        body=head(sc["headline"])+f"<div style='display:flex;gap:12px;margin-top:44px'>{col(sc['left'],False,.5)}{col(sc['right'],True,1.4)}</div>"
    elif t=="thread":
        ms="".join(f"<div style='display:flex;justify-content:{'flex-end' if m['from']=='me' else 'flex-start'};margin-top:10px;{A('fu',.35,.7+i*.7)}'><div style='max-width:78%;padding:9px 13px;border-radius:18px;font-size:17px;font-weight:500;line-height:1.2;background:{'#1FA855' if m['from']=='me' else '#e9e9eb'};color:{'#fff' if m['from']=='me' else '#111'}'>{m['text']}</div></div>" for i,m in enumerate(sc["msgs"]))
        body=head(sc["headline"])+f"<div style='margin:26px auto 0;width:272px;background:#0b0b0c;border-radius:42px;padding:9px;box-shadow:0 24px 50px rgba(0,0,0,.25);position:relative;{A('fu',.6,.2)}'><div style='position:absolute;left:50%;top:15px;width:70px;height:20px;margin-left:-35px;background:#0b0b0c;border-radius:12px;z-index:2'></div><div style='background:#fff;color:#111;border-radius:34px;overflow:hidden;height:{sc.get('h',500)}px;display:flex;flex-direction:column'><div style='height:40px;display:flex;justify-content:space-between;align-items:flex-end;padding:0 22px 4px;font-size:13px;font-weight:700'><span>{sc.get('time','9:41')}</span><span style='display:flex;gap:5px'>{icon('signal',14,'#111',2.4)}{icon('battery-full',18,'#111',2.2)}</span></div><div style='display:flex;align-items:center;gap:8px;padding:8px 12px;border-bottom:1px solid #eee;font-size:16px;font-weight:700'>{icon('chevron-left',18,'#111',2.4)}<div style='width:28px;height:28px;border-radius:50%;background:{TONE};display:flex;align-items:center;justify-content:center;font-size:14px'>{sc['contact'][0]}</div>{sc['contact']}</div><div style='padding:6px 12px'>{ms}</div></div></div>"
    elif t=="news":
        p=sc["paper"]
        cols="".join(f"<div style='height:9px;border-radius:4px;background:#cfc9bd;margin-top:9px;width:{w}%'></div>" for w in (100,92,100,84,96,70))
        body=f"<div style='margin-top:{sc.get('top',60)}px;transform:rotate(-2.5deg);{A('pop',.6,.2)}'><div style='background:#f6f1e4;color:#111;border:2px solid #111;padding:22px 22px 26px;box-shadow:0 18px 40px rgba(0,0,0,.2)'><div style='font-family:Georgia,serif;font-size:34px;font-weight:700;text-align:center;border-bottom:3px double #111;padding-bottom:8px'>{p['name']}</div><div style='display:flex;justify-content:space-between;font-size:15px;font-weight:600;margin:8px 0 14px'><span>{p['date']}</span><span>{p.get('edition','LATE EDITION')}</span></div><div style='font-family:Georgia,serif;font-size:{p.get('size',46)}px;font-weight:700;line-height:1.05;{A('fu',.5,.9)}'>{p['head']}</div><div style='display:flex;gap:14px;margin-top:16px'><div style='width:150px;height:120px;border:2px solid #111;background:{TONE};display:flex;align-items:center;justify-content:center;flex:none;{A('pop',.5,1.4)}'>{icon(p.get('icon','triangle-alert'),64,'#111',2)}</div><div style='flex:1'>{cols}</div></div></div></div>"+(f"<div style='font-size:32px;font-weight:600;margin-top:34px;{A('fu',.5,1.8)}'>{sc['sub']}</div>" if sc.get('sub') else "")
    elif t=="list":
        its="".join(f"<div class=card style='display:flex;align-items:center;gap:16px;padding:20px 20px;margin-top:16px;{A('fu',.5,.4+i*.55)}'><div style='width:46px;height:46px;border-radius:50%;background:{TONE};border:2px solid #111;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:24px;flex:none'>{i+1}</div><div style='font-size:30px;font-weight:600;line-height:1.1'>{x}</div></div>" for i,x in enumerate(sc["items"]))
        body=head(sc["headline"])+f"<div style='margin-top:20px'>{its}</div>"
    elif t=="object":
        body=head(sc["headline"])+f"<div style='margin:56px auto 0;width:300px;height:300px;border-radius:50%;background:#fff;border:3px solid #111;display:flex;align-items:center;justify-content:center;{A('pop',.6,.4)};{('animation:pop .6s ease .4s both, jolt .5s linear 1.4s both') if BAD else ''}'>{icon(sc['icon'],150,'#d3382c' if BAD else '#111',1.8)}</div><div style='text-align:center;font-size:36px;font-weight:700;margin-top:30px;{A('fu',.5,1.1)}'>{sc['label']}</div>"
    elif t=="comic":
        P=sc["panels"]; n=len(P); ph=int(sc.get("ph",(700-(n-1)*12)//n))
        def panel(i,p):
            bg=p.get("bg",TONE); d=.35+i*.7
            dots=f"background-image:radial-gradient(rgba(0,0,0,.16) 2.2px,transparent 2.6px);background-size:12px 12px;"
            rays=f"<div style='position:absolute;inset:-40%;background:repeating-conic-gradient(rgba(255,255,255,.55) 0 4deg,transparent 4deg 12deg);animation:spin 14s linear infinite;opacity:.9'></div>" if p.get("rays",True) else ""
            sfx=f"<div style='position:absolute;right:10px;bottom:6px;font-family:Impact,Anton,sans-serif;font-size:{p.get('sfxsize',54)}px;letter-spacing:1px;color:#fff;-webkit-text-stroke:3px #111;text-shadow:4px 4px 0 #111;transform:rotate(-8deg);{A('pop',.35,d+.5)}'>{p['sfx']}</div>" if p.get("sfx") else ""
            cap=f"<div style='position:absolute;left:0;top:0;background:#ffe27a;border:2px solid #111;border-width:0 2px 2px 0;padding:6px 12px;font-size:17px;font-weight:800;letter-spacing:.6px;text-transform:uppercase;max-width:78%'>{p['cap']}</div>" if p.get("cap") else ""
            spd=f"<div style='position:absolute;inset:0;{dots}'></div>"
            return f"<div style='position:relative;height:{ph}px;border:4px solid #111;background:{bg};overflow:hidden;{'transform:rotate('+str(p.get('rot',0))+'deg);'}{A('pop',.45,d)}'>{rays}{spd}<div style='position:absolute;inset:0;display:flex;align-items:center;justify-content:center;{A('pop',.5,d+.15)};{'animation:pop .5s ease '+str(d+.15)+'s both, jolt .5s linear '+str(d+.7)+'s both' if p.get('shake') else ''}'>{icon(p['icon'],p.get('isize',130),'#111',2.2)}</div>{cap}{sfx}</div>"
        body=f"<div style='display:flex;flex-direction:column;gap:12px;margin-top:{sc.get('top',10)}px'>{''.join(panel(i,p) for i,p in enumerate(P))}</div>"
    elif t=="promo":
        pre,body=PR.render(sc,dur,sc.get("_tl",[(0,dur)]*len(sc["lines"])))
    elif t=="cinema":
        pre=CN.render(sc,dur)+"<style>h1{color:#fff;text-shadow:0 3px 22px rgba(0,0,0,.75),0 1px 2px rgba(0,0,0,.6)}.lt{position:absolute;left:0;bottom:36px;width:487px}</style>"
        hd=head(sc["headline"]) if sc.get("headline") else ""
        lt=sc.get("lt")
        ltx=f"<div class=lt style='{A('fu',.5,lt.get('d',.8))}'><div style='display:flex;align-items:stretch;background:rgba(10,10,20,.72);border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,.18)'><div style='width:8px;background:{TONE}'></div><div style='padding:12px 16px;color:#fff'><div style='font-size:17px;font-weight:800;letter-spacing:1.4px;opacity:.75'>{lt['tag']}</div><div style='font-size:28px;font-weight:700;line-height:1.1;margin-top:3px'>{lt['text']}</div></div></div></div>" if lt else ""
        body=hd+ltx
    elif t=="question":
        body=head(sc["headline"])+f"<div class=card style='margin-top:60px;padding:36px;display:flex;gap:22px;align-items:center;{A('pop',.6,.6)}'><div style='width:70px;height:70px;border-radius:50%;background:{LIME};display:flex;align-items:center;justify-content:center;font-size:42px;flex:none'>?</div><div style='font-size:40px;font-weight:600;line-height:1.2'>{sc['q']}</div></div>"
    extra=""
    pre=locals().get('pre','')
    if BAD: extra+=f"<style>.hl{{background:{TONE}}}</style>"
    if sc.get("flash"): extra+=f"<div style='position:absolute;inset:0;background:#E5322D;pointer-events:none;{A('flash',.7,sc['flash'],'ease-out')}'></div>"
    if False:
        import random; random.seed(7); cols=["#FF6B6B","#FFD23F","#3BCEAC","#5B8DEF","#B084F5","#fff"]
        extra+="".join(f"<i style='position:absolute;left:{random.randint(60,660)}px;top:150px;width:{random.randint(9,15)}px;height:{random.randint(14,22)}px;background:{random.choice(cols)};border:1.5px solid #111;border-radius:3px;animation:fall {random.uniform(1.6,2.6):.2f}s ease-in {sc['confetti']+random.random()*.9:.2f}s both'></i>" for _ in range(34))
    return f"<html><head><style>{CSS}</style>{extra if BAD else ''}</head><body>{pre}{extra if not BAD else extra.replace('<style>.hl{background:'+TONE+'}</style>','')}<div class=safe style='{A('sc',.3,0)}{';animation:sc .3s ease both,camera '+str(dur)+'s linear both' if sc.get('cine') else ''}'>{body}</div>{CINE if sc.get('cine') else ''}</body></html>"
# ---------- audio fx / music
def tone(f,d,sr,vol=.25,dec=18):
    t=np.arange(int(d*sr))/sr; return (np.sin(2*np.pi*f*t)*np.exp(-dec*t)*vol).astype(np.float32)
def place(fx,sr,t,p,g=1.0):
    i=int(t*sr)
    if i<0 or i>=len(fx): return
    q=p[:len(fx)-i]; fx[i:i+len(q)]+=q*g
def pop(sr,f=620,vol=.3):
    t=np.arange(int(.12*sr))/sr; fr=f*(1+1.2*np.exp(-40*t)); return (np.sin(2*np.pi*np.cumsum(fr)/sr)*np.exp(-30*t)*vol).astype(np.float32)
def thud(sr,f=70,d=.5,vol=.5):
    t=np.arange(int(d*sr))/sr; fr=f*(1+1.5*np.exp(-25*t)); return (np.sin(2*np.pi*np.cumsum(fr)/sr)*np.exp(-9*t)*vol).astype(np.float32)
def buzz(sr,f=150,d=.32,vol=.22):
    t=np.arange(int(d*sr))/sr; w=np.sign(np.sin(2*np.pi*f*t))*.6+np.sin(2*np.pi*f*2.01*t)*.4; return (w*np.minimum(1,t*80)*np.exp(-5*t)*vol).astype(np.float32)
def ding(sr,f=1175,vol=.2):
    t=np.arange(int(.9*sr))/sr; return ((np.sin(2*np.pi*f*t)+.4*np.sin(2*np.pi*f*2.76*t))*np.exp(-5*t)*vol).astype(np.float32)
def sparkle(sr,vol=.12):
    out=np.zeros(int(.7*sr),dtype=np.float32)
    for k,f in enumerate([1568,2093,2637,3136]):
        p=tone(f,.25,sr,vol,14); j=int(k*.06*sr); out[j:j+len(p)]+=p
    return out
def mix(v,sr,scenes,total):
    n=len(v); fx=np.zeros(n,dtype=np.float32)
    for sc,s in zip(spec["scenes"],scenes):
        t0=s["start"]; place(fx,sr,t0+.05,pop(sr,520,.18))
        ty=sc["type"]; bad=sc.get("tone")=="bad"
        if ty=="stat":
            for k in range(10): place(fx,sr,t0+.5+k*.085,tone(500+k*60,.1,sr,.1,30))
            place(fx,sr,t0+1.5,thud(sr,60,.7,.7))
            if bad: place(fx,sr,t0+1.5,buzz(sr,110,.5,.25))
        if ty=="pills":
            for i in range(len(sc["items"])): place(fx,sr,t0+sc.get("dim",2.2)+i*.15,buzz(sr,160-i*12,.28,.2))
        if ty=="chats":
            for k in range(len(sc["rows"])): place(fx,sr,t0+.9+k*.3,ding(sr,1568,.1)[:int(.4*sr)])
        if ty=="stage":
            for ob in sc["objects"]:
                d=t0+ob.get("d",.3); k=ob["k"]
                if k=="bubble": place(fx,sr,d,pop(sr,700 if ob["text"] not in("!!","?") else 420,.28))
                elif k=="person": place(fx,sr,d+.3,thud(sr,90,.18,.22)); place(fx,sr,d+.5,thud(sr,85,.18,.18))
                elif k=="sign": place(fx,sr,d,ding(sr,1319,.22))
                elif k=="phone" and ob.get("spinner"): place(fx,sr,d,buzz(sr,130,.45,.22))
                elif k=="float": place(fx,sr,d,sparkle(sr))
        if ty=="promo":
            for e in sc["els"]:
                k=e["k"]; d=e.get("d",.3)
                if k not in("space","confetti"): place(fx,sr,t0+d+.05,pop(sr,560,.2))
                if k=="phone":
                    for m in e["msgs"]: place(fx,sr,t0+m["d"]+.05,pop(sr,880 if m["from"]=="me" else 620,.22))
                    for tt,nb in e.get("badge",[]): place(fx,sr,t0+tt,tone(1300,.08,sr,.12,30))
                if k=="moon":
                    for tt,nb in e.get("badge",[]): place(fx,sr,t0+tt,tone(1100+nb*40,.08,sr,.12,30))
                if k=="toggles":
                    for i in range(len(e["items"])): place(fx,sr,t0+d+.9+i*.85,pop(sr,1000,.3)); place(fx,sr,t0+d+.9+i*.85+.05,ding(sr,1568,.1)[:int(.3*sr)])
                if k=="check":
                    for i in range(len(e["items"])): place(fx,sr,t0+d+.6+i*e.get("gap",.55),ding(sr,1319,.14)[:int(.35*sr)])
                if k=="fan":
                    for i in range(3): place(fx,sr,t0+d+i*.22,pop(sr,640+i*120,.22))
                if k=="bar": place(fx,sr,t0+d+1.6,pop(sr,1100,.3))
                if k=="confetti":
                    for j in range(5): place(fx,sr,t0+d+j*.08,pop(sr,800+j*140,.18))
                if k=="big": place(fx,sr,t0+d+.1,thud(sr,70,.4,.5))
                if k=="notif":
                    for nn in e["items"]: place(fx,sr,t0+nn["d"],ding(sr,1480,.12)[:int(.3*sr)])
                if k=="meter":
                    for i in range(len(e["rows"])): place(fx,sr,t0+d+.6+i*.5,pop(sr,700+i*100,.22))
                if k=="burst": place(fx,sr,t0+d,pop(sr,900,.3)); place(fx,sr,t0+d+.05,sparkle(sr))
                if k=="phone":
                    for t in e.get("buzz",[]): place(fx,sr,t0+t,buzz(sr,140,.25,.18))
        if ty=="cinema":
            for e in sc.get("sfx",[]):
                k=e["k"]; tt=t0+e["t"]
                if k=="thud": place(fx,sr,tt,thud(sr,e.get("f",55),e.get("d",.9),e.get("v",.7)))
                elif k=="ding": place(fx,sr,tt,ding(sr,e.get("f",1319),.2))
                elif k=="buzz": place(fx,sr,tt,buzz(sr,e.get("f",120),e.get("d",.6),.22))
                elif k=="pop": place(fx,sr,tt,pop(sr,e.get("f",520),.25))
                elif k=="spark": place(fx,sr,tt,sparkle(sr))
                elif k=="beat":
                    for j in range(e.get("n",4)): place(fx,sr,tt+j*e.get("gap",.6),thud(sr,48,.35,.55))
        if sc.get("flash"): place(fx,sr,t0+sc["flash"],thud(sr,55,.8,.7))
        if False:
            for k in range(5): place(fx,sr,t0+sc["confetti"]+k*.05,pop(sr,800+k*140,.25))
            for k,f in enumerate([523,659,784,1047]): place(fx,sr,t0+sc["confetti"]+.1+k*.1,ding(sr,f,.16)[:int(.6*sr)])
    # soft music: 96bpm pad + bass + kick, ducked by voice
    bpm=96; spb=60/bpm; t=np.arange(n)/sr; m=np.zeros(n,dtype=np.float32)
    chords=[(220,277,330),(196,247,294),(175,220,262),(196,247,294)]
    for b in range(int(total/(spb*4))+1):
        c=chords[b%4]; i0=int(b*spb*4*sr); L=int(spb*4*sr)
        seg=np.arange(min(L,max(0,n-i0)))/sr
        for f in c: m[i0:i0+len(seg)]+=(np.sin(2*np.pi*f*seg)*.04*np.minimum(1,seg*3)*np.minimum(1,(spb*4-seg)*3)).astype(np.float32)
        for bt in range(4):
            j=i0+int(bt*spb*sr); k=tone(55,.3,sr,.22,9); m[j:j+len(k)]+=k[:max(0,n-j)] if j<n else 0
    env=np.convolve(np.abs(v),np.ones(int(.15*sr))/int(.15*sr),"same"); duck=1-.7*np.clip(env*6,0,1)
    out=v*1.0+fx+m*duck*.55
    out/=max(1,np.max(np.abs(out))/.95); return out
# ---------- video
async def render(scenes,total):
    from playwright.async_api import async_playwright
    FPS=30; fdir=os.path.join(TMP,"f"); shutil.rmtree(fdir,ignore_errors=True); os.makedirs(fdir); n=0
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path=shutil.which("google-chrome") or "/usr/bin/google-chrome",args=["--no-sandbox","--allow-file-access-from-files"])
        pg=await b.new_page(viewport={"width":720,"height":1280},device_scale_factor=1.5)
        for si,(sc,s) in enumerate(zip(spec["scenes"],scenes)):
            f=os.path.join(TMP,f"s{si}.html"); sc["cine"]=spec.get("cine",False); sc["_tl"]=[(a-s["start"],d) for a,d in s["lines"]]; open(f,"w").write(scene_html(sc,s["dur"])); await pg.goto("file://"+f); await pg.wait_for_timeout(300)
            await pg.evaluate("document.getAnimations().forEach(a=>a.pause())")
            if STILLS:
                tq=max(0.5,s['dur']-0.55); await pg.evaluate("(t)=>document.getAnimations().forEach(a=>a.currentTime=t*1000)",tq); await pg.evaluate(SETCNT,tq)
                iss=await pg.evaluate(QA_JS)
                for i in iss: QA_ISSUES.append(f"scene {si+1}: {i}")
                await pg.screenshot(path=os.path.join(OUT,f"{spec['slug']}_still{si+1}.png")); continue
            nf=int(round(s["dur"]*FPS))
            for k in range(nf):
                t=k/FPS
                await pg.evaluate("(t)=>document.getAnimations().forEach(a=>a.currentTime=t*1000)",t); await pg.evaluate(SETCNT,t)
                await pg.screenshot(path=os.path.join(fdir,f"{n:05d}.jpg"),type="jpeg",quality=90); n+=1
        await b.close()
    return n

QA_JS="""()=>{const sx=88,sr=575,st=167,sb=1000,tol=3,issues=[];
const safe=document.querySelector('.safe'); safe.style.animation='none'; const svg=document.querySelector('svg.stage'); const sv=svg?svg.getBoundingClientRect():null;
const els=[...safe.querySelectorAll('*')].filter(e=>{const c=e.children.length===0||e.tagName==='IMG'||e.tagName==='svg'; return c && !(e.parentElement&&e.parentElement.closest('[style*="overflow:hidden"]'))});
for(const e of els){ if(e.closest('svg')&&e.tagName!=='svg') continue; const r=(e.tagName==='IMG'?e.parentElement:e).getBoundingClientRect(); if(r.width<2||r.height<2) continue; const cs=getComputedStyle(e); if(parseFloat(cs.opacity)<0.05) continue;
 if(r.left<sx-tol||r.right>sr+tol||r.top<st-tol||r.bottom>sb+tol) issues.push('outside safe area: '+(e.className&&e.className.baseVal!==undefined?e.className.baseVal:e.className||e.tagName)+' '+(e.textContent||'').slice(0,30)+' ['+[r.left,r.top,r.right,r.bottom].map(Math.round)+']');
 if(e.scrollWidth>e.clientWidth+2&&cs.overflow!=='visible'&&e.tagName!=='svg') issues.push('text overflow: '+(e.textContent||'').slice(0,30));}
if(sv){for(const a of document.querySelectorAll('svg.stage .chk')){const r=a.getBoundingClientRect(); if(r.width<2) continue; if(r.left<sv.left-tol||r.right>sv.right+tol||r.top<sv.top-tol||r.bottom>sv.bottom+tol) issues.push('stage object clipped: '+Math.round(r.left-sv.left)+','+Math.round(r.top-sv.top)+','+Math.round(r.right-sv.left)+','+Math.round(r.bottom-sv.top));}}
const hs=[...document.querySelectorAll('h1')]; const sr2=svg?svg.getBoundingClientRect():(document.querySelector('.safe > div:not(h1)')||{getBoundingClientRect:()=>null}).getBoundingClientRect(); if(hs.length&&sr2){const hb=hs[hs.length-1].getBoundingClientRect(); if(hb.bottom>sr2.top+2) issues.push('headline overlaps visual by '+Math.round(hb.bottom-sr2.top)+'px');}
return issues;}"""
QA_ISSUES=[]
SETCNT="""(t)=>{const c=document.getElementById('cnt'); if(!c) return; const to=parseFloat(c.dataset.to); const x=Math.max(0,Math.min(1,(t-0.5)/1.0)); const e=1-Math.pow(1-x,3); const dec=parseInt(c.dataset.dec||'0'); c.textContent=c.dataset.pre+(to*e).toFixed(dec)+c.dataset.suf;}"""
def main():
    v,sr,scenes,total=tts(); print("voice total",round(total,1),"s",flush=True)
    n=asyncio.run(render(scenes,total))
    if STILLS:
        open(os.path.join(OUT,spec['slug']+'.qa.txt'),'w').write('\n'.join(QA_ISSUES) or 'QA OK'); print('QA:',QA_ISSUES or 'OK'); return
    audio=mix(v,sr,scenes,total); sf.write(os.path.join(TMP,"a.wav"),audio,sr)
    mp4=os.path.join(OUT,spec["slug"]+".mp4")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","30","-i",os.path.join(TMP,"f","%05d.jpg"),"-i",os.path.join(TMP,"a.wav"),"-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-vf","scale=1080:1920","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",mp4],check=True)
    open(os.path.join(OUT,spec["slug"]+".caption.txt"),"w").write(spec["caption"]); print("DONE",mp4,flush=True)
main()
