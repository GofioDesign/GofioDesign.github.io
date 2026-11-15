"""Imágenes OG (1200x630) de cada página y cada idioma. Escribe HTML en <scratch>/og/ para rasterizar con Chrome."""
import io, os, sys
repo, S = sys.argv[1], sys.argv[2]
OUT = os.path.join(S, "og"); os.makedirs(OUT, exist_ok=True)
BASE = "file:///" + repo.replace("\\", "/").rstrip("/") + "/"

CSS = """
html,body{margin:0;width:1200px;height:630px;overflow:hidden}
body{background:#8b421e;color:#efe4cf;font-family:Nunito,sans-serif;position:relative}
.friso{position:absolute;left:0;right:0;height:44px;background:url(assets/pintaderas/friso.svg) repeat-x left center}
.arriba{top:40px}.abajo{bottom:40px}
.caja{position:absolute;inset:84px 0;display:flex;align-items:center;gap:56px;padding:0 96px}
.titulo{font-family:"GD Glifos","Poiret One",sans-serif;font-weight:400;text-transform:uppercase;letter-spacing:.02em;color:#f7ede9;line-height:1.02;margin:0}
.sub{margin:18px 0 0;font-weight:800;font-size:34px;line-height:1.25;color:#f7ede9}
.linea{margin:12px 0 0;font-size:27px;line-height:1.35;max-width:24em}
.web{position:absolute;right:96px;bottom:100px;font-size:22px;font-weight:700;letter-spacing:.04em}
.col{display:flex;flex-direction:column}
.tiles{display:flex;gap:22px;margin-top:30px}
.tiles img{width:318px;height:199px;object-fit:cover;object-position:top;border:3px solid #efe4cf;border-radius:5px;display:block}
"""


def page(name, lang, body):
    html = ('<!doctype html><html lang="%s"><head><meta charset="utf-8"><base href="%s">'
            '<link rel="stylesheet" href="portada.css"><style>%s</style></head><body>'
            '<div class="friso arriba"></div><div class="friso abajo"></div>%s</body></html>' % (lang, BASE, CSS, body))
    io.open(os.path.join(OUT, name + ".html"), "w", encoding="utf-8").write(html)


LOGO = '<img src="assets/marca/logotipo-crema.svg" width="%d" height="%d" alt="">'
HOME = {
 "es": ("Estudio en Tenerife desde 2005", "Webs, redes, jardines y patrimonio, hechos para durar."),
 "en": ("A studio in Tenerife since 2005", "Websites, networks, gardens and heritage, made to last."),
 "de": ("Studio auf Teneriffa seit 2005", "Websites, Netzwerke, Gärten und Kulturerbe, auf Dauer angelegt."),
 "fr": ("Studio à Tenerife depuis 2005", "Sites web, réseaux, jardins et patrimoine, faits pour durer."),
}
for lang, (sub, line) in HOME.items():
    page("inicio-" + lang, lang, '<div class="caja">%s<div class="col"><p class="titulo" style="font-size:96px">Gofio Design</p>'
         '<p class="sub">%s</p><p class="linea">%s</p></div></div><p class="web">gofiodesign.eu</p>' % (LOGO % (230, 230), sub, line))

PROJ = {
 "es": ("Proyectos web", "Webs para clientes, plataformas culturales y herramientas abiertas"),
 "en": ("Web projects", "Client websites, cultural platforms and open tools"),
 "de": ("Webprojekte", "Websites für Kunden, Kulturplattformen und offene Werkzeuge"),
 "fr": ("Projets web", "Sites pour des clients, plateformes culturelles et outils ouverts"),
}
TILES = "".join('<img src="assets/projects/%s" alt="">' % f for f in ("mi-terapia-regresiva.jpg", "archipielago-vivo.jpg", "diez-claves.jpg"))
for lang, (t, sub) in PROJ.items():
    page("proyectos-" + lang, lang, '<div class="caja" style="align-items:flex-start;padding-top:20px"><div class="col">'
         '<div style="display:flex;align-items:center;gap:26px">%s<p class="titulo" style="font-size:78px">%s</p></div>'
         '<p class="linea" style="max-width:none;margin-top:16px">%s</p><div class="tiles">%s</div></div></div>' % (LOGO % (96, 96), t, sub, TILES))

page("marca", "es", '<div class="caja"><div class="col" style="flex:1"><p class="titulo" style="font-size:88px">Kit de marca</p>'
     '<p class="sub">Logotipo pintadera, título y sello</p><p class="linea">SVG listos para usar, con normas de uso.</p></div>'
     '<div style="display:grid;grid-template-columns:auto auto;gap:22px;align-items:center">'
     '<img src="assets/marca/logotipo-crema.svg" width="170" height="170" alt=""><img src="assets/marca/logotipo-ambar.svg" width="170" height="170" alt="">'
     '<div style="background:#efe4cf;border-radius:8px;padding:15px;display:grid;place-items:center"><img src="assets/marca/logotipo-marron.svg" width="140" height="140" alt=""></div>'
     '<img src="assets/marca/monograma-gd-crema.svg" width="120" height="120" alt="" style="justify-self:center"></div></div>')

page("privacidad", "es", '<div class="caja">%s<div class="col"><p class="titulo" style="font-size:84px">Legal y privacidad</p>'
     '<p class="sub">Datos personales y cookies</p><p class="linea">Castellano · English · Deutsch · Français</p></div></div>'
     '<p class="web">gofiodesign.eu</p>' % (LOGO % (200, 200)))
print("ok", len(os.listdir(OUT)))
