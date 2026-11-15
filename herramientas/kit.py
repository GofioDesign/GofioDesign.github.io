"""Genera los SVG del kit de marca Gofio Design (pintadera de dientes de sierra)."""
import io, re, sys, os
repo, S = sys.argv[1], sys.argv[2]
OUT = os.path.join(repo, "assets", "marca")
BRAND = os.path.join(repo, "assets", "brand")
BARRO, HONDO, CREMA, MARRON, AMBAR = "#8b421e", "#59220d", "#efe4cf", "#554242", "#e6b458"

LOGO = io.open(os.path.join(S, "logo-prop.txt"), encoding="utf-8").read().strip()      # 120x120, currentColor
LOGO16 = io.open(os.path.join(S, "logo-16.txt"), encoding="utf-8").read().strip()
FRISO = io.open(os.path.join(repo, "assets", "pintaderas", "friso.svg"), encoding="utf-8").read()

# Silueta plana de «GOFIO DESIGN» (Poiret One con la G y la D propias), tomada del título del kit anterior
src = io.open(os.path.join(OUT, "titulo-crema.svg"), encoding="utf-8").read()
src = re.sub(r"<metadata>.*?</metadata>", "", src, flags=re.S)
TITLE_D = re.findall(r'<path d="([^"]+)"', src)[0]
TITLE = '<g transform="translate(20 96)"><path d="%s"/></g>' % TITLE_D   # en caja 682x120


def svg(vb, body, label, color=None, extra=""):
    c = ' color="%s"' % color if color else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" role="img" aria-label="%s"%s>%s%s</svg>\n'
            % (vb, label, c, extra, body))


def write(path, text):
    io.open(path, "w", encoding="utf-8", newline="\n").write(text)


files = {}
# Logotipo (pintadera) en tres tintas planas
for tone, col in (("crema", CREMA), ("marron", MARRON), ("ambar", AMBAR)):
    files["logotipo-%s.svg" % tone] = svg("0 0 120 120", LOGO, "Gofio Design", col)
# Solo el GD, para 16 px y favicons
for tone, col in (("crema", CREMA), ("marron", MARRON)):
    files["monograma-gd-%s.svg" % tone] = svg("0 0 120 120", LOGO16, "Gofio Design", col)
# Título plano
for tone, col in (("crema", CREMA), ("marron", MARRON)):
    files["titulo-%s.svg" % tone] = svg("0 0 682 120", '<g fill="currentColor">%s</g>' % TITLE, "GOFIO DESIGN", col)
# Logotipo horizontal: pintadera y título en línea
for tone, col in (("crema", CREMA), ("marron", MARRON)):
    body = ('<svg width="120" height="120" viewBox="0 0 120 120">%s</svg>'
            '<svg x="128" y="6" width="619" height="109" viewBox="0 0 682 120"><g fill="currentColor">%s</g></svg>' % (LOGO, TITLE))
    files["horizontal-%s.svg" % tone] = svg("0 0 760 120", body, "Gofio Design", col)
# Logotipo vertical: pintadera encima, título debajo
for tone, col in (("crema", CREMA), ("marron", MARRON)):
    body = ('<svg x="251" y="0" width="180" height="180" viewBox="0 0 120 120">%s</svg>'
            '<svg x="0" y="196" width="682" height="120" viewBox="0 0 682 120"><g fill="currentColor">%s</g></svg>' % (LOGO, TITLE))
    files["vertical-%s.svg" % tone] = svg("0 0 682 316", body, "Gofio Design", col)
# Icono de app: barro a sangre con la pintadera en crema
files["icono-app.svg"] = svg("0 0 512 512",
    '<rect width="512" height="512" fill="%s"/><svg x="76" y="76" width="360" height="360" viewBox="0 0 120 120">%s</svg>' % (BARRO, LOGO),
    "Gofio Design", CREMA)
# Favicon: solo el GD, marrón; crema si el navegador está en modo oscuro
files["favicon.svg"] = svg("0 0 120 120", LOGO16, "Gofio Design",
    extra="<style>svg{color:%s}@media (prefers-color-scheme:dark){svg{color:%s}}</style>" % (MARRON, CREMA))
# Imagen para redes 1200x630: barro, frisos arriba y abajo, pintadera y título
tile = re.sub(r'^<svg[^>]*>|</svg>\s*$', "", FRISO.strip())
og = ('<defs><pattern id="friso" width="192" height="44" patternUnits="userSpaceOnUse">%s</pattern></defs>'
      '<rect width="1200" height="630" fill="%s"/>'
      '<svg y="40" width="1200" height="44"><rect width="1200" height="44" fill="url(#friso)"/></svg>'
      '<svg y="546" width="1200" height="44"><rect width="1200" height="44" fill="url(#friso)"/></svg>'
      '<svg x="110" y="185" width="260" height="260" viewBox="0 0 120 120">%s</svg>'
      '<svg x="410" y="257" width="682" height="120" viewBox="0 0 682 120"><g fill="currentColor">%s</g></svg>'
      % (tile, BARRO, LOGO, TITLE))
files["og-image.svg"] = svg("0 0 1200 630", og, "Gofio Design, estudio en Tenerife desde 2005", CREMA)

for name, text in files.items():
    write(os.path.join(OUT, name), text)

# Archivos que usan las otras páginas del sitio
write(os.path.join(BRAND, "logo-sello.svg"), files["logotipo-marron.svg"])
write(os.path.join(BRAND, "logo-sello-oscuro.svg"), files["logotipo-crema.svg"])
write(os.path.join(BRAND, "favicon.svg"), files["favicon.svg"])

# Fuentes para rasterizar (se renderizan con Chrome sin ventana)
R = os.path.join(S, "raster"); os.makedirs(R, exist_ok=True)
page = lambda w, h, body: ('<!doctype html><html><head><style>html,body{margin:0;width:%dpx;height:%dpx;overflow:hidden;background:transparent}'
                           'svg{display:block;width:%dpx;height:%dpx}</style></head><body>%s</body></html>' % (w, h, w, h, body))
inline = lambda vb, body, col, bg="": '<svg viewBox="%s" style="color:%s">%s%s</svg>' % (vb, col, bg, body)
write(os.path.join(R, "og.html"), page(1200, 630, inline("0 0 1200 630", og, CREMA)))
for size in (180, 192, 512):
    pad = round(size * 0.15)
    body = '<rect width="120" height="120" fill="%s"/><svg x="18" y="18" width="84" height="84" viewBox="0 0 120 120">%s</svg>' % (BARRO, LOGO)
    write(os.path.join(R, "icon-%d.html" % size), page(size, size, inline("0 0 120 120", body, CREMA)))
for size, art in ((16, LOGO16), (32, LOGO), (48, LOGO)):
    write(os.path.join(R, "fav-%d.html" % size), page(size, size, inline("0 0 120 120", art, MARRON)))
print("ok", len(files))
