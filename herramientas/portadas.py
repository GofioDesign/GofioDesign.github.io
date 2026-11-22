import sys, io, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo_lib
root, symfile = sys.argv[1], sys.argv[2]
GD = open(sys.argv[3], encoding="utf-8").read().strip()
SYMBOLS = open(symfile, encoding="utf-8").read().strip()
WA = "M12 2a9.9 9.9 0 0 0-8.5 15.1L2 22l5-1.4A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .9.9-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 12 12 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"
GD_OLD = '<path d="M64 99.1887V171.876C27.0639 161.429 0 127.47 0 87.1886C0 42.6581 33.0758 5.85272 76 0V87.1886H38V99.1887H64Z"/><path d="M100 1.52588e-05C142.924 5.85274 176 42.6581 176 87.1887C176 131.719 142.924 168.525 100 174.377L100 1.52588e-05Z"/>'

PAGES = {
 "es": dict(file="index.html", locale="es_ES",
   title="Gofio Design | Estudio en Tenerife desde 2005",
   desc="Estudio en Tenerife desde 2005. Webs, redes de datos, jardines de flora autóctona y patrimonio, hechos para durar. Escríbeme por WhatsApp.",
   ogdesc="Webs, redes de datos, jardines de flora autóctona y patrimonio, hechos para durar.",
   skip="Saltar al contenido", home="Gofio Design, inicio", navlabel="Idiomas", pfile="proyectos.html", projects="Proyectos",
   lema="Cultivamos soluciones",
   hook="Proyectos y consultoría para la transformación ecosocial. En Tenerife desde 2005: webs, redes, jardines y patrimonio, hechos para durar.",
   cta="Escríbeme por WhatsApp", layerslabel="Tres capas de trabajo",
   layers=["Identidad e infraestructura digital", "Paisaje y territorio canario", "Gestión de activos y dinamización"],
   h_proj="Proyectos reales", all="Ver los doce proyectos publicados y los que están en marcha",
   h_serv="Qué hacemos",
   items=[[("Sistemas de marca", "Logotipos y branding para empresas en Canarias que buscan proyectar profesionalidad y raíces."),
           ("Redes de datos", "Instalación técnica y certificación de redes para oficinas, alojamientos y viviendas en la isla."),
           ("Marketing digital", "Presencia online y comunicación para el mercado local y europeo.")],
          [("Diseño de jardines", "Espacios exteriores con flora autóctona y riego eficiente, adaptados al clima de Tenerife."),
           ("Ejecución y renaturalización", "Construcción y mantenimiento de proyectos que recuperan la biodiversidad local.")],
          [("Logística circular y eventos", "Coordinación de eventos sostenibles, patrocinios y maquinaria técnica para sectores creativos."),
           ("Interpretación del patrimonio", "Dinamización en reservas ambientales y proyectos educativos con centros de enseñanza."),
           ("Eficiencia y ahorro", "Talleres y consultoría para aplicar medidas de eficiencia energética en comunidades locales.")]],
   h_close="¿Hablamos de tu encargo?",
   close="Cuéntame qué necesitas. Te respondo en persona, desde Tenerife.",
   legal="Legal y privacidad", kit="Kit de marca",
   cookielabel="Aviso de cookies",
   cookie="Utilizamos cookies para mejorar su experiencia y analizar el tráfico. Puede aceptar todas las cookies o rechazar las no esenciales.",
   more="Más información", accept="Aceptar", reject="Rechazar"),
 "en": dict(file="en.html", locale="en_GB",
   title="Gofio Design | Studio in Tenerife since 2005",
   desc="Studio in Tenerife since 2005. Websites, data networks, native-flora gardens and heritage, made to last. Message me on WhatsApp.",
   ogdesc="Websites, data networks, native-flora gardens and heritage, made to last.",
   skip="Skip to content", home="Gofio Design, home", navlabel="Languages", pfile="projects.html", projects="Projects",
   lema="We grow solutions",
   hook="Projects and consultancy for eco-social change. In Tenerife since 2005: websites, networks, gardens and heritage, made to last.",
   cta="Message me on WhatsApp", layerslabel="Three layers of work",
   layers=["Digital identity and infrastructure", "Canarian landscape and territory", "Asset management and community engagement"],
   h_proj="Real projects", all="See the twelve published projects and those in progress",
   h_serv="What we do",
   items=[[("Brand systems", "Logos and branding for companies in the Canary Islands that want to project professionalism and roots."),
           ("Data networks", "Technical installation and certification of networks for offices, holiday lets and homes on the island."),
           ("Digital marketing", "Online presence and communication for the local and European market.")],
          [("Garden design", "Outdoor spaces with native flora and efficient irrigation, adapted to Tenerife’s climate."),
           ("Build and rewilding", "Construction and maintenance of projects that restore local biodiversity.")],
          [("Circular logistics and events", "Coordination of sustainable events, sponsorships and technical equipment for creative sectors."),
           ("Heritage interpretation", "Activities in nature reserves and educational projects with schools."),
           ("Efficiency and savings", "Workshops and consultancy to apply energy-efficiency measures in local communities.")]],
   h_close="Shall we talk about your project?",
   close="Tell me what you need. I reply in person, from Tenerife.",
   legal="Legal &amp; Privacy", kit="Brand kit",
   cookielabel="Cookie notice",
   cookie="We use cookies to improve your experience and analyse traffic. You can accept all cookies or reject non-essential ones.",
   more="Read more", accept="Accept", reject="Reject"),
 "de": dict(file="de.html", locale="de_DE",
   title="Gofio Design | Studio auf Teneriffa seit 2005",
   desc="Studio auf Teneriffa seit 2005. Websites, Datennetze, Gärten mit einheimischer Flora und Kulturerbe, auf Dauer angelegt. Schreiben Sie mir auf WhatsApp.",
   ogdesc="Websites, Datennetze, Gärten mit einheimischer Flora und Kulturerbe, auf Dauer angelegt.",
   skip="Zum Inhalt springen", home="Gofio Design, Startseite", navlabel="Sprachen", pfile="projekte.html", projects="Projekte",
   lema="Wir lassen Lösungen wachsen",
   hook="Projekte und Beratung für den sozial-ökologischen Wandel. Auf Teneriffa seit 2005: Websites, Netzwerke, Gärten und Kulturerbe, auf Dauer angelegt.",
   cta="Schreiben Sie mir auf WhatsApp", layerslabel="Drei Arbeitsbereiche",
   layers=["Digitale Identität und Infrastruktur", "Kanarische Landschaft und Territorium", "Asset Management und Community-Engagement"],
   h_proj="Echte Projekte", all="Alle zwölf veröffentlichten Projekte und die laufenden ansehen",
   h_serv="Was wir machen",
   items=[[("Markensysteme", "Logos und Branding für Unternehmen auf den Kanaren, die Professionalität und Verwurzelung zeigen wollen."),
           ("Datennetzwerke", "Technische Installation und Zertifizierung von Netzwerken für Büros, Ferienunterkünfte und Wohnungen auf der Insel."),
           ("Digitales Marketing", "Online-Präsenz und Kommunikation für den lokalen und europäischen Markt.")],
          [("Gartengestaltung", "Außenbereiche mit einheimischer Flora und sparsamer Bewässerung, angepasst an das Klima Teneriffas."),
           ("Umsetzung und Renaturierung", "Bau und Pflege von Projekten, die die lokale Artenvielfalt zurückbringen.")],
          [("Kreislauflogistik und Veranstaltungen", "Koordination nachhaltiger Veranstaltungen, Sponsoring und Technik für kreative Branchen."),
           ("Vermittlung des Kulturerbes", "Programme in Naturschutzgebieten und Bildungsprojekte mit Schulen."),
           ("Effizienz und Einsparung", "Workshops und Beratung zur Umsetzung von Energieeffizienz in lokalen Gemeinschaften.")]],
   h_close="Sprechen wir über Ihr Vorhaben?",
   close="Erzählen Sie mir, was Sie brauchen. Ich antworte persönlich, von Teneriffa aus.",
   legal="Rechtliches &amp; Datenschutz", kit="Markenkit",
   cookielabel="Cookie-Hinweis",
   cookie="Wir verwenden Cookies, um Ihr Erlebnis zu verbessern und den Datenverkehr zu analysieren. Sie können alle Cookies akzeptieren oder die nicht notwendigen ablehnen.",
   more="Mehr erfahren", accept="Akzeptieren", reject="Ablehnen"),
 "fr": dict(file="fr.html", locale="fr_FR",
   title="Gofio Design | Studio à Tenerife depuis 2005",
   desc="Studio à Tenerife depuis 2005. Sites web, réseaux de données, jardins de flore indigène et patrimoine, faits pour durer. Écrivez-moi sur WhatsApp.",
   ogdesc="Sites web, réseaux de données, jardins de flore indigène et patrimoine, faits pour durer.",
   skip="Aller au contenu", home="Gofio Design, accueil", navlabel="Langues", pfile="projets.html", projects="Projets",
   lema="Nous cultivons des solutions",
   hook="Projets et conseil pour la transformation écosociale. À Tenerife depuis 2005&#8239;: sites web, réseaux, jardins et patrimoine, faits pour durer.",
   cta="Écrivez-moi sur WhatsApp", layerslabel="Trois domaines de travail",
   layers=["Identité numérique et infrastructure", "Paysage et territoire canarien", "Gestion d’actifs et dynamisation sociale"],
   h_proj="Projets réels", all="Voir les douze projets publiés et ceux en cours",
   h_serv="Ce que nous faisons",
   items=[[("Systèmes de marque", "Logos et image de marque pour les entreprises des Canaries qui veulent affirmer leur professionnalisme et leurs racines."),
           ("Réseaux de données", "Installation technique et certification de réseaux pour bureaux, hébergements touristiques et logements sur l’île."),
           ("Marketing numérique", "Présence en ligne et communication pour le marché local et européen.")],
          [("Conception de jardins", "Espaces extérieurs avec flore indigène et arrosage économe, adaptés au climat de Tenerife."),
           ("Réalisation et renaturation", "Construction et entretien de projets qui restaurent la biodiversité locale.")],
          [("Logistique circulaire et événements", "Coordination d’événements durables, de parrainages et de matériel technique pour les secteurs créatifs."),
           ("Interprétation du patrimoine", "Animation dans les réserves naturelles et projets éducatifs avec les établissements scolaires."),
           ("Efficacité et économies", "Ateliers et conseil pour appliquer des mesures d’efficacité énergétique dans les communautés locales.")]],
   h_close="Parlons de votre projet&#8239;?",
   close="Dites-moi ce dont vous avez besoin. Je réponds en personne, depuis Tenerife.",
   legal="Mentions légales &amp; confidentialité", kit="Kit de marque",
   cookielabel="Avis sur les cookies",
   cookie="Nous utilisons des cookies pour améliorer votre expérience et analyser le trafic. Vous pouvez accepter tous les cookies ou refuser ceux qui ne sont pas essentiels.",
   more="En savoir plus", accept="Accepter", reject="Refuser"),
}
ORDER = ["es", "en", "de", "fr"]
LAYER_IDS = [("capa-identidad", "p-cuadrado"), ("capa-paisaje", "p-circulo"), ("capa-gestion", "p-triangulo")]
TILES = [("mi-terapia-regresiva", "mi-terapia-regresiva.jpg", "Mi Terapia Regresiva"),
         ("archipielago-vivo", "archipielago-vivo.jpg", "Archipiélago Vivo"),
         ("diez-claves", "diez-claves.jpg", "Diez Claves")]


def page(lang):
    p = PAGES[lang]
    url = "https://gofiodesign.eu/" + p["file"]
    nav = []
    for l in ORDER:
        attrs = ' hreflang="%s"' % l
        if l != lang:
            attrs += ' lang="%s"' % l
        else:
            attrs += ' aria-current="page"'
        nav.append('<a href="%s"%s>%s</a>' % (PAGES[l]["file"], attrs, l.upper()))
    navhtml = '\n          <span class="punto" aria-hidden="true">·</span>\n          '.join(nav)

    layers = []
    for (lid, sym), name in zip(LAYER_IDS, p["layers"]):
        layers.append(
            '        <li>\n'
            '          <a href="#%s">\n'
            '            <svg class="pintadera" aria-hidden="true" focusable="false"><use href="#%s" /></svg>\n'
            '            <span>%s</span>\n'
            '          </a>\n'
            '        </li>' % (lid, sym, name))

    tiles = []
    for a, img, n in TILES:
        tiles.append(
            '          <li>\n'
            '            <a class="azulejo" href="%s#%s">\n'
            '              <img src="assets/projects/%s" alt="" width="1280" height="800" loading="lazy" />\n'
            '              <span>%s</span>\n'
            '            </a>\n'
            '          </li>' % (p["pfile"], a, img, n))

    details = []
    for (lid, sym), name, items in zip(LAYER_IDS, p["layers"], p["items"]):
        dl = "\n".join("              <dt>%s</dt>\n              <dd>%s</dd>" % (t, d) for t, d in items)
        details.append(
            '          <article class="capa-detalle" id="%s">\n'
            '            <svg class="pintadera" aria-hidden="true" focusable="false"><use href="#%s" /></svg>\n'
            '            <h3>%s</h3>\n'
            '            <dl>\n%s\n            </dl>\n'
            '          </article>' % (lid, sym, name, dl))

    alts = "\n".join('    <link rel="alternate" hreflang="%s" href="https://gofiodesign.eu/%s" />' % (l, PAGES[l]["file"]) for l in ORDER)
    btn = ('<a class="boton-whatsapp" href="https://wa.me/34623760960">\n'
           '          <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="%s"/></svg>\n'
           '          %s\n'
           '        </a>') % (WA, p["cta"])
    symbols = SYMBOLS.replace("\n", "\n      ")

    out = []
    out.append('<!doctype html>')
    out.append('<html lang="%s">' % lang)
    out.append('  <head>')
    out.append('    <meta charset="UTF-8" />')
    out.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0" />')
    out.append('    <title>%s</title>' % p["title"])
    out.append('    <meta name="description" content="%s" />' % p["desc"])
    out.append('    <link rel="canonical" href="%s" />' % url)
    out.append(alts)
    out.append('    <link rel="alternate" hreflang="x-default" href="https://gofiodesign.eu/index.html" />')
    out.append('    <meta name="geo.region" content="ES-CN" />')
    out.append('    <meta name="geo.placename" content="Tenerife" />')
    out.append(seo_lib.block(lang, p["file"], p["title"], p["ogdesc"], "assets/og/inicio-%s.png" % lang, seo_lib.ALT_HOME[lang]))
    out.append('    <link rel="preload" href="assets/fonts/poiret-one-latin.woff2" as="font" type="font/woff2" crossorigin />')
    out.append('    <link rel="preload" href="assets/fonts/nunito-latin.woff2" as="font" type="font/woff2" crossorigin />')
    out.append('    <link rel="stylesheet" href="portada.css?v=20261115c" />')
    out.append('    <link rel="icon" href="/favicon.ico" sizes="any" />')
    out.append('    <link rel="icon" href="/assets/brand/favicon.svg" type="image/svg+xml" />')
    out.append('    <link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png" />')
    out.append('    <link rel="manifest" href="/site.webmanifest" />')
    out.append('    <meta name="theme-color" content="#8b421e" />')
    out.append('  </head>')
    out.append('  <body>')
    out.append('    <a class="skip-link" href="#principal">%s</a>' % p["skip"])
    out.append('')
    out.append('    <div id="cookie-banner" class="cookie-banner" role="region" aria-label="%s">' % p["cookielabel"])
    out.append('      <div class="contenedor">')
    out.append('        <p>%s <a href="privacy.html">%s</a>.</p>' % (p["cookie"], p["more"]))
    out.append('        <div class="cookie-actions">')
    out.append('          <button type="button" class="cookie-accept" onclick="acceptCookies()">%s</button>' % p["accept"])
    out.append('          <button type="button" class="cookie-reject" onclick="rejectCookies()">%s</button>' % p["reject"])
    out.append('        </div>')
    out.append('      </div>')
    out.append('    </div>')
    out.append('')
    out.append('    <svg class="sprite" aria-hidden="true" focusable="false">')
    out.append('      ' + symbols)
    out.append('    </svg>')
    out.append('')
    out.append('    <header class="cabecera">')
    out.append('      <div class="barra contenedor">')
    out.append('        <a class="sello-gd" href="%s" aria-label="%s">' % (p["file"], p["home"]))
    out.append('          <svg viewBox="0 0 120 120" aria-hidden="true" focusable="false">%s</svg>' % GD)
    out.append('        </a>')
    out.append('        <nav class="nav-lenguas" aria-label="%s">' % p["navlabel"])
    out.append('          ' + navhtml)
    out.append('        </nav>')
    out.append('      </div>')
    out.append('      <div class="friso" aria-hidden="true"></div>')
    out.append('')
    out.append('      <div class="frente contenedor">')
    out.append('        <h1 class="titulo">GOFIO DESIGN</h1>')
    out.append('        <p class="lema">%s</p>' % p["lema"])
    out.append('        <p class="gancho">%s</p>' % p["hook"].replace(". ", ".<br />\n          ", 1))
    out.append('        ' + btn)
    out.append('      </div>')
    out.append('')
    out.append('      <div class="friso-fino" aria-hidden="true"></div>')
    out.append('      <ul class="capas contenedor" aria-label="%s">' % p["layerslabel"])
    out.append("\n".join(layers))
    out.append('      </ul>')
    out.append('      <div class="friso-fino" aria-hidden="true"></div>')
    out.append('    </header>')
    out.append('')
    out.append('    <main id="principal">')
    out.append('      <section class="proyectos contenedor" aria-labelledby="h-proyectos">')
    out.append('        <h2 id="h-proyectos">%s</h2>' % p["h_proj"])
    out.append('        <ul class="azulejos">')
    out.append("\n".join(tiles))
    out.append('        </ul>')
    out.append('        <p class="ver-todos"><a href="%s">%s</a></p>' % (p["pfile"], p["all"]))
    out.append('      </section>')
    out.append('')
    out.append('      <div class="friso-fino" aria-hidden="true"></div>')
    out.append('')
    out.append('      <section class="servicios contenedor" aria-labelledby="h-servicios">')
    out.append('        <h2 id="h-servicios">%s</h2>' % p["h_serv"])
    out.append('        <div class="capas-detalle">')
    out.append("\n".join(details))
    out.append('        </div>')
    out.append('      </section>')
    out.append('')
    out.append('      <div class="friso-fino" aria-hidden="true"></div>')
    out.append('')
    out.append('      <section class="cierre contenedor" aria-labelledby="h-cierre">')
    out.append('        <h2 id="h-cierre">%s</h2>' % p["h_close"])
    out.append('        <p>%s</p>' % p["close"])
    out.append('        ' + btn)
    out.append('      </section>')
    out.append('    </main>')
    out.append('')
    out.append('    <div class="friso" aria-hidden="true"></div>')
    out.append('    <footer class="pie">')
    out.append('      <svg class="sello-pie" viewBox="0 0 120 120" aria-hidden="true" focusable="false">%s</svg>' % GD)
    out.append('      <p>')
    out.append('        &copy; 2005–<span id="current-year">2026</span>')
    out.append('        <strong>Gofio Design</strong> |')
    out.append('        <a href="privacy.html">%s</a>' % p["legal"])
    out.append('        | <a href="marca.html">%s</a>' % p["kit"])
    out.append('      </p>')
    out.append('      <div id="email-placeholder"></div>')
    out.append('    </footer>')
    out.append('')
    out.append('    <script src="script.js"></script>')
    if lang == "es":  # se conserva tal como estaba en la portada española
        out.append('    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-55DKZ9C5" height="0" width="0" style="display: none; visibility: hidden"></iframe></noscript>')
    out.append('  </body>')
    out.append('</html>')
    return "\n".join(out) + "\n"


for l in ORDER:
    with io.open(root + "/" + PAGES[l]["file"], "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page(l))
print("ok")
