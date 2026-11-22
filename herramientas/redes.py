"""Lema, logotipos en PNG y piezas para redes sociales de Gofio Design.

Uso (desde la raíz del repositorio, con fonttools, brotli y cairosvg instalados):
    python -I herramientas/redes.py "$PWD"

Escribe:
- assets/marca/vertical-lema-{crema,marron}.svg: pintadera, título y lema «Cultivamos soluciones».
- assets/marca/png/*.png: los logotipos del kit en PNG con fondo transparente.
- assets/marca/redes/*.svg y *.png: avatar y portadas (LinkedIn, X, Facebook, Google,
  Instagram, Dribbble). Tintas planas: crema sobre barro, como el resto del kit.
Los textos van a trazos (Nunito de assets/fonts), así que no hace falta instalar fuentes.
"""
import io, os, re, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
import cairosvg

repo = sys.argv[1]
MARCA = os.path.join(repo, "assets", "marca")
PNG = os.path.join(MARCA, "png"); REDES = os.path.join(MARCA, "redes")
os.makedirs(PNG, exist_ok=True); os.makedirs(REDES, exist_ok=True)
BARRO, CREMA, MARRON = "#8b421e", "#efe4cf", "#554242"

LEMA = "Cultivamos soluciones"
DESCRIPTOR = "Proyectos y consultoría para la transformación ecosocial"


def leer(n):
    return io.open(os.path.join(MARCA, n), encoding="utf-8").read()


def cuerpo(svg):
    return re.sub(r"^<svg[^>]*>|</svg>\s*$", "", svg.strip())


LOGO = cuerpo(leer("logotipo-crema.svg"))            # caja 120x120, currentColor
TITULO = cuerpo(leer("titulo-crema.svg"))            # caja 682x120, línea base en y=96
FRISO = cuerpo(io.open(os.path.join(repo, "assets", "pintaderas", "friso.svg"), encoding="utf-8").read())  # 192x44

nunito = TTFont(os.path.join(repo, "assets", "fonts", "nunito-latin.woff2"))
N6 = instantiateVariableFont(TTFont(os.path.join(repo, "assets", "fonts", "nunito-latin.woff2")), {"wght": 600})
N4 = instantiateVariableFont(nunito, {"wght": 400})


def texto(t, size, f, ls=0.01):
    """Texto a trazos con la línea base en y=0. Devuelve (d, ancho)."""
    x = 0; ds = []; cm = f.getBestCmap(); gs = f.getGlyphSet(); k = size / f["head"].unitsPerEm
    for ch in t:
        n = cm[ord(ch)]; pen = SVGPathPen(gs); rp = DecomposingRecordingPen(gs)
        gs[n].draw(rp); rp.replay(TransformPen(pen, (k, 0, 0, -k, x, 0)))
        ds.append(pen.getCommands()); x += f["hmtx"][n][0] * k + ls * size
    return " ".join(c for c in ds if c), x - ls * size


def svg(w, h, body, label, color=CREMA, fondo=None):
    bg = '<rect width="%d" height="%d" fill="%s"/>' % (w, h, fondo) if fondo else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img" '
            'aria-label="%s" color="%s">%s%s</svg>\n' % (w, h, w, h, label, color, bg, body))


def logo(x, y, lado):
    return '<svg x="%.1f" y="%.1f" width="%.1f" height="%.1f" viewBox="0 0 120 120">%s</svg>' % (x, y, lado, lado, LOGO)


def titulo(x, y, ancho):
    """Título con la esquina superior de su caja 682x120 en (x, y). Devuelve (svg, alto)."""
    alto = ancho * 120 / 682
    return ('<svg x="%.1f" y="%.1f" width="%.1f" height="%.1f" viewBox="0 0 682 120">%s</svg>'
            % (x, y, ancho, alto, TITULO)), alto


def linea(t, x, y, size, f=N6, ancla="izq"):
    d, w = texto(t, size, f)
    if ancla == "centro": x -= w / 2
    return '<path d="%s" transform="translate(%.1f %.1f)" fill="currentColor"/>' % (d, x, y), w


def friso(y, w, alto):
    """Banda de pintadera a lo ancho, con el módulo de assets/pintaderas/friso.svg."""
    k = alto / 44
    return ('<defs><pattern id="f%d" width="192" height="44" patternUnits="userSpaceOnUse" '
            'patternTransform="translate(0 %.1f) scale(%.4f)">%s</pattern></defs>'
            '<rect y="%.1f" width="%d" height="%.1f" fill="url(#f%d)"/>' % (int(y), y, k, FRISO, y, w, alto, int(y)))


def escribe(nombre, texto_svg, png=True, ancho=None):
    ruta = os.path.join(REDES if not nombre.startswith("png/") else MARCA, nombre)
    io.open(ruta + ".svg", "w", encoding="utf-8", newline="\n").write(texto_svg)
    if png:
        cairosvg.svg2png(bytestring=texto_svg.encode(), write_to=ruta + ".png", output_width=ancho)


# ---------- Vertical con lema (kit) ----------
def vertical_lema(color):
    lado = 180; tw = 682; th = 120
    lema_sz = 46
    b = [logo((tw - lado) / 2, 0, lado)]
    t, _ = titulo(0, lado + 16, tw); b.append(t)
    l, _ = linea(LEMA, tw / 2, lado + 16 + th + 52, lema_sz, ancla="centro"); b.append(l)
    return svg(tw, int(lado + 16 + th + 70), "".join(b), "Gofio Design. %s" % LEMA, color)


for tono, col in (("crema", CREMA), ("marron", MARRON)):
    io.open(os.path.join(MARCA, "vertical-lema-%s.svg" % tono), "w", encoding="utf-8", newline="\n").write(vertical_lema(col))

# ---------- Logotipos del kit en PNG (fondo transparente) ----------
for n in sorted(os.listdir(MARCA)):
    if n.endswith(".svg") and n not in ("favicon.svg", "og-image.svg"):
        s = leer(n)
        vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
        ancho = 1024 if vb[2] <= vb[3] * 1.2 else 2000
        cairosvg.svg2png(bytestring=s.encode(), write_to=os.path.join(PNG, n[:-4] + ".png"), output_width=ancho)

# ---------- Avatar: sirve para LinkedIn, X, WhatsApp, Instagram, Dribbble y Google ----------
# El círculo de recorte de las redes deja libre el 70 % central: la pintadera ocupa el 60 %.
A = 1080
escribe("avatar", svg(A, A, logo(A * 0.2, A * 0.2, A * 0.6), "Gofio Design", fondo=BARRO))


# ---------- Portadas ----------
def portada(w, h, libre_izq=0.0, con_descriptor=True):
    """Barro con frisos arriba y abajo; pintadera, título, lema y descriptor.
    libre_izq: fracción del ancho que se deja vacía a la izquierda (donde la red pone el avatar)."""
    fr = max(18, h * 0.075); m = h * 0.07
    b = [friso(m, w, fr), friso(h - m - fr, w, fr)]
    zona_x0 = w * libre_izq; zona_w = w - zona_x0
    interior = h - 2 * (m + fr)
    lado = interior * 0.62
    tw = min(zona_w * 0.5, lado * 3.3)
    th = tw * 120 / 682
    lema_sz = th * 0.42; desc_sz = th * 0.26
    alto_txt = th + lema_sz * 1.35 + (desc_sz * 1.6 if con_descriptor else 0)
    ancho_txt = max(tw, texto(DESCRIPTOR, desc_sz, N4)[1] if con_descriptor else 0)
    ancho_bloque = lado + lado * 0.18 + ancho_txt
    x0 = zona_x0 + (zona_w - ancho_bloque) / 2
    cy = h / 2
    b.append(logo(x0, cy - lado / 2, lado))
    tx = x0 + lado * 1.18
    ty = cy - alto_txt / 2 - th * 0.12
    t, _ = titulo(tx - tw * 0.03, ty, tw); b.append(t)
    y = ty + th + lema_sz * 1.05
    b.append(linea(LEMA, tx, y, lema_sz)[0])
    if con_descriptor:
        b.append(linea(DESCRIPTOR, tx, y + desc_sz * 1.75, desc_sz, N4)[0])
    return svg(w, h, "".join(b), "Gofio Design. %s. %s" % (LEMA, DESCRIPTOR), fondo=BARRO)


def vertical(w, h, con_descriptor=True, k=1.0):
    """Formato alto o casi cuadrado (Instagram, Dribbble): todo centrado. k agranda los textos."""
    u = min(w, h * 0.8)
    fr = u * 0.05; m = u * 0.06
    b = [friso(m, w, fr), friso(h - m - fr, w, fr)]
    lado = u * 0.4; tw = u * 0.74; th = tw * 120 / 682
    lema_sz = u * 0.055 * k; desc_sz = u * 0.032 * k
    desc_sz = min(desc_sz, desc_sz * w * 0.84 / texto(DESCRIPTOR, desc_sz, N4)[1])  # que quepa con margen
    total = lado + u * 0.07 + th + lema_sz * 1.6 + (desc_sz * 2.2 if con_descriptor else 0)
    y = (h - total) / 2
    b.append(logo((w - lado) / 2, y, lado)); y += lado + u * 0.07
    t, _ = titulo((w - tw) / 2, y, tw); b.append(t); y += th + lema_sz * 1.2
    b.append(linea(LEMA, w / 2, y, lema_sz, ancla="centro")[0])
    if con_descriptor:
        b.append(linea(DESCRIPTOR, w / 2, y + desc_sz * 2.2, desc_sz, N4, ancla="centro")[0])
    return svg(w, h, "".join(b), "Gofio Design. %s. %s" % (LEMA, DESCRIPTOR), fondo=BARRO)


escribe("linkedin-perfil-1584x396", portada(1584, 396, libre_izq=0.28))
escribe("linkedin-empresa-1128x191", portada(1128, 191, con_descriptor=False))
escribe("x-cabecera-1500x500", portada(1500, 500, libre_izq=0.22))
escribe("facebook-portada-1640x624", portada(1640, 624, libre_izq=0.2))
escribe("google-portada-1024x576", portada(1024, 576))
escribe("instagram-publicacion-1080x1350", vertical(1080, 1350))
escribe("instagram-historia-1080x1920", vertical(1080, 1920, k=1.2))
escribe("dribbble-presentacion-1600x1200", vertical(1600, 1200))
print("ok")
