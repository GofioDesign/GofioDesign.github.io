# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Tres públicos con el mismo peso, todos en Tenerife o con interés en Canarias, y la web debe servirlos sin priorizar ninguno:

- **Pymes y profesionales de la isla** que necesitan web, marca o infraestructura técnica y buscan un estudio cercano al que puedan llamar por WhatsApp.
- **Entidades públicas, reservas ambientales y centros educativos** (ayuntamientos, reservas, colegios) que encargan dinamización, interpretación del patrimonio, dossieres y materiales didácticos.
- **Comunidades de vecinos y particulares** que necesitan jardines con flora autóctona, redes domésticas o TV colectiva.

El visitante llega normalmente desde una búsqueda local o desde un enlace en una web hecha por el estudio. Su trabajo es decidir si Gofio Design es el estudio adecuado para su encargo y contactar.

## Product Purpose

Sitio web estático y multilingüe (ES principal, EN, DE, FR) del estudio Gofio Design, publicado en gofiodesign.eu (GitHub Pages). Presenta los servicios del estudio en tres capas (identidad e infraestructura digital; paisaje y territorio canario; gestión de activos y dinamización), muestra los proyectos realizados y ofrece el kit de marca descargable. Éxito: que un visitante de cualquiera de los tres públicos entienda qué hace el estudio, vea trabajo real comparable al suyo y contacte.

## Positioning

Cuatro pilares confirmados por el usuario, y el concepto de cualquier superficie debe sostenerse en los cuatro:

1. **Raíz canaria.** Veinte años de trabajo en Tenerife (desde 2005) con arraigo real: flora autóctona, territorio insular, oficios y cultura de la isla, mercado local y europeo. Un vecino recién llegado no puede afirmar esa trayectoria ni ese arraigo.
2. **Compromiso con las cosas bien hechas.** El estudio se define por el oficio y el acabado, no por la velocidad ni el volumen. Esto es lo que el visitante debe percibir antes de leer una sola línea.

3. **Conocimiento en múltiples campos.** Un solo estudio que domina identidad digital, redes, paisaje, patrimonio, eventos y eficiencia energética, y que cruza esos campos en cada encargo. No es una agencia web ni un paisajista: es un estudio de intervención interdisciplinar.

4. **Accesibilidad universal.** No es un requisito técnico que se cumple al final: es parte de la identidad del estudio. Una dirección visual que solo funciona para quien ve bien, lee rápido o usa ratón queda descartada, por atractiva que sea.

El método Problema · Idea · Plan · Hecho es el procedimiento que une los cuatro pilares y apoya al concepto, pero no los sustituye.

## Operating Context

- Estudio unipersonal fundado en 2005 por Juan Alberto González Rodríguez (Fasnia, Tenerife): graduado en Bellas Artes por la Universidad de La Laguna; desarrollador web, diseñador digital, coordinador de proyectos, educador ambiental y soporte informático L1/L2. Vivió más de cuatro años en Alemania y otros tantos en Francia; trabaja en español, inglés, alemán y francés, y de ahí las cuatro versiones del sitio. Fuente: `Profile.pdf` (CV, en la raíz del repo, no publicar).
- Campos reales que cruza el estudio, todos con trabajo demostrable: desarrollo web e identidad digital; gestión de dominios y DNS (16 dominios); instalación y certificación de redes de datos en oficinas, alojamientos turísticos y viviendas; educación e interpretación ambiental, histórica y cultural; gestión de patrimonio (prácticas en CICOP, La Laguna); coordinación de proyectos comunitarios (cofundador de PROYECT4 y de la Asociación La Destiladera); email marketing; soporte informático internacional (Atos, cuenta WSP, 2018–2020).
- El contacto principal es WhatsApp (+34 623 760 960) y un correo ofuscado por JavaScript en el pie.
- El sitio aloja además, bajo el mismo dominio, varias webs de clientes y proyectos (`/clinicadentaldharma_v2/`, `/sindical-federado/`, `/TV-App/`, `/OpenPlayNetwork/`), enlazadas desde la página de proyectos.
- Cada proyecto se documenta con la ficha Problema · Idea · Concepto, que es el método de trabajo del estudio y aparece también en los proyectos en desarrollo.
- Analítica con Google Tag Manager (GTM-55DKZ9C5) y banner de cookies con aceptar/rechazar; página legal cuatrilingüe en `privacy.html`.
- Despliegue: GitHub Pages con CNAME `gofiodesign.eu`; cache-busting manual del CSS mediante `?v=` en cada HTML.

## Capabilities and Constraints

- Stack existente: HTML, CSS y JavaScript sin framework ni proceso de build; Google Fonts (Nunito, Poiret One), Font Awesome 6 por CDN, fuente propia `gd-glifos.woff2` solo para la G y la D.
- Cuatro versiones de idioma como archivos independientes (`index.html`, `en.html`, `de.html`, `fr.html`) con `hreflang` cruzado; cualquier cambio en la portada debe replicarse en los cuatro.
- Páginas: portada, proyectos, kit de marca, legal/privacidad. Sitemap y robots mantenidos a mano.
- Compromiso de accesibilidad WCAG 2.2 AA ya trabajado (contraste, landmarks, encabezados, foco).
- **Cifras pendientes de revisión:** el meta description y los títulos de la portada afirman «hasta un 70 % menos en la factura de agua», «redes Omada» y «TV satélite colectiva con 5 años de garantía». El usuario indica que deben confirmarse o retirarse; el trabajo futuro no debe repetirlas como hechos hasta que se confirmen, ni inventar otras.
- **Decisión del 13 nov 2026:** la portada y el kit de marca dejan de llevar tagline y línea de método. «Curiosidad natural» y «Del problema a la idea, de la idea al concepto» se retiran; bajo el nombre no va ninguna frase. Los SVG del kit que incluyen el tagline (logotipos horizontales y verticales, OG) quedan pendientes de regenerar sin él.
- **Fichas de proyecto:** el método se muestra en cuatro pasos, Problema · Idea · Plan · Hecho, en lugar de Problema · Idea · Concepto. En proyectos en desarrollo, Hecho queda abierto y se dice.
- Terminología fija: nombres de las tres capas de servicio tal como figuran en la portada.

## Brand Commitments

- Nombre: Gofio Design. Tagline: «Curiosidad natural» (EN Natural curiosity · FR Curiosité naturelle · DE Natürliche Neugier).
- Kit de marca publicado en `marca.html` y `assets/marca/`, con normas de uso explícitas que el usuario ha hecho públicas y por tanto vinculantes: monograma GD en relieve sobre fondo claro y en hueco sobre fondo oscuro; título «GOFIO DESIGN» en hueco sobre claro y en relieve sobre oscuro; versiones planas o tinta marrón cuando el nombre tenga que leerse como texto.
- Paleta oficial: crema #EFE4CF (fondo), beige #E6D7BA (capas), arena #C9AE80 (líneas y relieve), marrón #554242 (títulos, nav, pie), ámbar #E6B458 (acento, nunca para texto), texto #4A3F35.
- Tipografía oficial: Poiret One con los glifos propios G y D para títulos; Nunito para texto.
- Activos: `assets/brand/` (favicons, sello, OG image) y `assets/marca/` (logotipos horizontales y verticales, monogramas, título, icono de app, OG en SVG, zip completo).
- Voz: castellano directo, frases cortas, sin anglicismos innecesarios; tono cercano y profesional.

## Evidence on Hand

- Doce proyectos publicados con captura en `assets/projects/` y enlace vivo: Clínica Dental Dharma, Mi Terapia Regresiva, Canarias.africa, Macaronesico, Archipiélago Vivo, San Blas Reserva Ambiental (dossier de visitas escolares, guías y materiales), campañas de email, Sindical Federado, TV-App, Open Play Network, Diez Claves. El usuario confirma que son reales.
- Cinco proyectos en desarrollo con ficha Problema · Idea · Concepto: San Blas Experiencia Creativa, PhoTown, Gofio Jornada, Akashicos, app de meditación.
- Trayectoria desde 2005 (pie de página «© 2005–2026»); primer proyecto web villapipol.com.
- **Cifras verificadas por el CV, utilizables como prueba:** en la Reserva Ambiental San Blas, las campañas de email a centros educativos aumentaron las reservas escolares un 65,4 %, los participantes un 103,5 % y los ingresos un 97,4 % entre los cursos 2024–25 y 2025–26. Son resultados de un trabajo del estudio (campañas de email, listadas en proyectos) y pueden citarse con esa atribución.
- Otros hechos citables: coordinación de la II Tenerife Sustainable Fashion Week (Universidad de La Laguna); campaña de ahorro energético con reparto de kits de eficiencia (PROYECT4); señalética, web y bebedero de aves homologado en renaturalización costera con el Ayuntamiento de Arafo; guía de aves de la Reserva Ambiental San Blas.
- **Ausencias que no deben fabricarse:** no hay testimonios de clientes, cifras de resultados verificadas, premios ni prensa. Las cifras actuales del meta están en revisión (ver Capabilities and Constraints).

## Product Principles

1. **Tres públicos, una puerta.** Pyme, entidad pública y particular deben reconocerse en la portada sin que ninguno quede relegado.
2. **Mostrar trabajo real antes que prometer.** Los proyectos publicados son la prueba; nada de cifras ni testimonios que no existan.
3. **Veinte años en la isla.** La trayectoria y el arraigo canario son el argumento de confianza y deben ser legibles, no decorativos.
4. **Un cambio, cuatro idiomas.** Toda decisión de portada se diseña sabiendo que vive en ES, EN, DE y FR a la vez.
5. **El kit de marca manda.** Las normas publicadas de relieve, hueco, paleta y tipografía son el límite de cualquier trabajo visual.

## Accessibility & Inclusion

La accesibilidad universal es un pilar del posicionamiento (ver Positioning). Mínimo WCAG 2.2 AA en todo el sitio: contraste de 4,5:1 en texto normal y 3:1 en texto grande, landmarks, jerarquía de encabezados, foco visible, navegación completa por teclado, respeto a `prefers-reduced-motion`, textos alternativos reales y tamaños legibles en móvil. Los efectos de relieve y hueco de la marca no se usan para texto que deba leerse; en ese caso, versiones planas o tinta marrón. Las tipografías de píxel, las tramas sobre texto y los fondos con textura bajo texto corrido quedan fuera salvo en títulos grandes con contraste comprobado.
