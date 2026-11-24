from icons import icon_at
"""Flat outlined people + props as inline SVG (moodbod illustrated style). Coordinates: person is 100x205 local units."""
INK="#1c2033"
SKIN={"a":"#8d5a3b","b":"#6b4226","c":"#c68642","d":"#e0ac69","e":"#f1c27d"}
SHIRT={"lav":"#d9d3f0","cream":"#f7e3b2","lime":"#e3ee9a","blue":"#bcd8f5","pink":"#f6c6cf","white":"#f4f4f4"}
HAIR="#231f20"; TROU="#34385a"
ARMS={ # (shoulder, elbow, hand) per side
 "stand":{"L":[(30,60),(22,90),(22,116)],"R":[(70,60),(78,90),(78,116)]},
 "wave":{"L":[(30,60),(22,90),(22,116)],"R":[(70,60),(90,48),(92,20)]},
 "phone":{"L":[(30,60),(22,90),(22,116)],"R":[(70,60),(84,76),(66,40)]},
 "hold":{"L":[(30,60),(30,92),(45,88)],"R":[(70,60),(70,92),(55,88)]},
 "shrug":{"L":[(30,60),(12,80),(18,98)],"R":[(70,60),(88,80),(82,98)]},
 "point":{"L":[(30,60),(22,90),(22,116)],"R":[(70,60),(94,62),(112,58)]},
 "cross":{"L":[(30,60),(26,92),(58,90)],"R":[(70,60),(74,92),(42,94)]},
 "watch":{"L":[(30,60),(22,90),(22,116)],"R":[(70,60),(84,86),(58,80)]},
 "up":{"L":[(30,60),(10,48),(8,20)],"R":[(70,60),(90,48),(92,20)]},
}
def _arm(pts,shirt,skin):
    d="M"+" L".join(f"{x} {y}" for x,y in pts); hx,hy=pts[-1]
    return (f"<path d='{d}' fill='none' stroke='{INK}' stroke-width='17' stroke-linecap='round' stroke-linejoin='round'/>"
            f"<path d='{d}' fill='none' stroke='{shirt}' stroke-width='11' stroke-linecap='round' stroke-linejoin='round'/>"
            f"<circle cx='{hx}' cy='{hy}' r='7' fill='{skin}' stroke='{INK}' stroke-width='3'/>")
def face(expr):
    eyes=f"<circle cx='43' cy='31' r='2.4' fill='{INK}'/><circle cx='57' cy='31' r='2.4' fill='{INK}'/>"
    m={"smile":f"<path d='M42 39 Q50 46 58 39' fill='none' stroke='{INK}' stroke-width='2.6' stroke-linecap='round'/>",
       "frown":f"<path d='M43 43 Q50 37 57 43' fill='none' stroke='{INK}' stroke-width='2.6' stroke-linecap='round'/><path d='M38 24 L46 26 M62 24 L54 26' stroke='{INK}' stroke-width='2.4' stroke-linecap='round'/>",
       "worried":f"<path d='M43 43 Q50 39 57 43' fill='none' stroke='{INK}' stroke-width='2.6' stroke-linecap='round'/><path d='M38 26 L46 23 M62 26 L54 23' stroke='{INK}' stroke-width='2.4' stroke-linecap='round'/>",
       "open":f"<ellipse cx='50' cy='41' rx='4' ry='5' fill='{INK}'/>"}[expr]
    return eyes+m
def _wrap_pivot(inner,px,py,style):
    return f"<g transform='translate({px},{py})'><g style='transform-origin:0 0;transform-box:view-box;{style}'><g transform='translate({-px},{-py})'>{inner}</g></g></g>"
def _hair(style,col=HAIR):
    st=f"stroke='{INK}' stroke-width='2.5' stroke-linejoin='round'"
    if style=="bald": return "",""
    cap=f"<path d='M32 29 Q32 9 50 9 Q68 9 68 29 Q60 19 50 20 Q40 19 32 29Z' fill='{col}' {st}/>"
    if style=="long":
        back=f"<path d='M30 30 Q28 8 50 8 Q72 8 70 30 L72 78 Q50 84 28 78Z' fill='{col}' {st}/>"
        return back,cap
    if style=="bun": return f"<circle cx='50' cy='5' r='9' fill='{col}' {st}/>",cap
    if style=="afro": return f"<circle cx='50' cy='20' r='26' fill='{col}' {st}/>",cap.replace(f"fill='{col}'","fill='none'").replace("stroke-width='2.5'","stroke-width='0'")
    return "",cap
def person(skin="a",shirt="lav",pose="stand",expr="smile",apron=None,hat=False,hair="short",phone=False,dress=None,anim=None,expr2=None,expr2_at=0,sweat=False,hairc=None):
    s=SKIN[skin]; sh=SHIRT[shirt]; arms=ARMS[pose]; hc=hairc or HAIR
    g=""
    back,cap=_hair(hair,hc); g+=back
    if dress:
        g+=f"<rect x='34' y='116' width='11' height='72' rx='4' fill='{s}' stroke='{INK}' stroke-width='3'/><rect x='55' y='116' width='11' height='72' rx='4' fill='{s}' stroke='{INK}' stroke-width='3'/>"
        g+=f"<ellipse cx='39' cy='191' rx='12' ry='6' fill='{INK}'/><ellipse cx='61' cy='191' rx='12' ry='6' fill='{INK}'/>"
    else:
        g+=f"<rect x='32' y='116' width='15' height='72' rx='4' fill='{TROU}' stroke='{INK}' stroke-width='3'/><rect x='53' y='116' width='15' height='72' rx='4' fill='{TROU}' stroke='{INK}' stroke-width='3'/>"
        g+=f"<ellipse cx='38' cy='191' rx='13' ry='6' fill='{INK}'/><ellipse cx='62' cy='191' rx='13' ry='6' fill='{INK}'/>"
    larm=_arm(arms["L"],sh,s)
    if anim=="cheer": larm=_wrap_pivot(larm,30,60,"animation:swingL .7s ease-in-out infinite")
    g+=larm
    g+=f"<rect x='28' y='52' width='44' height='68' rx='14' fill='{sh}' stroke='{INK}' stroke-width='3'/>"
    if dress: g+=f"<path d='M30 100 L70 100 L82 150 L18 150Z' fill='{dress}' stroke='{INK}' stroke-width='3' stroke-linejoin='round'/>"
    if apron: g+=f"<rect x='34' y='70' width='32' height='50' rx='6' fill='{apron}' stroke='{INK}' stroke-width='3'/>"
    g+=f"<rect x='45' y='44' width='10' height='12' fill='{s}' stroke='{INK}' stroke-width='3'/>"
    head=f"<circle cx='50' cy='30' r='18' fill='{s}' stroke='{INK}' stroke-width='3'/>{cap}"
    if hat: head+=f"<rect x='34' y='-12' width='32' height='22' rx='8' fill='#fff' stroke='{INK}' stroke-width='3'/><rect x='32' y='6' width='36' height='8' rx='3' fill='#fff' stroke='{INK}' stroke-width='3'/>"
    f1=face(expr)
    if expr2: f1=f"<g style='animation:hide .01s linear {expr2_at}s forwards'>{f1}</g><g style='opacity:0;animation:show .01s linear {expr2_at}s forwards'>{face(expr2)}</g>"
    head+=f1
    if sweat: head+=f"<path d='M72 14 Q76 22 72 26 Q68 22 72 14Z' fill='#7cc4ff' stroke='{INK}' stroke-width='2' style='animation:drip 1.1s ease-in infinite'/>"
    if anim in ("shake","cheer") : head=_wrap_pivot(head,50,48,"animation:shake .45s ease-in-out infinite")
    g+=head
    rarm=_arm(arms["R"],sh,s)
    if phone or pose=="phone":
        hx,hy=arms["R"][-1]; rarm+=f"<rect x='{hx-2}' y='{hy-20}' width='13' height='22' rx='3' fill='#2b2f45' stroke='{INK}' stroke-width='2.5'/>"
    if anim in ("wave","cheer"): rarm=_wrap_pivot(rarm,70,60,"animation:swingR .6s ease-in-out infinite")
    if anim=="watch": rarm=_wrap_pivot(rarm,70,60,"animation:tap 1.2s ease-in-out infinite")
    g+=rarm
    if pose=="hold":
        g+=f"<rect x='41' y='74' width='18' height='28' rx='3' fill='#2b2f45' stroke='{INK}' stroke-width='2.5'/><rect x='43.5' y='77' width='13' height='20' rx='1.5' fill='#fff3cd'/>"
    return g
def actor(x,y,sc,cls_anim,inner,flip=False,chk=True):
    f=f"scale({-sc},{sc}) translate(-100,0)" if flip else f"scale({sc})"
    return f"<g transform='translate({x},{y})'><g class='{'chk ' if chk else ''}a' style='{cls_anim}'><g transform='{f}'>{inner}</g></g></g>"
def bubble(x,y,text,w=84,h=56,anim="",tail="left"):
    tx=x+18 if tail=="left" else x+w-30
    return (f"<g class='chk' style='{anim}'><path d='M{x} {y+12} Q{x} {y} {x+12} {y} L{x+w-12} {y} Q{x+w} {y} {x+w} {y+12} L{x+w} {y+h-12} Q{x+w} {y+h} {x+w-12} {y+h} L{tx+16} {y+h} L{tx} {y+h+16} L{tx+4} {y+h} L{x+12} {y+h} Q{x} {y+h} {x} {y+h-12}Z' fill='#fff' stroke='{INK}' stroke-width='3' stroke-linejoin='round'/>"
            f"<text x='{x+w/2}' y='{y+h/2+11}' text-anchor='middle' font-family='Inter' font-weight='700' font-size='32' fill='#d3382c'>{text}</text></g>")
def counter(x,y,w,h=100):
    return (f"<g class='chk'><rect x='{x}' y='{y}' width='{w}' height='{h}' rx='6' fill='#e9d3b0' stroke='{INK}' stroke-width='3'/>"
            f"<rect x='{x-8}' y='{y-12}' width='{w+16}' height='16' rx='5' fill='#c99a5b' stroke='{INK}' stroke-width='3'/>"
            + "".join(f"<rect x='{x+14+i*((w-28)/3)}' y='{y+22}' width='{(w-28)/3-10}' height='{h-40}' rx='4' fill='#f4e6cc' stroke='{INK}' stroke-width='2.5'/>" for i in range(3))+"</g>")
def awning(x,y,w):
    n=8; sw=w/n; out=""
    for i in range(n):
        out+=f"<path d='M{x+i*sw} {y} L{x+(i+1)*sw} {y} L{x+(i+1)*sw} {y+34} Q{x+(i+.5)*sw} {y+54} {x+i*sw} {y+34}Z' fill='{'#d4553a' if i%2==0 else '#ffffff'}' stroke='{INK}' stroke-width='3' stroke-linejoin='round'/>"
    return f"<g class='chk'>{out}</g>"
def sign(x,y,text,color="#1FA855",anim=""):
    return (f"<g class='chk' style='{anim}'><path d='M{x+30} {y-40} L{x+30} {y} M{x+110} {y-40} L{x+110} {y}' stroke='{INK}' stroke-width='3'/>"
            f"<rect x='{x}' y='{y}' width='140' height='54' rx='12' fill='{color}' stroke='{INK}' stroke-width='3'/>"
            f"<text x='{x+70}' y='{y+37}' text-anchor='middle' font-family='Inter' font-weight='800' font-size='30' fill='#fff'>{text}</text></g>")
def phone_prop(x,y,w,h,lines,spinner=False,anim=""):
    t="".join(f"<text x='{x+w/2}' y='{y+52+i*30}' text-anchor='middle' font-family='Inter' font-weight='700' font-size='22' fill='#111'>{l}</text>" for i,l in enumerate(lines))
    sp=icon_at('loader-circle',x+w/2-20,y+h-76,40,'#111',2.4,'animation:spin 1s linear infinite') if spinner else ""
    return (f"<g class='chk' style='{anim}'><rect x='{x}' y='{y}' width='{w}' height='{h}' rx='22' fill='#0b0b0c' stroke='{INK}' stroke-width='3'/><rect x='{x+8}' y='{y+8}' width='{w-16}' height='{h-16}' rx='15' fill='#fff3cd'/>{t}{sp}</g>")

# ---------- environment props (generic) ----------
def _t(x,y,s,fill,txt,w=700,anchor="middle",extra=""):
    return f"<text x='{x}' y='{y}' text-anchor='{anchor}' font-family='Inter' font-weight='{w}' font-size='{s}' fill='{fill}' {extra}>{txt}</text>"
def prop(o):
    k=o["name"]; x=o.get("x",0); y=o.get("y",0); d=o.get("d",0.3); w=o.get("w",100); h=o.get("h",100)
    pop=f"animation:pop .5s ease {d}s both;transform-box:fill-box;transform-origin:center"
    if k=="wall":
        return f"<g class='chk'><rect x='{x}' y='{y}' width='{w}' height='{h}' rx='18' fill='{o.get('color','#ffffff')}' fill-opacity='{o.get('op',.38)}'/></g>"
    if k=="board":   # departure board
        rows=o.get("rows",[]); hh=44+len(rows)*38
        out=f"<rect x='{x}' y='{y}' width='{w}' height='{hh}' rx='12' fill='#1d2438' stroke='{INK}' stroke-width='3'/>"+_t(x+16,y+30,20,'#9fb4ff',o.get('title','DEPARTURES'),800,'start')
        for i,(a,b) in enumerate(rows):
            yy=y+44+i*38
            out+=_t(x+16,yy+26,22,'#fff',a,700,'start')+f"<rect x='{x+w-170}' y='{yy+4}' width='156' height='28' rx='6' fill='#d3382c' style='animation:pulse2 1.2s ease-in-out {d+.6+i*.2}s infinite'/>"+_t(x+w-92,yy+25,18,'#fff',b,800)
        out=f"<path d='M{x+40} {y-34} V{y} M{x+w-40} {y-34} V{y}' stroke='{INK}' stroke-width='3'/>"+out
        return f"<g class='chk' style='{pop}'>{out}</g>"
    if k=="suitcase":
        c=o.get("color","#d4553a"); s=o.get("s",1)
        return (f"<g class='chk' style='{pop}'><g transform='translate({x} {y}) scale({s})'><path d='M18 0 h20 v-12 a4 4 0 0 0 -4 -4 h-12 a4 4 0 0 0 -4 4z' fill='none' stroke='{INK}' stroke-width='3'/>"
                f"<rect x='0' y='0' width='56' height='64' rx='8' fill='{c}' stroke='{INK}' stroke-width='3'/><path d='M14 8 v48 M42 8 v48' stroke='{INK}' stroke-opacity='.35' stroke-width='3'/>"
                f"<circle cx='12' cy='70' r='4' fill='{INK}'/><circle cx='44' cy='70' r='4' fill='{INK}'/></g></g>")
    if k=="window":
        pl=(f"<g style='animation:planeX 6s linear {d}s infinite'><path d='M{x+10} {y+h*0.3} l34 -6 l10 -8 l6 0 l-4 9 l16 2 l-2 5 l-16 1 l5 10 l-6 0 l-12 -9 l-30 0z' fill='#fff' stroke='{INK}' stroke-width='2.5' stroke-linejoin='round'/></g>") if o.get('plane') else ""
        return (f"<g class='chk'><rect x='{x}' y='{y}' width='{w}' height='{h}' rx='10' fill='#cfe9ff' stroke='{INK}' stroke-width='3'/><path d='M{x+w/2} {y} V{y+h} M{x} {y+h/2} H{x+w}' stroke='{INK}' stroke-width='3'/>{pl}</g>")
    if k=="desk":
        return (f"<g class='chk'><rect x='{x}' y='{y}' width='{w}' height='14' rx='5' fill='#c99a5b' stroke='{INK}' stroke-width='3'/>"
                f"<rect x='{x+10}' y='{y+14}' width='12' height='{h}' fill='#e9d3b0' stroke='{INK}' stroke-width='3'/><rect x='{x+w-22}' y='{y+14}' width='12' height='{h}' fill='#e9d3b0' stroke='{INK}' stroke-width='3'/>"
                f"<rect x='{x+22}' y='{y+14}' width='{w-44}' height='{h*0.55}' fill='#e9d3b0' stroke='{INK}' stroke-width='3'/></g>")
    if k=="monitor":
        err=o.get("err",False); body=icon_at('triangle-alert',x+w/2-18,y+14,36,'#d3382c',2.4,'animation:pulse2 1s ease-in-out infinite') if err else ""
        lines="".join(_t(x+w/2,y+h*0.62+i*20,16,'#333',l,700) for i,l in enumerate(o.get("lines",[])))
        return (f"<g class='chk' style='{pop}'><rect x='{x}' y='{y}' width='{w}' height='{h}' rx='8' fill='#fff' stroke='{INK}' stroke-width='3'/><rect x='{x+6}' y='{y+6}' width='{w-12}' height='{h-12}' rx='4' fill='{'#ffe9e7' if err else '#eef4ff'}'/>{body}{lines}"
                f"<rect x='{x+w/2-6}' y='{y+h}' width='12' height='14' fill='{INK}'/><rect x='{x+w/2-26}' y='{y+h+12}' width='52' height='8' rx='4' fill='{INK}'/></g>")
    if k=="laptop":
        rows=o.get("rows",3); cells="".join(f"<rect x='{x+14}' y='{y+14+i*20}' width='{w-28}' height='14' rx='4' fill='#d9f2d9' stroke='{INK}' stroke-width='1.5'/>"+icon_at('check',x+w-40,y+13+i*20,16,'#1c8a4c',3,f'animation:pop .4s ease {d+.8+i*.35}s both') for i in range(rows))
        return (f"<g class='chk' style='{pop}'><rect x='{x}' y='{y}' width='{w}' height='{h}' rx='8' fill='#fff' stroke='{INK}' stroke-width='3'/>{cells}<path d='M{x-14} {y+h+4} h{w+28} l-8 12 h{-w-12}z' fill='#ddd' stroke='{INK}' stroke-width='3' stroke-linejoin='round'/></g>")
    if k=="papers":
        return (f"<g class='chk'>"+"".join(f"<rect x='{x+i*4}' y='{y-i*7}' width='{w}' height='{h*0.35}' rx='3' fill='#fff' stroke='{INK}' stroke-width='2.5' transform='rotate({(-3,2,-1,4)[i%4]} {x+w/2} {y})'/>" for i in range(4))+"</g>")
    if k=="clock":
        r=w/2; cx=x+r; cy=y+r
        return (f"<g class='chk'><circle cx='{cx}' cy='{cy}' r='{r}' fill='#fff' stroke='{INK}' stroke-width='3'/>"
                f"<line x1='{cx}' y1='{cy}' x2='{cx}' y2='{cy-r*0.55}' stroke='{INK}' stroke-width='4' stroke-linecap='round' style='transform-box:view-box;transform-origin:{cx}px {cy}px;animation:spin 1.6s linear infinite'/>"
                f"<line x1='{cx}' y1='{cy}' x2='{cx+r*0.35}' y2='{cy}' stroke='{INK}' stroke-width='4' stroke-linecap='round'/><circle cx='{cx}' cy='{cy}' r='4' fill='{INK}'/></g>")
    if k=="ringphone":   # small ringing phone
        return (f"<g class='chk' style='{pop}'><g style='transform-box:fill-box;transform-origin:center;animation:shake .35s ease-in-out {d}s infinite'><rect x='{x}' y='{y}' width='34' height='58' rx='8' fill='#0b0b0c' stroke='{INK}' stroke-width='2.5'/><rect x='{x+4}' y='{y+6}' width='26' height='40' rx='4' fill='#fff3cd'/>"
                f"{icon_at('phone-call',x+5,y+14,24,'#d3382c',2.6)}</g></g>")
    if k=="note":   # sticky note
        return (f"<g class='chk' style='{pop}'><g transform='rotate({o.get('rot',-4)} {x+w/2} {y+h/2})'><rect x='{x}' y='{y}' width='{w}' height='{h}' fill='{o.get('color','#ffe27a')}' stroke='{INK}' stroke-width='2.5'/>{_t(x+w/2,y+h/2+7,18,INK,o.get('text',''),800)}</g></g>")
    if k=="bench":
        return (f"<g class='chk'><rect x='{x}' y='{y}' width='{w}' height='{h}' rx='10' fill='#7aa2d6' stroke='{INK}' stroke-width='3'/><rect x='{x+10}' y='{y+h}' width='12' height='{o.get('legs',46)}' fill='{INK}'/><rect x='{x+w-22}' y='{y+h}' width='12' height='{o.get('legs',46)}' fill='{INK}'/></g>")
    if k=="plant":
        return (f"<g class='chk'><path d='M{x+20} {y} q-18 -30 -4 -52 q14 18 4 52z M{x+20} {y} q14 -34 34 -40 q-2 24 -34 40z M{x+20} {y} q-30 -14 -36 -38 q26 4 36 38z' fill='#4fa86a' stroke='{INK}' stroke-width='2.5' stroke-linejoin='round'/><path d='M{x} {y} h40 l-6 40 h-28z' fill='#d4553a' stroke='{INK}' stroke-width='3' stroke-linejoin='round'/></g>")
    if k=="mug":
        return (f"<g class='chk'><rect x='{x}' y='{y}' width='30' height='32' rx='6' fill='#fff' stroke='{INK}' stroke-width='3'/><path d='M{x+30} {y+8} q14 0 14 10 q0 10 -14 10' fill='none' stroke='{INK}' stroke-width='3'/>"
                f"<path d='M{x+10} {y-6} q-6 -10 0 -18 M{x+20} {y-6} q-6 -10 0 -18' fill='none' stroke='{INK}' stroke-opacity='.45' stroke-width='3' stroke-linecap='round' style='animation:floaty 2s ease-out infinite'/></g>")
    if k=="paper_float":
        return f"<g class='chk'><g style='animation:floaty 2.2s ease-out {d}s infinite;transform-box:fill-box;transform-origin:center'><rect x='{x}' y='{y}' width='30' height='38' rx='3' fill='#fff' stroke='{INK}' stroke-width='2.5' transform='rotate({o.get('rot',12)} {x+15} {y+19})'/></g></g>"
    return ""

def _bag(x,y,s,c):
    return (f"<g transform='translate({x} {y}) scale({s})'><path d='M18 0 h20 v-10 a4 4 0 0 0 -4 -4 h-12 a4 4 0 0 0 -4 4z' fill='none' stroke='{INK}' stroke-width='3.5'/>"
            f"<rect x='0' y='0' width='56' height='64' rx='8' fill='{c}' stroke='{INK}' stroke-width='3.5'/><path d='M14 8 v48 M42 8 v48' stroke='{INK}' stroke-opacity='.3' stroke-width='3'/></g>")
BAGC=["#d4553a","#4f7fd6","#e8b93d","#4fa86a","#8b6fd6","#e07aa0","#3b4a6b","#f08a4b"]
_old_prop=prop
def prop(o):
    k=o.get("name")
    x=o.get("x",0); y=o.get("y",0); d=o.get("d",0.3); w=o.get("w",100)
    if k=="bagpile":   # pyramid of suitcases, base at y (bottom edge), width w
        out=""; n=o.get("n",4); s=o.get("s",0.8); bw=56*s; idx=0
        for r in range(n):
            cnt=n-r; rowx=x+(w-cnt*(bw+4))/2
            for i in range(cnt):
                out+=_bag(rowx+i*(bw+4), y-(r+1)*(64*s+2), s, BAGC[(idx*3+r)%len(BAGC)]); idx+=1
        return f"<g class='chk' style='animation:pop .5s ease {d}s both;transform-box:fill-box;transform-origin:center bottom'>{out}</g>"
    if k=="carousel":
        out=(f"<rect x='{x}' y='{y}' width='{w}' height='34' rx='17' fill='#59607a' stroke='{INK}' stroke-width='3'/>"
             f"<rect x='{x+8}' y='{y+6}' width='{w-16}' height='22' rx='11' fill='#2c3248'/>"
             +"".join(f"<rect x='{x+24+i*46}' y='{y+9}' width='20' height='16' rx='3' fill='#444b66'/>" for i in range((w-48)//46))
             +_bag(x+w*0.2,y-30,0.5,"#e8b93d")+_bag(x+w*0.55,y-30,0.5,"#4f7fd6"))
        return f"<g class='chk'>{out}</g>"
    return _old_prop(o)

# ---- props added for the Eras Tour reel ----
_prev_prop2=prop
def prop(o):
    k=o.get("name"); x=o.get("x",0); y=o.get("y",0); d=o.get("d",0.3); w=o.get("w",100); h=o.get("h",100)
    pop=f"animation:pop .5s ease {d}s both;transform-box:fill-box;transform-origin:center"
    if k=="sofa":
        c=o.get("color","#8b6fd6")
        return (f"<g class='chk'><rect x='{x}' y='{y}' width='{w}' height='{h}' rx='18' fill='{c}' stroke='{INK}' stroke-width='3'/>"
                f"<rect x='{x-14}' y='{y+h*0.35}' width='26' height='{h*0.65}' rx='12' fill='{c}' stroke='{INK}' stroke-width='3'/>"
                f"<rect x='{x+w-12}' y='{y+h*0.35}' width='26' height='{h*0.65}' rx='12' fill='{c}' stroke='{INK}' stroke-width='3'/>"
                f"<rect x='{x+10}' y='{y+h*0.5}' width='{w-20}' height='{h*0.5}' rx='10' fill='{c}' fill-opacity='.7' stroke='{INK}' stroke-width='3'/>"
                f"<rect x='{x+16}' y='{y+h}' width='10' height='14' fill='{INK}'/><rect x='{x+w-26}' y='{y+h}' width='10' height='14' fill='{INK}'/></g>")
    if k=="ticket":
        return (f"<g class='chk' style='{pop}'><g transform='rotate({o.get('rot',-8)} {x+w/2} {y+h/2})'><rect x='{x}' y='{y}' width='{w}' height='{h}' rx='8' fill='#ffe27a' stroke='{INK}' stroke-width='3'/>"
                f"<circle cx='{x}' cy='{y+h/2}' r='9' fill='{o.get('bg','#cfe9ff')}' stroke='{INK}' stroke-width='3'/><circle cx='{x+w}' cy='{y+h/2}' r='9' fill='{o.get('bg','#cfe9ff')}' stroke='{INK}' stroke-width='3'/>"
                f"<path d='M{x+w*0.68} {y+8} V{y+h-8}' stroke='{INK}' stroke-width='2.5' stroke-dasharray='5 5'/>"
                +_t(x+w*0.34,y+h/2+8,o.get('size',22),INK,o.get('text','ADMIT ONE'),800)+"</g></g>")
    if k=="rope":   # queue stanchions with rope
        n=o.get("n",3); gap=w/(n-1) if n>1 else w; out=""
        for i in range(n):
            px=x+i*gap
            out+=f"<rect x='{px-4}' y='{y}' width='8' height='{h}' fill='{INK}'/><circle cx='{px}' cy='{y}' r='9' fill='#e8b93d' stroke='{INK}' stroke-width='3'/><rect x='{px-14}' y='{y+h}' width='28' height='7' rx='3' fill='{INK}'/>"
        out+=f"<path d='M{x} {y+6} Q{x+w/2} {y+34} {x+w} {y+6}' fill='none' stroke='#d3382c' stroke-width='6'/>"
        return f"<g class='chk'>{out}</g>"
    return _prev_prop2(o)

# ---- props added for the Prime Day reel ----
_prev_prop3=prop
def prop(o):
    k=o.get("name"); x=o.get("x",0); y=o.get("y",0); d=o.get("d",0.3); w=o.get("w",100); h=o.get("h",70)
    if k=="parcel":   # cardboard parcel with tape and label
        pp=f"animation:pop .5s ease {d}s both;transform-box:fill-box;transform-origin:center bottom"
        return (f"<g class='chk' style='{pp}'><rect x='{x}' y='{y}' width='{w}' height='{h}' rx='4' fill='#d9b27c' stroke='{INK}' stroke-width='3'/>"
                f"<rect x='{x+w/2-8}' y='{y}' width='16' height='{h}' fill='#c99a5b' stroke='{INK}' stroke-width='2'/>"
                f"<rect x='{x+w*0.1}' y='{y+h*0.5}' width='{w*0.22}' height='{h*0.28}' rx='2' fill='#fff' stroke='{INK}' stroke-width='2'/></g>")
    return _prev_prop3(o)
