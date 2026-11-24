"""Promo scene type: soft light stage, floating UI cards, word-phrase captions with bold keywords (blur-in).
Inspired by the clean product-promo format: prompt card typing, 'working' checklist, stacked cards, comment/DM bar."""
import re
from icons import icon

INK = "#14161d"; ACC = "#C8F169"; SHADOW = "0 18px 40px rgba(20,22,29,.14),0 2px 6px rgba(20,22,29,.08)"
CSS = """<style>
@keyframes blurin{from{opacity:0;filter:blur(12px);transform:translateY(14px)}to{opacity:1;filter:blur(0);transform:none}}
@keyframes fadeo{to{opacity:0;filter:blur(8px)}}
@keyframes cardin{from{opacity:0;transform:translateY(40px) scale(.94)}to{opacity:1;transform:none}}
@keyframes type{from{width:0}to{width:100%}}
@keyframes caret{50%{opacity:0}}
@keyframes tick{0%{transform:scale(0)}70%{transform:scale(1.25)}100%{transform:scale(1)}}
@keyframes floaty2{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
@keyframes fan{from{opacity:0;transform:translate(0,30px) rotate(0)}to{opacity:1;transform:translate(var(--dx),var(--dy)) rotate(var(--r))}}
@keyframes pcam{from{transform:perspective(1100px) rotateX(5deg) rotateY(-6deg) scale(1.05)}to{transform:perspective(1100px) rotateX(0) rotateY(3deg) scale(1)}}
@keyframes pexit{to{opacity:0;transform:scale(1.05);filter:blur(7px)}}
@keyframes blobA{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(60px,-80px) scale(1.2)}}
@keyframes blobB{0%,100%{transform:translate(0,0) scale(1.1)}50%{transform:translate(-70px,60px) scale(.9)}}
@keyframes zz{0%{opacity:0;transform:translate(0,0) scale(.5)}30%{opacity:1}100%{opacity:0;transform:translate(40px,-110px) scale(1.4)}}
@keyframes ripple{0%{opacity:.9;transform:scale(.2)}100%{opacity:0;transform:scale(2.4)}}
@keyframes confall{0%{opacity:0;transform:translateY(-60px) rotate(0)}15%{opacity:1}100%{opacity:1;transform:translateY(760px) rotate(540deg)}}
@keyframes spin360{to{transform:rotate(360deg)}}
@keyframes shk{0%,100%{transform:translateX(0)}20%{transform:translateX(-9px)}40%{transform:translateX(8px)}60%{transform:translateX(-5px)}80%{transform:translateX(3px)}}
@keyframes nin{from{opacity:0;transform:translateX(140px) scale(.9)}to{opacity:1;transform:none}}
@keyframes barg{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes bigpop{0%{opacity:0;transform:scale(.6);filter:blur(10px)}100%{opacity:1;transform:none;filter:blur(0)}}
.pc{background:#fff;border-radius:24px;box-shadow:SHADOWVAL;border:1px solid rgba(20,22,29,.06)}
</style>""".replace('SHADOWVAL',SHADOW)


def _cap(sc, tl):
    out = ""
    for j, phrases in enumerate(sc.get("caps", [])):
        t0, d = tl[j]; n = len(phrases)
        for k, p in enumerate(phrases):
            a = t0 + d * k / n; b = (t0 + d * (k + 1) / n) if k < n - 1 else t0 + d + .35
            txt = re.sub(r"\*(.+?)\*", r"<b style='font-weight:800'>\1</b>", p)
            out += (f"<div style='position:absolute;left:0;width:487px;bottom:{sc.get('capy', 64)}px;text-align:center;font-size:{sc.get('capsize', 54)}px;font-weight:500;letter-spacing:-1.2px;line-height:1.08;color:{INK};opacity:0;"
                    f"animation:blurin .32s ease {a:.2f}s both,fadeo .22s ease {b-.22:.2f}s forwards'>{txt}</div>")
    return out


def _el(e):
    k = e["k"]; d = e.get("d", .3)
    if k == "prompt":
        return (f"<div class=pc style='padding:22px 22px 18px;animation:cardin .6s cubic-bezier(.2,.8,.2,1) {d}s both'>"
                f"<div style='display:flex;align-items:center;gap:12px'><div style='width:44px;height:44px;border-radius:14px;background:{ACC};display:flex;align-items:center;justify-content:center'>{icon(e.get('icon','sparkles'),24,INK,2.2)}</div>"
                f"<div style='font-weight:700;font-size:22px;color:{INK}'>{e.get('who','Your idea')}</div></div>"
                f"<div style='margin-top:16px;font-size:27px;font-weight:500;line-height:1.25;color:{INK};border:1.5px solid rgba(20,22,29,.1);border-radius:16px;padding:16px 18px'>"
                f"<div style='display:flex;align-items:center'><span style='display:inline-block;overflow:hidden;white-space:nowrap;animation:type {e.get('type',1.6)}s steps(28) {d+.5}s both;flex:none;max-width:calc(100% - 12px)'>{e['text']}</span><span style='animation:caret .8s step-end infinite;color:{INK};margin-left:2px'>|</span></div></div></div>")
    if k == "check":
        rows = "".join(f"<div style='display:flex;align-items:center;gap:14px;padding:13px 4px;border-top:{'0' if i == 0 else '1px solid rgba(20,22,29,.07)'};font-size:27px;font-weight:600;color:{INK};opacity:0;animation:blurin .35s ease {d+.5+i*e.get('gap',.55):.2f}s both'>"
                       f"<span style='width:30px;height:30px;border-radius:50%;background:{ACC};display:flex;align-items:center;justify-content:center;flex:none;animation:tick .35s ease {d+.6+i*e.get('gap',.55):.2f}s both'>{icon('check',18,INK,3.4)}</span>{x}</div>" for i, x in enumerate(e["items"]))
        return (f"<div class=pc style='padding:20px 24px 12px;animation:cardin .6s cubic-bezier(.2,.8,.2,1) {d}s both'>"
                f"<div style='font-size:15px;font-weight:800;letter-spacing:1.6px;color:rgba(20,22,29,.5);margin-bottom:8px'>{e.get('title','WORKING ON IT')}</div>{rows}</div>")
    if k == "fan":
        cs = ""
        pos = [(-140, 18, -8), (0, 0, 0), (140, 30, 8)]
        for i, c in enumerate(e["cards"][:3]):
            dx, dy, r = pos[i]
            cs += (f"<div class=pc style='position:absolute;left:{243-95}px;top:0;width:190px;height:{e.get('h',300)}px;padding:18px;--dx:{dx}px;--dy:{dy}px;--r:{r}deg;opacity:0;animation:fan .7s cubic-bezier(.2,.8,.2,1) {d+i*.22:.2f}s both;background:{c.get('bg','#fff')}'>"
                   f"<div style='width:52px;height:52px;border-radius:16px;background:{c.get('c', ACC)};display:flex;align-items:center;justify-content:center'>{icon(c['icon'],28,INK,2.2)}</div>"
                   f"<div style='margin-top:18px;font-size:24px;font-weight:800;line-height:1.1;color:{INK}'>{c['t']}</div><div style='margin-top:8px;font-size:17px;font-weight:500;color:rgba(20,22,29,.6);line-height:1.2'>{c.get('s','')}</div></div>")
        return f"<div style='position:relative;height:{e.get('h',300)+60}px;width:487px'>{cs}</div>"
    if k == "big":
        return (f"<div style='text-align:center;opacity:0;animation:bigpop .6s cubic-bezier(.2,.8,.2,1) {d}s both'><div style='font-size:{e.get('size',210)}px;font-weight:800;letter-spacing:-8px;line-height:1;color:{INK}'>{e['text']}</div>"
                f"<div style='font-size:28px;font-weight:600;color:rgba(20,22,29,.5);margin-top:4px'>{e.get('sub','')}</div></div>")
    if k == "chips":
        return "<div style='display:flex;flex-wrap:wrap;gap:12px;justify-content:center'>" + "".join(
            f"<div style='background:#fff;border-radius:999px;box-shadow:{SHADOW};padding:12px 18px;font-size:23px;font-weight:700;color:{INK};opacity:0;animation:cardin .45s ease {d+i*.3:.2f}s both'>{x}</div>" for i, x in enumerate(e["items"])) + "</div>"
    if k == "bar":  # comment / DM bar with typed keyword
        return (f"<div class=pc style='display:flex;align-items:center;gap:14px;padding:14px 18px;border-radius:999px;animation:cardin .6s ease {d}s both'>"
                f"<div style='width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#ff7a59,#c8f169);flex:none'></div>"
                f"<div style='flex:1;font-size:30px;font-weight:700;color:{INK}'><div style='display:flex;align-items:center'><span style='display:inline-block;overflow:hidden;white-space:nowrap;animation:type {e.get('type',.9)}s steps({len(e['text'])}) {d+.6}s both'>{e['text']}</span><span style='animation:caret .8s step-end infinite;margin-left:2px'>|</span></div></div>"
                f"<div style='font-size:24px;font-weight:700;color:#2d8cf0'>Send</div></div>")
    if k == "space": return f"<div style='height:{e.get('h',30)}px'></div>"
    return ""



def _cursor(e, pts, d):
    """pts: list of (x,y,tclick) relative to element; returns cursor + ripples html"""
    kf=[]; tot=pts[-1][2]-d+.8
    t0=d
    kf.append(f"0%{{opacity:0;transform:translate({pts[0][0]+120}px,{pts[0][1]-120}px)}}")
    out=""
    for i,(x,y,tc) in enumerate(pts):
        p=max(0,min(100,(tc-.25-t0)/tot*100)); q=min(100,(tc-t0)/tot*100)
        kf.append(f"{p:.1f}%{{opacity:1;transform:translate({x}px,{y}px)}}")
        kf.append(f"{q:.1f}%{{opacity:1;transform:translate({x}px,{y}px) scale(.82)}}")
        out+=f"<div style='position:absolute;left:{x-26}px;top:{y-26}px;width:52px;height:52px;border-radius:50%;background:rgba(20,22,29,.25);opacity:0;animation:ripple .5s ease-out {tc:.2f}s both'></div>"
    kf.append(f"100%{{opacity:0;transform:translate({pts[-1][0]+60}px,{pts[-1][1]+40}px)}}")
    name="cur%d"%int(d*100)
    cur=(f"<style>@keyframes {name}{{{''.join(kf)}}}</style><div style='position:absolute;left:0;top:0;width:34px;height:34px;opacity:0;animation:{name} {tot:.2f}s ease-in-out {t0:.2f}s both;z-index:5'>"
         "<svg width='34' height='34' viewBox='0 0 24 24'><path d='M4 2 L4 19 L8.5 15 L11.5 21 L14 20 L11 14 L17 14Z' fill='#14161d' stroke='#fff' stroke-width='1.6' stroke-linejoin='round'/></svg></div>")
    return out+cur

def _el2(e):
    k=e["k"]; d=e.get("d",.3)
    if k=="phone":
        ms=""
        for i,m in enumerate(e["msgs"]):
            me=m["from"]=="me"
            ms+=(f"<div style='display:flex;justify-content:{'flex-end' if me else 'flex-start'};margin-top:10px;opacity:0;animation:cardin .4s cubic-bezier(.2,.8,.2,1) {m['d']:.2f}s both'>"
                 f"<div style='max-width:80%;padding:10px 14px;border-radius:18px;font-size:19px;font-weight:600;line-height:1.2;background:{ACC if me else '#fff'};color:{INK};box-shadow:0 2px 6px rgba(20,22,29,.1)'>{m['text']}{'<span style=\"font-size:13px;margin-left:8px;color:#2d8cf0\">✓✓</span>' if me else ''}</div></div>")
        badge=""
        if e.get("badge"):
            nums=e["badge"]  # list of (t, n)
            for i,(t,n) in enumerate(nums):
                tn=nums[i+1][0] if i+1<len(nums) else None
                badge+=(f"<span style='position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0;animation:tick .3s ease {t:.2f}s both"+(f",fadeo .12s ease {tn-.12:.2f}s forwards" if tn else "")+f"'>{n}</span>")
            badge=f"<div style='position:absolute;right:-18px;top:-18px;width:56px;height:56px;border-radius:50%;background:#ff4a3d;color:#fff;font-weight:800;font-size:28px;box-shadow:0 6px 14px rgba(255,74,61,.4);z-index:4'>{badge}</div>"
        buz=''.join(f',shk .45s linear {t:.2f}s both' for t in e.get('buzz',[]))
        return (f"<div style='display:flex;justify-content:center;animation:cardin .7s cubic-bezier(.2,.8,.2,1) {d}s both{buz}'><div style='position:relative;width:292px;height:{e.get('h',470)}px;border-radius:44px;background:#14161d;padding:9px;box-shadow:{SHADOW};animation:floaty2 3s ease-in-out {d+.7}s infinite'>{badge}"
                f"<div style='width:100%;height:100%;border-radius:36px;background:#efeae2;overflow:hidden;position:relative'><div style='background:#14161d;color:#fff;padding:16px 18px 12px;display:flex;align-items:center;gap:10px'><div style='width:34px;height:34px;border-radius:50%;background:{ACC}'></div><div><div style='font-size:18px;font-weight:700'>{e.get('who','Your shop')}</div><div style='font-size:13px;opacity:.7'>{e.get('time','00:14')}</div></div></div><div style='padding:6px 14px'>{ms}</div></div></div></div>")
    if k=="toggles":
        rows="";pts=[]
        for i,x in enumerate(e["items"]):
            tc=d+.9+i*.85
            rows+=(f"<div style='display:flex;align-items:center;justify-content:space-between;height:74px;border-top:{'0' if i==0 else '1px solid rgba(20,22,29,.07)'};font-size:27px;font-weight:700;color:{INK};opacity:0;animation:blurin .4s ease {d+.4+i*.2:.2f}s both'><span>{x}</span>"
                   f"<span style='position:relative;width:70px;height:40px;border-radius:20px;background:#d5d6da;animation:trk .25s ease {tc:.2f}s both;flex:none'><i style='position:absolute;left:4px;top:4px;width:32px;height:32px;border-radius:50%;background:#fff;box-shadow:0 2px 5px rgba(0,0,0,.25);animation:knob .25s cubic-bezier(.3,1.5,.5,1) {tc:.2f}s both'></i></span></div>")
            pts.append((395,24+60+i*74+37-8,tc))
        css="<style>@keyframes trk{to{background:"+ACC+"}}@keyframes knob{to{transform:translateX(30px)}}</style>"
        return css+(f"<div class=pc style='position:relative;padding:24px 24px 14px;animation:cardin .6s cubic-bezier(.2,.8,.2,1) {d}s both'><div style='font-size:15px;font-weight:800;letter-spacing:1.6px;color:rgba(20,22,29,.5);margin-bottom:6px'>{e.get('title','TOOLS')}</div>{rows}{_cursor(e,pts,d+.2)}</div>")
    if k=="orbit":
        r=e.get("r",132); ch=""
        for i,x in enumerate(e["items"]):
            import math
            a=2*math.pi*i/len(e["items"])-math.pi/2
            cx=170+r*math.cos(a); cy=170+r*math.sin(a)
            ch+=(f"<div style='position:absolute;left:{cx:.0f}px;top:{cy:.0f}px;width:0;height:0'><div style='transform:translate(-50%,-50%);'><div style='white-space:nowrap;background:#fff;border-radius:999px;box-shadow:{SHADOW};padding:11px 18px;font-size:22px;font-weight:800;color:{INK};animation:spin360 9s linear {d}s infinite reverse'>{x}</div></div></div>")
        return (f"<div style='position:relative;width:340px;height:340px;margin:0 auto;opacity:0;animation:cardin .6s ease {d}s both'><div style='position:absolute;left:30px;top:30px;width:280px;height:280px;border-radius:50%;border:2px dashed rgba(20,22,29,.18)'></div>"
                f"<div style='position:absolute;left:105px;top:105px;width:130px;height:130px;border-radius:50%;background:{ACC};box-shadow:{SHADOW};display:flex;align-items:center;justify-content:center;animation:bigpop .6s ease {d+.2}s both'>{icon(e.get('icon','message-circle'),64,INK,2.2)}</div>"
                f"<div style='position:absolute;inset:0;animation:spin360 9s linear {d}s infinite'>{ch}</div></div>")
    if k=="moon":
        zs="".join(f"<div style='position:absolute;left:{150+i*22}px;top:{20-i*8}px;font-size:{34+i*10}px;font-weight:800;color:{INK};opacity:0;animation:zz 1.8s ease-out {d+.5+i*.55:.2f}s infinite'>Z</div>" for i in range(3))
        nums=e.get("badge",[]); b=""
        for i,(t,n) in enumerate(nums):
            tn=nums[i+1][0] if i+1<len(nums) else None
            b+=(f"<span style='position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0;animation:tick .28s ease {t:.2f}s both"+(f",fadeo .1s ease {tn-.1:.2f}s forwards" if tn else "")+f"'>{n}</span>")
        return (f"<div style='position:relative;width:300px;height:300px;margin:0 auto;opacity:0;animation:bigpop .6s ease {d}s both'><div style='position:absolute;left:50px;top:70px;width:200px;height:200px;border-radius:50%;background:#14161d;display:flex;align-items:center;justify-content:center;box-shadow:{SHADOW}'>{icon('moon',104,ACC,2)}</div>{zs}"
                f"<div style='position:absolute;right:20px;top:60px;width:72px;height:72px;border-radius:50%;background:#ff4a3d;color:#fff;font-weight:800;font-size:36px;box-shadow:0 8px 18px rgba(255,74,61,.45)'>{b}</div></div>")

    if k=="notif":
        o=""
        for i,n in enumerate(e["items"]):
            o+=(f"<div style='display:flex;align-items:center;gap:12px;background:#fff;border-radius:18px;box-shadow:{SHADOW};padding:12px 16px;opacity:0;animation:nin .45s cubic-bezier(.2,.9,.3,1.2) {n['d']:.2f}s both'>"
                f"<div style='width:40px;height:40px;border-radius:12px;background:{ACC};display:flex;align-items:center;justify-content:center;flex:none'>{icon('message-circle',22,INK,2.4)}</div>"
                f"<div><div style='font-size:15px;font-weight:800;letter-spacing:.8px;color:rgba(20,22,29,.5)'>WHATSAPP · {n.get('time','NOW')}</div><div style='font-size:23px;font-weight:700;color:{INK}'>{n['text']}</div></div></div>")
        return f"<div style='display:flex;flex-direction:column;gap:12px'>{o}</div>"
    if k=="meter":
        o=""
        for i,(lab,w) in enumerate(e["rows"]):
            dd=d+.4+i*.5
            o+=(f"<div style='margin-top:14px;opacity:0;animation:blurin .4s ease {dd:.2f}s both'><div style='display:flex;justify-content:space-between;font-size:22px;font-weight:700;color:{INK}'><span>{lab}</span><span style='color:rgba(20,22,29,.5)'>{w}%</span></div>"
                f"<div style='height:16px;border-radius:8px;background:rgba(20,22,29,.08);margin-top:6px;overflow:hidden'><div style='height:100%;width:{w}%;border-radius:8px;background:{ACC};transform-origin:left;animation:barg .9s cubic-bezier(.2,.8,.2,1) {dd+.2:.2f}s both'></div></div></div>")
        return f"<div class=pc style='padding:10px 24px 22px;animation:cardin .6s ease {d}s both'>{o}</div>"
    if k=="burst":
        import math
        o=""
        for i in range(14):
            a=2*math.pi*i/14; x=math.cos(a)*170; y=math.sin(a)*170
            o+=f"<i style='position:absolute;left:50%;top:50%;width:{14 if i%2 else 22}px;height:{14 if i%2 else 22}px;margin:-8px;border-radius:50%;background:{[ACC,'#ff7a59','#8aa7ff'][i%3]};opacity:0;--dx:{x:.0f}px;--dy:{y:.0f}px;--r:0deg;animation:fan .7s cubic-bezier(.2,.8,.2,1) {d+i*.02:.2f}s both'></i>"
        return f"<div style='position:relative;height:{e.get('h',10)}px'>{o}</div>"
    if k=="confetti":
        import random; r=random.Random(5); cols=[ACC,"#ff7a59","#8aa7ff","#ffd24a","#14161d"]; o=""
        for i in range(26):
            o+=f"<i style='position:absolute;left:{r.randint(0,480)}px;top:-40px;width:{r.randint(9,15)}px;height:{r.randint(12,20)}px;background:{r.choice(cols)};border-radius:3px;opacity:0;animation:confall {r.uniform(1.6,2.6):.2f}s ease-in {e.get('d',1)+r.uniform(0,.5):.2f}s both'></i>"
        return f"<div style='position:absolute;left:0;top:0;width:487px;height:760px;overflow:hidden;pointer-events:none'>{o}</div>"
    if k=="shake":
        return f"<div style='animation:shk .5s linear {d}s both'>{_el(e['inner'])}</div>"
    return None


def _blobs():
    import random; r=random.Random(11); cols=["#d8f59a","#cdd6ff","#ffd9c2","#e6d5ff"]; o=""
    for i in range(6):
        sz=r.randint(220,380)
        o+=f"<div style='position:absolute;left:{r.randint(-80,520)}px;top:{r.randint(100,1000)}px;width:{sz}px;height:{sz}px;border-radius:50%;background:{cols[i%4]};opacity:.55;filter:blur(55px);animation:blob{'AB'[i%2]} {r.uniform(5,8):.1f}s ease-in-out infinite'></div>"
    return o

def render(sc, dur, tl):
    pre = ("<div style='position:absolute;inset:0;background:radial-gradient(circle at 50% 36%,#fbfbfb 0,#ececee 58%,#d9d9dc 100%)'></div>" + _blobs() + CSS)
    els = "".join((_el2(e) if _el2(e) is not None else _el(e)) for e in sc["els"])
    top = sc.get("top", 90)
    body = (f"<div style='position:relative;margin-top:{top}px;display:flex;flex-direction:column;gap:{sc.get('gap', 26)}px;align-items:stretch;width:487px;transform-origin:50% 40%;animation:pcam {dur:.2f}s cubic-bezier(.2,.7,.2,1) both,pexit .25s ease {max(.5,dur-.3):.2f}s forwards'>{els}</div>"
            + _cap(sc, tl))
    return pre, body
