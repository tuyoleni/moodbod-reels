import os,re
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),"icons_pkg","node_modules","lucide-static","icons")
def _inner(n): return re.search(r"<svg[^>]*>(.*)</svg>",open(os.path.join(D,n+".svg")).read(),re.S).group(1)
def icon(n,size=20,color="currentColor",sw=2,style=""):
    return f"<svg xmlns='http://www.w3.org/2000/svg' width='{size}' height='{size}' viewBox='0 0 24 24' fill='none' stroke='{color}' stroke-width='{sw}' stroke-linecap='round' stroke-linejoin='round' style='flex:none;{style}'>{_inner(n)}</svg>"
def icon_at(n,x,y,size=24,color="#111",sw=2,style=""):
    return f"<g style='transform-box:fill-box;transform-origin:center;{style}'><svg x='{x}' y='{y}' width='{size}' height='{size}' viewBox='0 0 24 24' fill='none' stroke='{color}' stroke-width='{sw}' stroke-linecap='round' stroke-linejoin='round'>{_inner(n)}</svg></g>"
