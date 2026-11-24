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


def render(sc, dur, tl):
    pre = ("<div style='position:absolute;inset:0;background:radial-gradient(circle at 50% 36%,#fbfbfb 0,#ececee 58%,#d9d9dc 100%)'></div>" + CSS)
    els = "".join(_el(e) for e in sc["els"])
    top = sc.get("top", 90)
    body = (f"<div style='position:relative;margin-top:{top}px;display:flex;flex-direction:column;gap:{sc.get('gap', 26)}px;align-items:stretch;width:487px'>{els}</div>"
            + _cap(sc, tl))
    return pre, body
