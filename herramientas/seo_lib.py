"""Bloque de Open Graph, Twitter y datos estructurados común a todas las páginas."""
import json

SITE = "https://gofiodesign.eu/"
LOCALE = {"es": "es_ES", "en": "en_GB", "de": "de_DE", "fr": "fr_FR"}
HOMES = {"es": "index.html", "en": "en.html", "de": "de.html", "fr": "fr.html"}
ALT_HOME = {
    "es": "Logotipo de Gofio Design, una pintadera con las letras GD, junto al nombre y «Estudio en Tenerife desde 2005».",
    "en": "Gofio Design logo, a pintadera seal with the letters GD, next to the name and “A studio in Tenerife since 2005”.",
    "de": "Logo von Gofio Design, ein Pintadera-Siegel mit den Buchstaben GD, neben dem Namen und „Studio auf Teneriffa seit 2005“.",
    "fr": "Logo de Gofio Design, une pintadera avec les lettres GD, à côté du nom et « Studio à Tenerife depuis 2005 ».",
}
ALT_PROJ = {
    "es": "«Proyectos web» de Gofio Design, con capturas de Mi Terapia Regresiva, Archipiélago Vivo y Diez Claves.",
    "en": "Gofio Design “Web projects”, with screenshots of Mi Terapia Regresiva, Archipiélago Vivo and Diez Claves.",
    "de": "„Webprojekte“ von Gofio Design, mit Bildschirmfotos von Mi Terapia Regresiva, Archipiélago Vivo und Diez Claves.",
    "fr": "« Projets web » de Gofio Design, avec des captures de Mi Terapia Regresiva, Archipiélago Vivo et Diez Claves.",
}
DESC_ORG = "Estudio en Tenerife desde 2005: webs, redes de datos, jardines de flora autóctona y patrimonio."


def org():
    return {"@type": "ProfessionalService", "@id": SITE + "#estudio", "name": "Gofio Design", "url": SITE,
            "logo": SITE + "assets/brand/icon-512.png", "image": SITE + "assets/og/inicio-es.png",
            "description": DESC_ORG, "foundingDate": "2005", "email": "hola@gofiodesign.eu",
            "telephone": "+34623760960",
            "address": {"@type": "PostalAddress", "addressLocality": "Tenerife", "addressRegion": "Canarias", "addressCountry": "ES"},
            "areaServed": ["Tenerife", "Islas Canarias"],
            "knowsLanguage": ["es", "en", "de", "fr"]}


def block(lang, url, title, desc, image, alt, ldtype="WebPage", alternates=True, indent="    "):
    """Devuelve las líneas de <head> desde og:type hasta el JSON-LD (sin title/description/canonical)."""
    full = SITE + url
    img = SITE + image
    L = ['<meta property="og:type" content="website" />',
         '<meta property="og:site_name" content="Gofio Design" />',
         '<meta property="og:locale" content="%s" />' % LOCALE[lang]]
    if alternates:
        L += ['<meta property="og:locale:alternate" content="%s" />' % LOCALE[l] for l in LOCALE if l != lang]
    L += ['<meta property="og:title" content="%s" />' % title,
          '<meta property="og:description" content="%s" />' % desc,
          '<meta property="og:url" content="%s" />' % full,
          '<meta property="og:image" content="%s" />' % img,
          '<meta property="og:image:type" content="image/png" />',
          '<meta property="og:image:width" content="1200" />',
          '<meta property="og:image:height" content="630" />',
          '<meta property="og:image:alt" content="%s" />' % alt,
          '<meta name="twitter:card" content="summary_large_image" />',
          '<meta name="twitter:title" content="%s" />' % title,
          '<meta name="twitter:description" content="%s" />' % desc,
          '<meta name="twitter:image" content="%s" />' % img,
          '<meta name="twitter:image:alt" content="%s" />' % alt]
    page = {"@type": ldtype, "@id": full + "#pagina", "url": full, "name": title.replace("&amp;", "&"),
            "description": desc, "inLanguage": lang, "primaryImageOfPage": img,
            "isPartOf": {"@id": SITE + "#web"}, "publisher": {"@id": SITE + "#estudio"}}
    graph = [page, {"@type": "WebSite", "@id": SITE + "#web", "url": SITE, "name": "Gofio Design",
                    "inLanguage": ["es", "en", "de", "fr"], "publisher": {"@id": SITE + "#estudio"}}, org()]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    L.append('<script type="application/ld+json">%s</script>' % ld.replace("</", "<\\/"))
    return "\n".join(indent + x for x in L)
