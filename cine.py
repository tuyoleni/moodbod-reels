"""Cinematic scene engine: full-bleed layered sets (720x1280), parallax drift, camera moves, silhouette reveals, FX.
Used by make_reel.py for scene type "cinema". All art is generated SVG (no photos, no real likenesses)."""
import random, math
import chars as C
from icons import icon_at

W, H = 720, 1280
SKY = {
 "dusk":  [("0","#10123a"),("45","#4b2a70"),("80","#ff7a5c"),("100","#ffbd75")],
 "night": [("0","#05071c"),("60","#161b46"),("100","#2b2a66")],
 "alert": [("0","#12040a"),("55","#4a0d16"),("100","#a3202b")],
 "day":   [("0","#7fc4ff"),("100","#e9f6ff")],
 "warm":  [("0","#1d1530"),("100","#4a2b49")],
}

def _sky(kind, h=H):
    st = "".join(f"<stop offset='{o}%' stop-color='{c}'/>" for o, c in SKY[kind])
    return f"<linearGradient id='sky' x1='0' y1='0' x2='0' y2='1'>{st}</linearGradient>"

def skyline(seed, base, hmin, hmax, col, lit="#ffd27a", dens=.35, x0=-120, x1=860, wmin=34, wmax=86, flick=6):
    r = random.Random(seed); x = x0; out = []; fl = 0
    while x < x1:
        w = r.randint(wmin, wmax); h = r.randint(hmin, hmax)
        out.append(f"<rect x='{x}' y='{base-h}' width='{w}' height='{h+400}' fill='{col}'/>")
        if r.random() < .25:  # antenna
            out.append(f"<rect x='{x+w//2-1}' y='{base-h-r.randint(14,40)}' width='2' height='40' fill='{col}'/>")
        for wy in range(base - h + 12, base - 6, 15):
            for wx in range(x + 7, x + w - 8, 12):
                if r.random() < dens:
                    a = r.choice((.95, .75, .55))
                    anim = ""
                    if fl < flick and r.random() < .06:
                        fl += 1; anim = f" style='animation:pulse2 {r.uniform(1.2,2.6):.1f}s ease-in-out infinite'"
                    out.append(f"<rect x='{wx}' y='{wy}' width='6' height='9' fill='{lit}' opacity='{a}'{anim}/>")
        x += w + r.randint(0, 6)
    return "".join(out)

def drift(k, inner, dur, dx):
    return f"<g style='animation:dr{k} {dur:.2f}s linear both'>{inner}</g><style>@keyframes dr{k}{{from{{transform:translateX(0)}}to{{transform:translateX({dx}px)}}}}</style>"

def stars(n=46, seed=3):
    r = random.Random(seed)
    return "".join(f"<circle cx='{r.randint(0,W)}' cy='{r.randint(0,520)}' r='{r.choice((.8,1.1,1.5))}' fill='#fff' opacity='{r.uniform(.4,.95):.2f}' style='animation:pulse2 {r.uniform(1.5,3.5):.1f}s ease-in-out infinite'/>" for _ in range(n))

def bokeh(n=14, seed=9, cols=("#ffb36b", "#ff7a8c", "#7ad7ff")):
    r = random.Random(seed)
    return "".join(f"<circle cx='{r.randint(0,W)}' cy='{r.randint(700,1250)}' r='{r.randint(14,42)}' fill='{r.choice(cols)}' opacity='{r.uniform(.07,.2):.2f}'/>" for _ in range(n))

# ---------------------------------------------------------------- sets
def set_city(sc, dur):
    sky = sc.get("sky", "dusk")
    g = f"<rect width='{W}' height='{H}' fill='url(#sky)'/>"
    if sky in ("dusk", "night", "alert"): g += stars(40 if sky != "alert" else 14)
    g += "<circle cx='540' cy='300' r='150' fill='url(#moonglow)'/><circle cx='540' cy='300' r='44' fill='#fff6df'/><circle cx='554' cy='290' r='40' fill='url(#sky)' opacity='0'/>" if sc.get("moon", True) else ""
    g += drift(1, skyline(11, 820, 120, 330, "#2b2257" if sky != "alert" else "#3a0f1d", dens=.18, wmin=44, wmax=90, flick=2), dur, -10)
    g += drift(2, skyline(23, 960, 150, 420, "#171238" if sky != "alert" else "#240a14", dens=.3, flick=5), dur, -26)
    # hero tower (lit office floor) centre-right
    tx = sc.get("tower_x", 250)
    tower = (f"<rect x='{tx}' y='330' width='230' height='900' fill='#0b0a22'/><rect x='{tx+6}' y='330' width='218' height='6' fill='#ff6a5a' opacity='.9' style='animation:pulse2 1.1s ease-in-out infinite'/>")
    for fy in range(360, 1180, 38):
        for fx in range(tx + 14, tx + 214, 26):
            lit = (fy * 7 + fx * 3) % 5 != 0
            tower += f"<rect x='{fx}' y='{fy}' width='16' height='22' fill='{'#ffdc8a' if lit else '#1c1a45'}' opacity='{.9 if lit else 1}'/>"
    # the "one lit window" the camera pushes into
    wx, wy = tx + 92, 548
    tower += (f"<rect x='{wx-6}' y='{wy-6}' width='44' height='46' fill='#ffcf6b' opacity='.22' style='animation:pulse2 1.6s ease-in-out infinite'/><rect x='{wx}' y='{wy}' width='32' height='34' fill='#fff1b8'/>"
              f"<path d='M{wx+10} {wy+34} v-14 q6 -10 12 0 v14z' fill='#0b0a22'/>")
    g += drift(3, tower, dur, -44)
    g += drift(4, skyline(37, 1180, 170, 470, "#0a081f", dens=.22, wmin=50, wmax=110, flick=4), dur, -70)
    g += f"<rect y='1120' width='{W}' height='160' fill='#05040f'/><rect y='1120' width='{W}' height='4' fill='#ff7a5c' opacity='.5'/>" + bokeh()
    return g

def set_boardroom(sc, dur):
    g = f"<rect width='{W}' height='{H}' fill='#0c1a22'/>"
    # window with city
    g += "<clipPath id='win'><rect x='20' y='130' width='390' height='520'/></clipPath><g clip-path='url(#win)'>"
    g += f"<rect x='20' y='130' width='390' height='520' fill='url(#sky)'/>"
    g += drift(1, skyline(5, 560, 90, 230, "#2b2257", dens=.25, x0=-60, x1=480, flick=2), dur, -12)
    g += drift(2, skyline(8, 650, 120, 330, "#151034", dens=.35, x0=-60, x1=480, flick=3), dur, -30) + "</g>"
    g += "<g stroke='#06141b' stroke-width='10' fill='none'><rect x='20' y='130' width='390' height='520'/><path d='M150 130 V650 M280 130 V650 M20 390 H410'/></g>"
    # screen with falling chart
    sx, sy, sw, sh = 440, 210, 250, 300
    g += f"<rect x='{sx-8}' y='{sy-8}' width='{sw+16}' height='{sh+16}' rx='10' fill='#05090d' stroke='#25404d' stroke-width='3'/><rect x='{sx}' y='{sy}' width='{sw}' height='{sh}' fill='#0e1c26'/>"
    for i in range(1, 5): g += f"<path d='M{sx} {sy+i*60} H{sx+sw}' stroke='#27404d' stroke-width='1.5'/>"
    pts = [(0,.18),(.15,.2),(.3,.15),(.45,.34),(.6,.5),(.75,.62),(.9,.84),(1,.92)]
    d = "M" + " L".join(f"{sx+12+(sw-24)*a:.0f} {sy+sh*b:.0f}" for a, b in pts)
    g += f"<path d='{d}' fill='none' stroke='#ff5c6b' stroke-width='6' stroke-linecap='round' stroke-linejoin='round' pathLength='1' stroke-dasharray='1' style='animation:draw 2.2s ease-out .5s both'/>"
    g += f"<text x='{sx+16}' y='{sy+34}' font-size='24' font-weight='800' fill='#ff8a95' font-family='Inter,sans-serif'>{sc.get('screen','▼ 50%')}</text>"
    # pendant lamps
    for lx in (120, 360, 600):
        g += f"<path d='M{lx} 0 V90' stroke='#05090d' stroke-width='3'/><path d='M{lx-34} 118 Q{lx} 70 {lx+34} 118Z' fill='#1b2a33'/><path d='M{lx-30} 120 L{lx-150} 520 L{lx+150} 520 L{lx+30} 120Z' fill='url(#beam)' opacity='.55'/>"
    # long table front (drawn later over characters via 'front')
    return g

def front_boardroom(sc):
    return (f"<path d='M-20 830 L740 830 L760 1280 L-40 1280Z' fill='#1a2430'/><path d='M-20 830 L740 830' stroke='#7fa6bb' stroke-width='4' opacity='.8'/>"
            f"<path d='M-20 840 L740 840 L742 880 L-22 880Z' fill='#fff' opacity='.05'/>"
            f"<rect x='80' y='760' width='86' height='60' rx='6' fill='#10161d' stroke='#2c3a47' stroke-width='3'/><rect x='88' y='766' width='70' height='46' fill='#1d3b52'/>"
            f"<rect x='520' y='772' width='34' height='50' rx='7' fill='#0d1318' stroke='#2c3a47' stroke-width='2'/>")

def set_hall(sc, dur):
    g = f"<rect width='{W}' height='{H}' fill='#06060d'/>"
    # corridor perspective
    g += "<path d='M0 0 L250 330 L470 330 L720 0Z' fill='#0d0d1a'/><path d='M0 1280 L250 900 L470 900 L720 1280Z' fill='#101022'/><path d='M0 0 L250 330 L250 900 L0 1280Z' fill='#0a0a14'/><path d='M720 0 L470 330 L470 900 L720 1280Z' fill='#0a0a14'/>"
    for i in range(1, 7):
        t = i / 7; y = 330 - 330 * t * .0
    # floor lines
    for i in range(-4, 5):
        g += f"<path d='M{360+i*28} 900 L{360+i*190} 1280' stroke='#2a2a55' stroke-width='2' opacity='.5'/>"
    # door light
    g += "<rect x='250' y='330' width='220' height='570' fill='url(#door)'/><rect x='250' y='330' width='220' height='570' fill='none' stroke='#fff3d0' stroke-width='4' opacity='.9'/>"
    g += "<path d='M310 900 L120 1280 L600 1280 L410 900Z' fill='#ffe9b0' opacity='.18' style='animation:pulse2 2.4s ease-in-out infinite'/>"
    g += "<path d='M300 330 L-100 -120 L120 -200 L420 330Z' fill='#fff3d0' opacity='.10'/><path d='M420 330 L820 -120 L600 -200 L300 330Z' fill='#fff3d0' opacity='.10'/>"
    # drifting dust
    r = random.Random(4)
    g += "".join(f"<circle cx='{r.randint(100,620)}' cy='{r.randint(300,1000)}' r='{r.choice((1.5,2,3))}' fill='#fff1c9' opacity='{r.uniform(.2,.6):.2f}' style='animation:bob {r.uniform(1.4,2.8):.1f}s ease-in-out infinite'/>" for _ in range(40))
    return g

def set_office(sc, dur):
    g = f"<rect width='{W}' height='{H}' fill='url(#sky)'/>"
    g += "<clipPath id='win'><rect x='360' y='170' width='320' height='420'/></clipPath><g clip-path='url(#win)'><rect x='360' y='170' width='320' height='420' fill='#1b1f4f'/>"
    g += skyline(7, 590, 80, 240, "#241d57", dens=.3, x0=340, x1=700, flick=3) + skyline(9, 640, 120, 300, "#120e33", dens=.35, x0=340, x1=700, flick=3) + "</g>"
    g += "<g stroke='#120c1f' stroke-width='9' fill='none'><rect x='360' y='170' width='320' height='420'/><path d='M520 170 V590 M360 380 H680'/></g>"
    g += f"<ellipse cx='150' cy='520' rx='240' ry='300' fill='url(#lamp)'/>"
    g += "<rect x='40' y='300' width='8' height='260' fill='#0d0a16'/><path d='M0 300 Q44 240 90 300Z' fill='#f6c36b'/>"
    return g

def front_office(sc):
    return (f"<rect x='-20' y='930' width='760' height='360' fill='#171021'/><rect x='-20' y='926' width='760' height='10' fill='#3b2d52'/>"
            f"<path d='M150 940 L560 940 L590 1010 L120 1010Z' fill='#cfd3e6'/><rect x='170' y='700' width='360' height='240' rx='10' fill='#0f1220' stroke='#cfd3e6' stroke-width='6'/>"
            f"<rect x='182' y='712' width='336' height='216' fill='#1c2a4a'/>"
            + "".join(f"<rect x='200' y='{730+i*34}' width='{[220,170,250,140,200][i]}' height='10' rx='5' fill='#7fb0ff' opacity='.55'/>" for i in range(5)))

SETS = {"city": (set_city, None), "boardroom": (set_boardroom, front_boardroom), "hall": (set_hall, None), "office": (set_office, front_office)}

# ---------------------------------------------------------------- fx
def fx_speed(cx, cy, delay=0, col="#fff", n=44, r0=170, r1=700, seed=2):
    r = random.Random(seed); L = ""
    for i in range(n):
        a = 2 * math.pi * i / n + r.uniform(-.03, .03); a0 = r.uniform(r0, r0 + 120); a1 = r.uniform(r1 * .7, r1)
        L += f"<path d='M{cx+math.cos(a)*a0:.0f} {cy+math.sin(a)*a0:.0f} L{cx+math.cos(a)*a1:.0f} {cy+math.sin(a)*a1:.0f}' stroke='{col}' stroke-width='{r.choice((2,3,4,6))}' stroke-linecap='round'/>"
    return f"<g opacity='0' style='transform-origin:{cx}px {cy}px;transform-box:view-box;animation:spd .5s steps(2) {delay}s 3 both, spdjit .12s steps(2) {delay}s infinite'>{L}</g>"

def fx_rain(n=70, seed=1, col="#cfe4ff"):
    r = random.Random(seed); L = ""
    for _ in range(n):
        x = r.randint(-60, W + 60); y = r.randint(-80, H); ln = r.randint(34, 70)
        L += f"<path d='M{x} {y} l-8 {ln}' stroke='{col}' stroke-width='{r.choice((1.2,1.8,2.4))}' opacity='{r.uniform(.2,.5):.2f}' style='animation:rain {r.uniform(.45,.8):.2f}s linear -{r.uniform(0,.8):.2f}s infinite'/>"
    return L

def fx_papers(n=16, seed=5):
    r = random.Random(seed); L = ""
    for _ in range(n):
        x = r.randint(40, 680); d = r.uniform(0, 1.6); sp = r.uniform(2.2, 3.6)
        L += f"<g style='transform:translate({x}px,-60px)'><rect width='34' height='44' rx='3' fill='#fff' opacity='.9' style='transform-box:fill-box;transform-origin:center;animation:paperfall {sp:.1f}s ease-in {d:.1f}s infinite'/></g>"
    return L

def fx_embers(n=26, seed=6, col="#ffb36b"):
    r = random.Random(seed)
    return "".join(f"<circle cx='{r.randint(0,W)}' cy='{r.randint(900,1300)}' r='{r.choice((2,3,4))}' fill='{col}' style='animation:ember {r.uniform(2,4):.1f}s ease-out -{r.uniform(0,3):.1f}s infinite'/>" for _ in range(n))

def fx_alert(): return f"<rect width='{W}' height='{H}' fill='#ff2a3d' opacity='0' style='animation:alertp 1s ease-in-out infinite'/>"

def fx_cards(cards, cx, cy):
    out = ""
    pos = [(-185,-215,-7),(150,-250,6),(-205,-20,5),(185,-30,-6),(0,-340,-3)]
    for i, (ic, label) in enumerate(cards):
        dx, dy, rot = pos[i % len(pos)]; x = cx + dx - 70; y = cy + dy
        out += (f"<g style='transform-origin:{x+70}px {y}px;transform-box:view-box;animation:fu .5s ease {.4+i*.25}s both'><g style='transform-origin:{x+70}px {y}px;transform-box:view-box;animation:wob {2.2+i*.3:.1f}s ease-in-out infinite'>"
                f"<path d='M{x+70} {y} L{x+70} -60' stroke='#8d86b8' stroke-width='2' opacity='.6'/>"
                f"<g transform='rotate({rot} {x+70} {y})'><rect x='{x}' y='{y}' width='140' height='84' rx='16' fill='#ffffff' opacity='.94' stroke='#1c2033' stroke-width='3'/>"
                f"{icon_at(ic, x+14, y+16, 30, '#1c2033', 2.4)}<text x='{x+52}' y='{y+40}' font-size='22' font-weight='800' fill='#1c2033' font-family='Inter,sans-serif'>{label}</text>"
                f"<rect x='{x+14}' y='{y+58}' width='84' height='8' rx='4' fill='#d7d9e8'/>{icon_at('lock', x+108, y+52, 22, '#e5322d', 2.6)}</g></g></g>")
    return out

# ---------------------------------------------------------------- cast
def cast_svg(cast, dur):
    out = ""
    for i, c in enumerate(cast):
        s = c.get("s", 1.9); x = c["x"]; y = c["y"]; d = c.get("d", .3)
        inner = C.person(c.get("skin", "a"), c.get("shirt", "suit"), c.get("pose", "stand"), c.get("expr", "calm"), None, False, c.get("hair", "short"), False, c.get("dress"), c.get("anim"), c.get("expr2"), c.get("expr2_at", 0), c.get("sweat", False), c.get("hairc"))
        if c.get("tie"): inner += f"<path d='M50 56 L45 64 L50 100 L55 64Z' fill='{c['tie']}' stroke='{C.INK}' stroke-width='2'/><path d='M43 55 L50 66 L57 55' fill='#fff' stroke='{C.INK}' stroke-width='2'/>"
        if c.get("sil"):  # backlit silhouette -> reveal to colour
            r = c["reveal"]
            pct=int(100*r/(r+.4))
            inner = (f"<style>@keyframes sil{i}{{0%,{pct}%{{filter:brightness(0)}}100%{{filter:brightness(1)}}}}</style><g style='animation:sil{i} {r+.4:.2f}s linear both'>{inner}</g>")
        glow = c.get("glow", "#000")
        ent = {"fade": f"animation:fu .6s ease {d}s both", "pop": f"animation:pop .5s ease {d}s both", "walk": f"animation:walk {c.get('walk',2.6)}s cubic-bezier(.3,.1,.3,1) {d}s both"}[c.get("enter", "fade")]
        shake = f"<g style='transform-box:fill-box;transform-origin:center bottom;animation:jolt .5s linear {c['jolt']}s both'>{inner}</g>" if c.get("jolt") else inner
        body = f"<g style='animation:bob 1.7s ease-in-out {d+.5}s infinite;filter:drop-shadow(0 0 22px {glow})'>{shake}</g>"
        out += C.actor(x, y, s, ent + ";transform-box:fill-box", body, c.get("flip", False), chk=False)
    return out

KEY = """
@keyframes spd{0%{opacity:0}30%{opacity:.85}100%{opacity:0}}
@keyframes spdjit{from{transform:rotate(0)}to{transform:rotate(2.5deg)}}
@keyframes rain{from{transform:translate(0,-120px)}to{transform:translate(-30px,1300px)}}
@keyframes paperfall{0%{transform:translateY(0) rotate(0);opacity:0}15%{opacity:.9}100%{transform:translateY(1450px) rotate(420deg);opacity:.9}}
@keyframes ember{0%{transform:translateY(0);opacity:0}20%{opacity:.9}100%{transform:translateY(-520px) translateX(30px);opacity:0}}
@keyframes alertp{0%,100%{opacity:0}50%{opacity:.22}}
@keyframes sil{0%{filter:brightness(0)}78%{filter:brightness(0)}100%{filter:brightness(1)}}
@keyframes walk{from{opacity:0;transform:translateY(-90px) scale(.55)}to{opacity:1;transform:none}}
@keyframes hand{from{transform:translate(2px,-3px) rotate(.22deg)}to{transform:translate(-3px,2px) rotate(-.22deg)}}
@keyframes punch{0%{transform:scale(1)}30%{transform:scale(1.07)}100%{transform:scale(1)}}
@keyframes bar{from{transform:translateY(var(--o))}to{transform:none}}
"""

def render(sc, dur):
    setname = sc.get("set", "city"); bgf, frontf = SETS[setname]
    cam = sc.get("cam", {}); f = cam.get("from", [1, 0, 0]); t = cam.get("to", [1.12, 0, 0]); o = cam.get("o", [360, 640])
    camcss = (f"@keyframes cam{{from{{transform:translate({f[1]}px,{f[2]}px) scale({f[0]})}}to{{transform:translate({t[1]}px,{t[2]}px) scale({t[0]})}}}}")
    defs = (f"<defs>{_sky(sc.get('sky','dusk'))}"
            "<radialGradient id='moonglow'><stop offset='0' stop-color='#fff1c9' stop-opacity='.55'/><stop offset='1' stop-color='#fff1c9' stop-opacity='0'/></radialGradient>"
            "<linearGradient id='beam' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#ffe9b0' stop-opacity='.45'/><stop offset='1' stop-color='#ffe9b0' stop-opacity='0'/></linearGradient>"
            "<linearGradient id='door' x1='0' y1='0' x2='0' y2='1'><stop offset='0' stop-color='#fff8e0'/><stop offset='1' stop-color='#ffd78a'/></linearGradient>"
            "<radialGradient id='lamp'><stop offset='0' stop-color='#ffb36b' stop-opacity='.55'/><stop offset='1' stop-color='#ffb36b' stop-opacity='0'/></radialGradient></defs>")
    bg = bgf(sc, dur)
    cast = cast_svg(sc.get("cast", []), dur)
    front = frontf(sc) if frontf else ""
    fx = ""
    for e in sc.get("fx", []):
        k = e["k"]; d = e.get("d", 0)
        if k == "speed": fx += fx_speed(e.get("x", 360), e.get("y", 700), d, e.get("col", "#fff"))
        elif k == "rain": fx += fx_rain()
        elif k == "papers": fx += fx_papers()
        elif k == "embers": fx += fx_embers(col=e.get("col", "#ffb36b"))
        elif k == "alert": fx += fx_alert()
        elif k == "cards": fx += fx_cards(e["cards"], e.get("x", 360), e.get("y", 700))
        elif k == "text":  # comic SFX word in-world
            fx += (f"<text x='{e['x']}' y='{e['y']}' text-anchor='middle' font-family='Impact,Anton,sans-serif' font-size='{e.get('size',120)}' fill='{e.get('col','#fff')}' stroke='#111' stroke-width='9' paint-order='stroke' stroke-linejoin='round' "
                   f"style='transform-box:fill-box;transform-origin:center;transform:rotate({e.get('rot',-8)}deg);animation:pop .35s ease {d}s both'>{e['text']}</text>")
        elif k == "flash": fx += f"<rect width='{W}' height='{H}' fill='{e.get('col','#fff')}' opacity='0' style='animation:flash .6s ease-out {d}s both'/>"
    punch = sc.get("punch")
    world = f"{bg}{cast}{front}{fx}"
    world = f"<g style='transform-box:view-box;transform-origin:360px 640px;animation:hand 2.6s ease-in-out infinite alternate'>{world}</g>"
    world = f"<g style='transform-box:view-box;transform-origin:{o[0]}px {o[1]}px;animation:cam {dur:.2f}s cubic-bezier(.35,.05,.25,1) both'>{world}</g>"
    if punch: world = f"<g style='transform-box:view-box;transform-origin:360px 640px;animation:punch .35s ease-out {punch}s both'>{world}</g>"
    bars = ("<rect width='720' height='104' fill='#000' style='--o:-104px;animation:bar .7s ease-out both'/><rect y='1176' width='720' height='104' fill='#000' style='--o:104px;animation:bar .7s ease-out both'/>") if sc.get("bars", True) else ""
    return (f"<style>{KEY}{camcss}</style><svg width='720' height='1280' viewBox='0 0 720 1280' style='position:absolute;left:0;top:0'>{defs}{world}{bars}</svg>")
