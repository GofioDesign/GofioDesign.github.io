"""Genera projects.html (en), projekte.html (de) y projets.html (fr) a partir de proyectos.html (es).
También ajusta la navegación de idiomas y los hreflang en las cuatro versiones."""
import io, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo_lib
repo = sys.argv[1]
os.chdir(repo)
FILES = {"es": "proyectos.html", "en": "projects.html", "de": "projekte.html", "fr": "projets.html"}
HOME = {"es": "index.html", "en": "en.html", "de": "de.html", "fr": "fr.html"}
LOCALE = {"es": "es_ES", "en": "en_GB", "de": "de_DE", "fr": "fr_FR"}
BACK = {"es": "← Inicio", "en": "← Home", "de": "← Startseite", "fr": "← Accueil"}
NAV = {"es": "Navegación", "en": "Navigation", "de": "Navigation", "fr": "Navigation"}

# (es, en, de, fr)
T = [
 ("Proyectos web | Gofio Design", "Web projects | Gofio Design", "Webprojekte | Gofio Design", "Projets web | Gofio Design"),
 ("Proyectos web de Gofio Design en Tenerife: webs para clientes, plataformas culturales y herramientas abiertas. Vista previa de cada proyecto.",
  "Web projects by Gofio Design in Tenerife: client websites, cultural platforms and open tools. A preview of each project.",
  "Webprojekte von Gofio Design auf Teneriffa: Websites für Kunden, Kulturplattformen und offene Werkzeuge. Mit Vorschau zu jedem Projekt.",
  "Projets web de Gofio Design à Tenerife : sites pour des clients, plateformes culturelles et outils ouverts. Un aperçu de chaque projet."),
 ("Webs para clientes, plataformas culturales y herramientas abiertas hechas por Gofio Design.",
  "Client websites, cultural platforms and open tools made by Gofio Design.",
  "Websites für Kunden, Kulturplattformen und offene Werkzeuge von Gofio Design.",
  "Sites pour des clients, plateformes culturelles et outils ouverts réalisés par Gofio Design."),
 ('<h1 class="titulo">Proyectos web</h1>', '<h1 class="titulo">Web projects</h1>', '<h1 class="titulo">Webprojekte</h1>', '<h1 class="titulo">Projets web</h1>'),
 ("Webs para clientes, plataformas culturales y herramientas abiertas diseñadas y desarrolladas por Gofio Design.",
  "Client websites, cultural platforms and open tools, designed and built by Gofio Design.",
  "Websites für Kunden, Kulturplattformen und offene Werkzeuge, gestaltet und entwickelt von Gofio Design.",
  "Sites pour des clients, plateformes culturelles et outils ouverts, conçus et développés par Gofio Design."),
 ('<h2 id="publicados">Publicados</h2>', '<h2 id="publicados">Published</h2>', '<h2 id="publicados">Veröffentlicht</h2>', '<h2 id="publicados">Publiés</h2>'),
 ('<h2 id="en-desarrollo">En desarrollo</h2>', '<h2 id="en-desarrollo">In progress</h2>', '<h2 id="en-desarrollo">In Arbeit</h2>', '<h2 id="en-desarrollo">En cours</h2>'),
 ("¿Hablamos de tu web?", "Shall we talk about your website?", "Sprechen wir über Ihre Website?", "Parlons de votre site&#8239;?"),
 ("<p>Cuéntame qué necesitas. Te respondo en persona, desde Tenerife.</p>",
  "<p>Tell me what you need. I reply in person, from Tenerife.</p>",
  "<p>Erzählen Sie mir, was Sie brauchen. Ich antworte persönlich, von Teneriffa aus.</p>",
  "<p>Dites-moi ce dont vous avez besoin. Je réponds en personne, depuis Tenerife.</p>"),
 ("Para añadir un proyecto", "To add a project (edit proyectos.html and regenerate)", "Projekt hinzufügen (proyectos.html bearbeiten und neu erzeugen)", "Ajouter un projet (modifier proyectos.html et régénérer)"),
 ("<dt>Problema</dt>", "<dt>Problem</dt>", "<dt>Problem</dt>", "<dt>Problème</dt>"),
 ("<dt>Idea</dt>", "<dt>Idea</dt>", "<dt>Idee</dt>", "<dt>Idée</dt>"),
 ("<dt>Concepto</dt>", "<dt>Concept</dt>", "<dt>Konzept</dt>", "<dt>Concept</dt>"),
 ("Ver proyecto<span class=\"solo-lector\"> (se abre en otra pestaña)</span>",
  "View project<span class=\"solo-lector\"> (opens in a new tab)</span>",
  "Projekt ansehen<span class=\"solo-lector\"> (öffnet in einem neuen Tab)</span>",
  "Voir le projet<span class=\"solo-lector\"> (s’ouvre dans un nouvel onglet)</span>"),
 ('ficha-pronto">Próximamente', 'ficha-pronto">Coming soon', 'ficha-pronto">Demnächst', 'ficha-pronto">Bientôt'),
 ('ficha-pronto">Trabajo para cliente', 'ficha-pronto">Client work', 'ficha-pronto">Kundenauftrag', 'ficha-pronto">Travail pour un client'),
 ('ficha-pronto">Privada', 'ficha-pronto">Private', 'ficha-pronto">Privat', 'ficha-pronto">Privée'),
 # etiquetas
 ("Cliente · Optimización web", "Client · Web optimisation", "Kunde · Web-Optimierung", "Client · Optimisation web"),
 ("Cliente · Bienestar", "Client · Wellbeing", "Kunde · Wohlbefinden", "Client · Bien-être"),
 ("Cultura · Patrimonio", "Culture · Heritage", "Kultur · Kulturerbe", "Culture · Patrimoine"),
 ("Editorial · Territorio", "Editorial · Territory", "Redaktion · Region", "Éditorial · Territoire"),
 ("Comunidad · Mapa colaborativo", "Community · Collaborative map", "Gemeinschaft · Gemeinsame Karte", "Communauté · Carte collaborative"),
 ("San Blas Reserva Ambiental · Educación", "San Blas Reserva Ambiental · Education", "San Blas Reserva Ambiental · Bildung", "San Blas Reserva Ambiental · Éducation"),
 ("San Blas Reserva Ambiental · Guías", "San Blas Reserva Ambiental · Guides", "San Blas Reserva Ambiental · Führer", "San Blas Reserva Ambiental · Guides"),
 ("San Blas Reserva Ambiental · En desarrollo", "San Blas Reserva Ambiental · In progress", "San Blas Reserva Ambiental · In Arbeit", "San Blas Reserva Ambiental · En cours"),
 ("Plataforma · Código abierto", "Platform · Open source", "Plattform · Open Source", "Plateforme · Open source"),
 ("Herramienta · Comunidad", "Tool · Community", "Werkzeug · Gemeinschaft", "Outil · Communauté"),
 ("Herramientas abiertas · Seguridad digital", "Open tools · Digital security", "Offene Werkzeuge · Digitale Sicherheit", "Outils ouverts · Sécurité numérique"),
 ("Idea · En desarrollo", "Idea · In progress", "Idee · In Arbeit", "Idée · En cours"),
 ("Herramienta · En desarrollo", "Tool · In progress", "Werkzeug · In Arbeit", "Outil · En cours"),
 ("App privada · En desarrollo", "Private app · In progress", "Private App · In Arbeit", "Appli privée · En cours"),
 # títulos traducibles
 ("<h3>Dossier de visitas escolares</h3>", "<h3>School visit dossier</h3>", "<h3>Dossier für Schulbesuche</h3>", "<h3>Dossier des visites scolaires</h3>"),
 ("<h3>Guías y materiales</h3>", "<h3>Guides and materials</h3>", "<h3>Führer und Materialien</h3>", "<h3>Guides et supports</h3>"),
 ("<h3>Campañas de email</h3>", "<h3>Email campaigns</h3>", "<h3>E-Mail-Kampagnen</h3>", "<h3>Campagnes e-mail</h3>"),
 ("<h3>App de meditación</h3>", "<h3>Meditation app</h3>", "<h3>Meditations-App</h3>", "<h3>Appli de méditation</h3>"),
 # Clínica Dental Dharma
 ("Una web en WordPress pesada y con costes de alojamiento altos.", "A heavy WordPress site with high hosting costs.", "Eine schwerfällige WordPress-Website mit hohen Hosting-Kosten.", "Un site WordPress lourd et coûteux à héberger."),
 ("Migrarla a una web ligera y optimizar sus recursos.", "Move it to a lightweight site and optimise its assets.", "Sie auf eine schlanke Website umziehen und ihre Ressourcen optimieren.", "Le migrer vers un site léger et optimiser ses ressources."),
 ("Web estática más rápida y más barata de alojar. Propuesta entregada al cliente, pendiente de publicar.", "A static site that is faster and cheaper to host. Proposal delivered to the client, not yet published.", "Statische Website, schneller und günstiger zu hosten. Dem Kunden übergeben, noch nicht veröffentlicht.", "Site statique plus rapide et moins cher à héberger. Proposition remise au client, pas encore publiée."),
 # Mi Terapia Regresiva
 ("Una terapia poco conocida, difícil de explicar y de dar el primer paso.", "A little-known therapy, hard to explain and hard to take the first step towards.", "Eine wenig bekannte Therapie, schwer zu erklären, und der erste Schritt fällt schwer.", "Une thérapie peu connue, difficile à expliquer et dont le premier pas coûte."),
 ("Contarla con artículos y respuestas a las dudas habituales.", "Explain it through articles and answers to common questions.", "Sie mit Artikeln und Antworten auf häufige Fragen erklären.", "La raconter avec des articles et des réponses aux questions fréquentes."),
 ("Web con artículos, preguntas frecuentes y contacto directo por WhatsApp.", "A site with articles, FAQs and direct contact on WhatsApp.", "Website mit Artikeln, häufigen Fragen und direktem Kontakt über WhatsApp.", "Site avec articles, questions fréquentes et contact direct par WhatsApp."),
 # Canarias.africa
 ("El arte y la cultura de Canarias, dispersos y sin un lugar común.", "Canary Islands art and culture, scattered with no common home.", "Kunst und Kultur der Kanaren, verstreut und ohne gemeinsamen Ort.", "L’art et la culture des Canaries, dispersés et sans lieu commun."),
 ("Un museo sin edificio, construido entre todos.", "A museum without a building, built by everyone.", "Ein Museum ohne Gebäude, von allen gemeinsam gebaut.", "Un musée sans bâtiment, construit par tous."),
 ("Catálogo Atlántico de Núnea Arqueología, abierto y colaborativo.", "The Atlantic Catalogue by Núnea Arqueología, open and collaborative.", "Der Atlantische Katalog von Núnea Arqueología, offen und gemeinschaftlich.", "Le Catalogue atlantique de Núnea Arqueología, ouvert et collaboratif."),
 # Macaronesico
 ("Entender el territorio sin quedarse en titulares.", "Understanding the islands beyond the headlines.", "Die Region verstehen, ohne bei Schlagzeilen stehen zu bleiben.", "Comprendre le territoire au-delà des gros titres."),
 ("Un laboratorio abierto que cruce datos y voces de quienes lo habitan.", "An open lab that brings together data and the voices of the people who live there.", "Ein offenes Labor, das Daten und Stimmen der Menschen vor Ort zusammenführt.", "Un laboratoire ouvert qui croise données et voix de ceux qui l’habitent."),
 ("Análisis, opinión y datos sobre Canarias y la Macaronesia.", "Analysis, opinion and data on the Canary Islands and Macaronesia.", "Analysen, Meinungen und Daten zu den Kanaren und Makaronesien.", "Analyses, opinions et données sur les Canaries et la Macaronésie."),
 # Archipiélago Vivo
 ("Personas e iniciativas que cuidan Canarias, pero no se encuentran.", "People and initiatives that care for the Canary Islands, but never find each other.", "Menschen und Initiativen, die sich um die Kanaren kümmern, sich aber nicht finden.", "Des personnes et des initiatives qui prennent soin des Canaries sans se trouver."),
 ("Una red colaborativa que las ponga en el mapa.", "A collaborative network that puts them on the map.", "Ein gemeinsames Netz, das sie auf die Karte bringt.", "Un réseau collaboratif qui les met sur la carte."),
 ("Mapa, agenda y red que conecta personas, colectivos e iniciativas.", "A map, calendar and network connecting people, groups and initiatives.", "Karte, Kalender und Netz, das Menschen, Gruppen und Initiativen verbindet.", "Carte, agenda et réseau qui relie personnes, collectifs et initiatives."),
 # Dossier
 ("El profesorado necesita decidir y preparar una visita escolar con toda la información a mano.", "Teachers need to decide on and plan a school visit with all the information to hand.", "Lehrkräfte müssen einen Schulbesuch mit allen Informationen zur Hand planen können.", "Les enseignants doivent décider et préparer une sortie scolaire avec toutes les informations sous la main."),
 ("Un dossier web claro, pensado para quien organiza la salida.", "A clear web dossier, designed for whoever organises the trip.", "Ein klares Web-Dossier für alle, die den Ausflug organisieren.", "Un dossier web clair, pensé pour qui organise la sortie."),
 ("Visita a la Reserva, el Museo y el Túnel de la Experiencia Histórica, con cuadernos por niveles y solicitud de fecha.", "A visit to the Reserve, the Museum and the Historical Experience Tunnel, with workbooks by level and date booking.", "Besuch des Reservats, des Museums und des Tunnels der historischen Erfahrung, mit Heften nach Stufen und Terminanfrage.", "Visite de la Réserve, du Musée et du Tunnel de l’expérience historique, avec cahiers par niveau et demande de date."),
 # Guías y materiales
 ("Los visitantes necesitan reconocer plantas, aves y polinizadores en el sendero.", "Visitors need to recognise plants, birds and pollinators along the trail.", "Besucher müssen Pflanzen, Vögel und Bestäuber am Weg erkennen können.", "Les visiteurs doivent reconnaître plantes, oiseaux et pollinisateurs sur le sentier."),
 ("Materiales imprimibles para preparar, vivir y recordar la visita.", "Printable materials to prepare for, enjoy and remember the visit.", "Druckbare Materialien, um den Besuch vorzubereiten, zu erleben und in Erinnerung zu behalten.", "Des supports imprimables pour préparer, vivre et se souvenir de la visite."),
 ("Guías de campo, mapa, cuadernos didácticos, concurso escolar y la galería «Cien años después».", "Field guides, a map, workbooks, a school competition and the gallery “Cien años después” (A hundred years later).", "Feldführer, Karte, Lernhefte, Schulwettbewerb und die Galerie „Cien años después“ (Hundert Jahre später).", "Guides de terrain, carte, cahiers pédagogiques, concours scolaire et la galerie « Cien años después » (Cent ans après)."),
 # Campañas de email
 ("Llegar a hoteles, colegios y agencias con un mensaje adaptado a cada uno.", "Reaching hotels, schools and agencies with a message tailored to each.", "Hotels, Schulen und Agenturen mit einer jeweils passenden Botschaft erreichen.", "Toucher hôtels, écoles et agences avec un message adapté à chacun."),
 ("Campañas de email propias para cada público y temporada.", "Dedicated email campaigns for each audience and season.", "Eigene E-Mail-Kampagnen für jede Zielgruppe und Saison.", "Des campagnes e-mail propres à chaque public et saison."),
 ("Plantillas de email con fotos, vídeo e iconos de la Reserva, organizadas por público, año y campaña.", "Email templates with photos, video and icons from the Reserve, organised by audience, year and campaign.", "E-Mail-Vorlagen mit Fotos, Video und Symbolen des Reservats, nach Zielgruppe, Jahr und Kampagne geordnet.", "Modèles d’e-mail avec photos, vidéo et icônes de la Réserve, classés par public, année et campagne."),
 # Sindical Federado
 ("Comités y secciones sindicales sin una web propia, sencilla y barata.", "Union committees and branches with no simple, affordable website of their own.", "Betriebsräte und Gewerkschaftsgruppen ohne eigene, einfache und günstige Website.", "Des comités et sections syndicales sans site propre, simple et bon marché."),
 ("Un sistema estático que cada sección configura y federa con las demás.", "A static system that each branch sets up and federates with the others.", "Ein statisches System, das jede Gruppe selbst einrichtet und mit den anderen verbindet.", "Un système statique que chaque section configure et fédère avec les autres."),
 ("Plataforma de código abierto con convenio, prevención y participación.", "An open-source platform covering agreements, health and safety, and participation.", "Open-Source-Plattform mit Tarifvertrag, Arbeitsschutz und Beteiligung.", "Plateforme open source avec convention collective, prévention et participation."),
 # TV-App
 ("Emitir un canal propio sin infraestructura de televisión.", "Running your own channel without TV infrastructure.", "Einen eigenen Sender ohne Fernsehinfrastruktur betreiben.", "Diffuser sa propre chaîne sans infrastructure de télévision."),
 ("Programar por horarios vídeos de plataformas que ya existen.", "Schedule videos from existing platforms by time slot.", "Videos bestehender Plattformen nach Sendeplan programmieren.", "Programmer à heures fixes des vidéos de plateformes existantes."),
 ("Motor de televisión web con YouTube, Vimeo y PeerTube.", "A web TV engine with YouTube, Vimeo and PeerTube.", "Web-TV-Engine mit YouTube, Vimeo und PeerTube.", "Moteur de télévision web avec YouTube, Vimeo et PeerTube."),
 # Open Play Network
 ("Reportes en la comunidad de Steam confusos o poco neutrales.", "Confusing or one-sided reports in the Steam community.", "Unklare oder wenig neutrale Meldungen in der Steam-Community.", "Des signalements confus ou peu neutres dans la communauté Steam."),
 ("Plantillas guiadas para redactarlos bien.", "Guided templates to write them well.", "Geführte Vorlagen, um sie gut zu formulieren.", "Des modèles guidés pour bien les rédiger."),
 ("Kit para seleccionar, revisar y copiar reportes claros y neutrales.", "A kit to choose, review and copy clear, neutral reports.", "Ein Kit, um klare, neutrale Meldungen auszuwählen, zu prüfen und zu kopieren.", "Un kit pour choisir, relire et copier des signalements clairs et neutres."),
 # Diez Claves
 ("La seguridad digital se explica con jerga y miedo, y casi nunca pensando en quien habla español.", "Digital security is explained with jargon and fear, and hardly ever with Spanish speakers in mind.", "Digitale Sicherheit wird mit Fachjargon und Angst erklärt und kaum je für Spanischsprachige.", "La sécurité numérique s’explique avec du jargon et de la peur, et presque jamais pour les hispanophones."),
 ("Explicarla en español llano, siempre en diez claves, con herramientas que no envían nada a nadie.", "Explain it in plain Spanish, always in ten keys, with tools that send nothing to anyone.", "Sie in einfachem Spanisch erklären, immer in zehn Schlüsseln, mit Werkzeugen, die nichts an niemanden senden.", "L’expliquer en espagnol simple, toujours en dix clés, avec des outils qui n’envoient rien à personne."),
 ("95 guías en 9 temas y un generador de contraseñas con ñ y tildes, que funciona en el navegador, sin cookies y con el código a la vista.", "95 guides across 9 topics and a password generator that handles ñ and accents, running in the browser, with no cookies and open code.", "95 Anleitungen in 9 Themen und ein Passwortgenerator mit ñ und Akzenten, der im Browser läuft, ohne Cookies und mit offenem Code.", "95 guides en 9 thèmes et un générateur de mots de passe avec ñ et accents, qui fonctionne dans le navigateur, sans cookies et au code ouvert."),
 # San Blas Experiencia Creativa
 ("El concurso artístico escolar necesita un espacio digital para mostrar las obras.", "The school art competition needs a digital space to show the work.", "Der Kunstwettbewerb der Schulen braucht einen digitalen Raum für die Werke.", "Le concours artistique scolaire a besoin d’un espace numérique pour montrer les œuvres."),
 ("Una galería online con acceso por QR para los participantes.", "An online gallery with QR access for participants.", "Eine Online-Galerie mit QR-Zugang für die Teilnehmenden.", "Une galerie en ligne avec accès par QR pour les participants."),
 ("Galería del concurso que une creatividad, memoria y territorio, sin datos personales de menores.", "A competition gallery bringing together creativity, memory and place, with no personal data from minors.", "Galerie des Wettbewerbs, die Kreativität, Erinnerung und Region verbindet, ohne personenbezogene Daten Minderjähriger.", "Galerie du concours qui unit créativité, mémoire et territoire, sans données personnelles de mineurs."),
 # PhoTown
 ("Las redes abiertas no sirven para aprender fotografía en confianza.", "Open social networks are no place to learn photography among people you trust.", "Offene Netzwerke eignen sich nicht, um im Vertrauen Fotografie zu lernen.", "Les réseaux ouverts ne permettent pas d’apprendre la photo en confiance."),
 ("Un «Instagram» de grupo cerrado: familia, clase o amigos.", "A closed-group “Instagram”: family, class or friends.", "Ein „Instagram“ für geschlossene Gruppen: Familie, Klasse oder Freunde.", "Un « Instagram » de groupe fermé : famille, classe ou amis."),
 ("Compartir fotos para aprender fotografía y conocerse dentro del grupo.", "Share photos to learn photography and get to know each other within the group.", "Fotos teilen, um Fotografie zu lernen und sich in der Gruppe kennenzulernen.", "Partager des photos pour apprendre la photo et se connaître au sein du groupe."),
 # Gofio Jornada
 ("Registrar la jornada laboral sin papeles ni hojas de cálculo.", "Recording working hours without paper or spreadsheets.", "Arbeitszeit erfassen, ohne Papier und Tabellen.", "Enregistrer le temps de travail sans papier ni tableur."),
 ("Una aplicación web que se use en segundos.", "A web app you can use in seconds.", "Eine Web-App, die in Sekunden bedient ist.", "Une application web qui s’utilise en quelques secondes."),
 ("Registro sencillo de entradas, salidas y horas trabajadas. En desarrollo.", "Simple logging of clock-ins, clock-outs and hours worked. In progress.", "Einfache Erfassung von Kommen, Gehen und Arbeitsstunden. In Arbeit.", "Enregistrement simple des arrivées, départs et heures travaillées. En cours."),
 # Akashicos
 ("El manual de sanación akáshica no se lleva a todas partes.", "The Akashic healing manual isn’t something you can carry everywhere.", "Das Handbuch der Akasha-Heilung hat man nicht überall dabei.", "Le manuel de guérison akashique ne se transporte pas partout."),
 ("Tener el manual siempre a mano, en el móvil.", "Keep the manual always to hand, on your phone.", "Das Handbuch immer griffbereit auf dem Handy.", "Avoir le manuel toujours sous la main, sur son téléphone."),
 ("Aplicación personal con acceso por cuenta; sin versión pública por ahora.", "A personal app with account access; no public version for now.", "Persönliche App mit Kontozugang; vorerst keine öffentliche Version.", "Application personnelle avec accès par compte ; pas de version publique pour l’instant."),
 # App de meditación
 ("<dd>En estudio.</dd>", "<dd>Under study.</dd>", "<dd>In Prüfung.</dd>", "<dd>À l’étude.</dd>"),
 ("Una aplicación de meditación, en fase de idea.", "A meditation app, at the idea stage.", "Eine Meditations-App, noch in der Ideenphase.", "Une application de méditation, au stade de l’idée."),
 ("Muy pronto, más detalles.", "More details soon.", "Bald mehr dazu.", "Plus de détails très bientôt."),
 # Enlace a las extensiones de Chrome
 ('<h2 id="h-extensiones">Extensiones para Chrome</h2>', '<h2 id="h-extensiones">Chrome extensions</h2>', '<h2 id="h-extensiones">Chrome-Erweiterungen</h2>', '<h2 id="h-extensiones">Extensions pour Chrome</h2>'),
 ("También hago pequeñas herramientas gratuitas para el navegador.", "I also make small free tools for the browser.", "Ich entwickle auch kleine kostenlose Werkzeuge für den Browser.", "Je crée aussi de petits outils gratuits pour le navigateur."),
 ('<a href="extensiones.html">Ver las extensiones →</a>', '<a href="extensions.html">See the extensions →</a>', '<a href="erweiterungen.html">Zu den Erweiterungen →</a>', '<a href="extensions-fr.html">Voir les extensions →</a>'),
]


def between(s, a, b):
    i = s.index(a); j = s.index(b, i) + len(b); return s[i:j]


def nav(lang):
    out = ['        <nav class="nav-lenguas" aria-label="%s">' % NAV[lang],
           '          <a class="volver" href="%s">%s</a>' % (HOME[lang], BACK[lang])]
    for i, l in enumerate(("es", "en", "de", "fr")):
        if i: out.append('          <span class="punto" aria-hidden="true">·</span>')
        attrs = ' hreflang="%s"' % l + ('' if l == lang else ' lang="%s"' % l) + (' aria-current="page"' if l == lang else '')
        out.append('          <a href="%s"%s>%s</a>' % (FILES[l], attrs, l.upper()))
    out.append('        </nav>')
    return "\n".join(out)


ALT = "".join('    <link rel="alternate" hreflang="%s" href="https://gofiodesign.eu/%s" />\n' % (l, FILES[l]) for l in ("es", "en", "de", "fr")) + \
      '    <link rel="alternate" hreflang="x-default" href="https://gofiodesign.eu/proyectos.html" />\n'

es = io.open("proyectos.html", encoding="utf-8").read()
es = re.sub(r'    <link rel="alternate" hreflang[^\n]*\n', "", es)
es = es.replace('    <meta property="og:type"', ALT + '    <meta property="og:type"', 1)

for lang in ("es", "en", "de", "fr"):
    s = es
    home = io.open(HOME[lang], encoding="utf-8").read()
    s = re.sub(r'        <nav class="nav-lenguas".*?</nav>', lambda m: nav(lang), s, count=1, flags=re.S)
    if lang != "es":
        k = ("en", "de", "fr").index(lang) + 1
        for row in T:
            assert row[0] in s, "falta: " + row[0][:60]
            s = s.replace(row[0], row[k])
        s = s.replace('<html lang="es">', '<html lang="%s">' % lang)
        s = s.replace('content="es_ES"', 'content="%s"' % LOCALE[lang])
        s = s.replace('<link rel="canonical" href="https://gofiodesign.eu/proyectos.html" />', '<link rel="canonical" href="https://gofiodesign.eu/%s" />' % FILES[lang])
        s = s.replace('<meta property="og:url" content="https://gofiodesign.eu/proyectos.html" />', '<meta property="og:url" content="https://gofiodesign.eu/%s" />' % FILES[lang])
        # piezas compartidas con la portada de ese idioma
        for a, b in (('    <a class="skip-link"', '</a>\n'), ('    <div id="cookie-banner"', '      </div>\n    </div>\n'),
                     ('    <footer class="pie">', '    </footer>\n')):
            s = s.replace(between(s, a, b), between(home, a, b))
        s = re.sub(r'<a class="boton-whatsapp".*?</a>', lambda m: re.search(r'<a class="boton-whatsapp".*?</a>', home, re.S).group(0), s, flags=re.S)
        s = re.sub(r'<a class="sello-gd".*?</a>', lambda m: re.search(r'<a class="sello-gd".*?</a>', home, re.S).group(0), s, count=1, flags=re.S)
        s = re.sub(r'(?<=<a class="sello-gd" href=")[^"]+', HOME[lang], s)
    title = re.search(r"<title>(.*?)</title>", s).group(1)
    ogdesc = re.search(r'property="og:description" content="([^"]*)"', s).group(1)
    blk = seo_lib.block(lang, FILES[lang], title, ogdesc, "assets/og/proyectos-%s.png" % lang, seo_lib.ALT_PROJ[lang], "CollectionPage")
    s = seo_lib.poner_bloque(s, blk)
    io.open(FILES[lang], "w", encoding="utf-8", newline="\n").write(s)
    print(lang, FILES[lang])
