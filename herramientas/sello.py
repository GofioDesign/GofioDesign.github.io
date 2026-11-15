"""Sello «Un proyecto Gofio Design» para insertar desde otras webs (claro y oscuro).
Todo el texto va en trazos: una imagen SVG no carga fuentes externas."""
import io, os, re, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import parse_path

repo, S = sys.argv[1], sys.argv[2]
f = lambda v: ("%.2f" % v).rstrip("0").rstrip(".")
LOGO = io.open(os.path.join(S, "logo-prop.txt"), encoding="utf-8").read().strip()
src = io.open(os.path.join(repo, "assets", "marca", "titulo-crema.svg"), encoding="utf-8").read()
TITLE_D = re.findall(r'<path d="([^"]+)"', src)[0]

# Bounding box real del título (en su caja 682x120, desplazado translate(20 96))
bp = BoundsPen(None); parse_path(TITLE_D, bp)
tx0, ty0, tx1, ty1 = bp.bounds
tx0 += 20; tx1 += 20; ty0 += 96; ty1 += 96

# «UN PROYECTO» en Nunito 800, en trazos
font = instantiateVariableFont(TTFont(os.path.join(repo, "assets", "fonts", "nunito-latin.woff2")), {"wght": 800})
gs, cmap, upm = font.getGlyphSet(), font.getBestCmap(), font["head"].unitsPerEm
cap = font["OS/2"].sCapHeight


def text_path(txt, size, x, baseline, tracking):
    pen = SVGPathPen(gs, ntos=f)
    k = size / upm
    for ch in txt:
        g = cmap[ord(ch)]
        t = TransformPen(pen, (k, 0, 0, -k, x, baseline))
        gs[g].draw(t)
        x += gs[g].width * k + tracking
    return pen.getCommands(), x - tracking


H = 64                       # alto del sello
PAD = 10                     # margen interior
LOGO_S = H - 2 * PAD         # pintadera de 44
TX = PAD + LOGO_S + 12       # inicio del texto
# título: altura de mayúscula 20 px
title_cap = 20.0
ks = title_cap / (ty1 - ty0)
title_w = (tx1 - tx0) * ks
small_size = 9.5
small_cap = cap * small_size / upm
gap = 6.5
block = small_cap + gap + title_cap
top = (H - block) / 2
small_d, small_end = text_path("UN PROYECTO", small_size, TX, top + small_cap, 1.9)
title_y = top + small_cap + gap
W = round(TX + max(title_w, small_end - TX) + PAD + 6)

title = ('<g transform="translate(%s %s) scale(%s) translate(%s %s)"><path d="%s"/></g>'
         % (f(TX), f(title_y), ("%.5f" % ks), f(-tx0 + 20), f(-ty0 + 96), TITLE_D))


def sello(bg, ink, line):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="Un proyecto Gofio Design">'
            '<title>Un proyecto Gofio Design</title>'
            '<rect x="1" y="1" width="%d" height="%d" rx="%s" fill="%s" stroke="%s" stroke-width="2"/>'
            '<g color="%s" fill="%s"><svg x="%d" y="%d" width="%d" height="%d" viewBox="0 0 120 120">%s</svg>'
            '<path d="%s"/>%s</g></svg>\n'
            % (W, H, W, H, W - 2, H - 2, f((H - 2) / 2), bg, line, ink, ink, PAD, PAD, LOGO_S, LOGO_S, LOGO, small_d, title))


OUT = os.path.join(repo, "assets", "sello"); os.makedirs(OUT, exist_ok=True)
for name, bg, ink, line in (("claro", "#efe4cf", "#554242", "#554242"), ("oscuro", "#8b421e", "#efe4cf", "#efe4cf")):
    io.open(os.path.join(OUT, "un-proyecto-gofio-design-%s.svg" % name), "w", encoding="utf-8", newline="\n").write(sello(bg, ink, line))
print("ok", W, H)
