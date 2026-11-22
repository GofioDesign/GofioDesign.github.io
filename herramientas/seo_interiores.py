import io, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo_lib
os.chdir(sys.argv[1])
# Kit de marca
s = io.open("marca.html", encoding="utf-8").read()
desc = "Logotipo pintadera, título, sello «Un proyecto Gofio Design» y normas de uso de Gofio Design, en SVG."
blk = seo_lib.block("es", "marca.html", "Kit de marca | Gofio Design", desc, "assets/og/marca.png",
                    "«Kit de marca» de Gofio Design: el logotipo pintadera en crema, ámbar y marrón, y el GD solo.", alternates=False)
s = seo_lib.poner_bloque(s, blk)
io.open("marca.html", "w", encoding="utf-8", newline="\n").write(s)
# Privacidad
s = io.open("privacy.html", encoding="utf-8").read()
desc = "Aviso legal, protección de datos (RGPD) y cookies de Gofio Design, en castellano, inglés, alemán y francés."
blk = seo_lib.block("es", "privacy.html", "Legal y privacidad | Gofio Design", desc, "assets/og/privacidad.png",
                    "«Legal y privacidad» de Gofio Design, con el logotipo pintadera.", alternates=False)
s = re.sub(r'    <meta name="description" content="[^"]*" />\n', '    <meta name="description" content="%s" />\n' % desc, s, count=1)
s = seo_lib.poner_bloque(s, blk)
io.open("privacy.html", "w", encoding="utf-8", newline="\n").write(s)
print("ok")
