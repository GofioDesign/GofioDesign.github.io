# Herramientas de generación

El sitio no tiene paso de compilación. Estos scripts escriben los HTML y los recursos de marca, y el resultado se sube al repositorio tal cual. Hay que ejecutarlos desde la raíz del repositorio con Python 3.

`datos/` guarda las piezas intermedias: los símbolos de las tres pintaderas y el logotipo en sus versiones principal y de 16 px.

## Cambiar texto de las portadas (index, en, de, fr)

Los textos de los cuatro idiomas están en `PAGES`, dentro de `portadas.py`. No edites los HTML a mano: se sobrescriben.

Si cambias `portada.css` o los favicons, sube `V_CSS` o `V_FAVICON` al principio de `portadas.py` para que los navegadores no usen la copia antigua. Las demás páginas llevan el mismo `?v=` escrito a mano.

```sh
python -I herramientas/portadas.py "$PWD" herramientas/datos/symbols.txt herramientas/datos/logo-inner.txt
```

## Añadir o cambiar un proyecto

1. Edita la ficha en `proyectos.html`, que es la versión española y la fuente de las demás.
2. Añade la traducción de cada texto nuevo a la lista `T` de `proyectos_i18n.py`. Cada fila es `(es, en, de, fr)`.
3. Genera `projects.html`, `projekte.html` y `projets.html`:

```sh
python -I herramientas/proyectos_i18n.py "$PWD"
```

Si falta una traducción, el script se detiene y muestra qué texto falta.

## SEO y Open Graph

`seo_lib.py` escribe Open Graph, la tarjeta de X/Twitter y el JSON-LD. `poner_bloque()` sustituye el bloque entero de la página, así que los scripts se pueden ejecutar las veces que haga falta sin duplicarlo. La descripción del estudio para el JSON-LD es `DESC_ORG`. Lo usan `portadas.py` y `proyectos_i18n.py`. Para el kit y privacidad:

```sh
python -I herramientas/seo_interiores.py "$PWD"
```

Imágenes OG (`assets/og/`): `og.py` escribe un HTML por imagen, que luego se rasteriza con Chrome sin ventana a 1200 × 630.

```sh
python -I herramientas/og.py "$PWD" <carpeta-temporal>
# por cada <carpeta-temporal>/og/NOMBRE.html:
chrome --headless=new --hide-scrollbars --allow-file-access-from-files --window-size=1200,630 \
  --virtual-time-budget=3000 --screenshot=assets/og/NOMBRE.png file:///<carpeta-temporal>/og/NOMBRE.html
```

## Marca

- `logo_sistema.py`: geometría del logotipo pintadera. Escribe `datos/logo-prop.txt` (principal) y `datos/logo-16.txt` (solo el GD) y una página de vista previa. Si cambia el logotipo, copia `logo-prop.txt` sobre `logo-inner.txt`.
  ```sh
  python -I herramientas/logo_sistema.py vista.html herramientas/datos/logo-prop.txt herramientas/datos/logo-16.txt
  ```
- `pintaderas.py`: imprime los tres símbolos (`python -I herramientas/pintaderas.py > herramientas/datos/symbols.txt`).
- `kit.py`: escribe los SVG de `assets/marca/`, el favicon (`assets/brand/favicon.svg`, el sello completo a sangre sobre barro) y los HTML para rasterizar `favicon.ico`, `favicon-16/32`, `apple-touch-icon` e `icon-192/512` con ese mismo dibujo.
  ```sh
  python -I herramientas/kit.py "$PWD" herramientas/datos
  ```
- `redes.py`: escribe el vertical con lema (`assets/marca/vertical-lema-*.svg`), los PNG de todos los logotipos (`assets/marca/png/`) y el avatar y las portadas de redes (`assets/marca/redes/`). El lema y el descriptor están arriba del script. Necesita `fonttools`, `brotli` y `cairosvg`. Después hay que rehacer el zip del kit.
  ```sh
  python -I herramientas/redes.py "$PWD"
  ```
- `tarjeta.py`: tarjeta de visita (SVG) en `assets/marca/tarjeta-visita/` y la ficha `juangonzalez.vcf`, que hay que copiar a `personal/`. Nombre, cargo, lema, descriptor y estilo del separador están arriba del script. Necesita `fonttools`, `brotli` y `segno`; el PNG y el PDF de imprenta se sacan con `cairosvg` y `pypdf`.
  ```sh
  python -I herramientas/tarjeta.py "$PWD" assets/marca/tarjeta-visita && mv assets/marca/tarjeta-visita/juangonzalez.vcf personal/
  ```
- `sello.py`: escribe el sello «Un proyecto Gofio Design» en `assets/sello/`. Necesita `fonttools` y `brotli`; conviene instalarlos en un entorno virtual.
  ```sh
  python -I herramientas/sello.py "$PWD" herramientas/datos
  ```
  **No cambies las rutas de `assets/sello/`.** Otras webs enlazan esos archivos directamente, y es así como el sello se actualiza solo.
