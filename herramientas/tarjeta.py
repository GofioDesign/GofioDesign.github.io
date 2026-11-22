# Tarjeta de visita Gofio Design, sistema pintadera (nov 2026).
# 85x55 mm + 3 mm de sangrado por lado. Unidad interna: 0,1 mm. Lienzo 910x610.
# Uso: python -I herramientas/tarjeta.py "$PWD" assets/marca/tarjeta-visita
# (luego: PNG y PDF de imprenta, ver herramientas/LEEME.md)
# Toma el logotipo y el título del kit de la web (assets/marca) y las fuentes de assets/fonts.
# Tintas planas, sin relieves ni sombras (normas de gofiodesign.eu/marca.html).
import os, re, sys
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
import segno

REPO, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

# Datos de contacto (cambiar aquí y volver a generar)
NOMBRE = 'Juan González'
CARGO = 'Dirección y ejecución de proyectos'
TEL = '+34 623 760 960'
EMAIL = 'hola@gofiodesign.eu'
WEB = 'gofiodesign.eu'
# El QR abre la ficha de contacto publicada en la web (se actualiza sin reimprimir la tarjeta)
VCF_URL = 'https://gofiodesign.eu/personal/juangonzalez.vcf'
# Lema y descriptor: propuesta en revisión (22 nov). Vacío = no se imprime.
LEMA = 'Cultivamos soluciones'
DESCRIPTOR = 'Proyectos y consultoría para la transformación ecosocial'

BARRO, HONDO, CREMA, MARRON, AMBAR = '#8B421E', '#59220D', '#EFE4CF', '#554242', '#E6B458'
W, H, B = 910, 610, 30          # lienzo y sangrado
S = B + 40                      # margen de seguridad: 4 mm dentro del corte

def fuente(n, peso=None):
    f = TTFont(f'{REPO}/assets/fonts/{n}')
    return instantiateVariableFont(f, {'wght': peso}) if peso else f
n4 = fuente('nunito-latin.woff2', 400)
n6 = fuente('nunito-latin.woff2', 600)
n7 = fuente('nunito-latin.woff2', 700)

def texto(t, size, ls, f):
    """Texto a trazos con línea base en y=0. Devuelve (d, ancho)."""
    x = 0; ds = []; cm = f.getBestCmap(); gs = f.getGlyphSet(); k = size / f['head'].unitsPerEm
    for ch in t:
        n = cm[ord(ch)]; pen = SVGPathPen(gs); rp = DecomposingRecordingPen(gs)
        gs[n].draw(rp); rp.replay(TransformPen(pen, (k, 0, 0, -k, x, 0)))
        ds.append(pen.getCommands()); x += f['hmtx'][n][0] * k + ls * size
    return ' '.join(c for c in ds if c), x - ls * size

def plano(d, x, y, fill):
    return f'<path d="{d}" transform="translate({x:.2f} {y:.2f})" fill="{fill}"/>'

def kit(nombre, x, y, w, color):
    """Incrusta un SVG del kit (logotipo, título) a la anchura w, con su tinta."""
    s = open(f'{REPO}/assets/marca/{nombre}.svg').read()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    h = w * vb[3] / vb[2]
    cuerpo = re.sub(r'^<svg[^>]*>|</svg>\s*$', '', s.strip())
    return (f'<svg x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" viewBox="{" ".join(map(str, vb))}" '
            f'color="{color}" overflow="visible">{cuerpo}</svg>'), h

def friso(y, color, alto=66, fino=True, girar=False):
    """Friso de dientes de sierra a sangre (módulo de assets/pintaderas/friso-fino.svg)."""
    k = alto / 22; paso = 32 * k; n = int(W / paso) + 2; x0 = (W - n * paso) / 2
    sw = 1.4 * k
    tri = ''.join(f'M{x0+i*paso:.2f} {y+17*k:.2f}L{x0+i*paso+16*k:.2f} {y+6*k:.2f}L{x0+(i+1)*paso:.2f} {y+17*k:.2f}'
                  f'M{x0+i*paso+8*k:.2f} {y+17*k:.2f}L{x0+i*paso+16*k:.2f} {y+11.5*k:.2f}L{x0+i*paso+24*k:.2f} {y+17*k:.2f}' for i in range(n))
    giro = f' transform="rotate(180 {W/2} {y + alto/2:.2f})"' if girar else ''   # dientes hacia abajo
    return (f'<g fill="none" stroke="{color}" stroke-width="{sw:.2f}" stroke-linejoin="round" stroke-linecap="round"{giro}>'
            f'<path d="M0 {y+1.5*k:.2f}H{W}M0 {y+20.5*k:.2f}H{W}"/><path d="{tri}"/></g>')

def svg(cuerpo, etiqueta, guias=False):
    g = ''
    if guias:   # corte (ámbar) y margen de seguridad (azul), solo para revisar
        g = (f'<rect x="{B}" y="{B}" width="{W-2*B}" height="{H-2*B}" fill="none" stroke="#00A3FF" stroke-width="2" stroke-dasharray="8 6"/>'
             f'<rect x="{S}" y="{S}" width="{W-2*S}" height="{H-2*S}" fill="none" stroke="#FF3D9A" stroke-width="1.2" stroke-dasharray="4 6"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="91mm" height="61mm" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{etiqueta}">{cuerpo}{g}</svg>\n')

# ---------- ANVERSO: barro, pintadera y título en crema, friso abajo ----------
def anverso(guias=False):
    p = [f'<rect width="{W}" height="{H}" fill="{BARRO}"/>']
    fr_alto = 40; fr_y = H - B - 22 - fr_alto          # friso dentro del margen, sobre el corte
    lw = 210; tw = 470; aire = 46
    _, lh = kit('logotipo-crema', 0, 0, lw, CREMA); _, th = kit('titulo-crema', 0, 0, tw, CREMA)
    gsz = 30; lema = texto(LEMA, gsz, 0.02, n6) if LEMA else None
    extra = (34 + gsz * 0.72) if lema else 0
    if lema: lw = 180
    _, lh = kit('logotipo-crema', 0, 0, lw, CREMA)
    arriba = B + 22 + 40; bloque = lh + aire + th + extra; y0 = arriba + (fr_y - arriba - bloque) / 2
    p.append(kit('logotipo-crema', (W - lw) / 2, y0, lw, CREMA)[0])
    p.append(kit('titulo-crema', (W - tw) / 2, y0 + lh + aire, tw, CREMA)[0])
    if lema:
        p.append(plano(lema[0], (W - lema[1]) / 2, y0 + lh + aire + th + extra, CREMA))
    p.append(friso(fr_y, CREMA, fr_alto, girar=True))   # la de abajo, girada 180°
    p.append(friso(B + 22, CREMA, 40))
    return svg(''.join(p), 'Tarjeta Gofio Design, anverso', guias)

# ---------- REVERSO: crema, tinta marrón, datos y QR ----------
VCARD = ('BEGIN:VCARD\r\nVERSION:3.0\r\n'
         f'N:González;Juan;;;\r\nFN:{NOMBRE}\r\nORG:Gofio Design\r\nTITLE:{CARGO}\r\nNOTE:{LEMA}. {DESCRIPTOR}.\r\n'
         f'TEL;TYPE=CELL:{TEL.replace(" ", "")}\r\nEMAIL:{EMAIL}\r\nURL:https://{WEB}\r\nEND:VCARD\r\n')

def qr(x, y, lado, color):
    q = segno.make(VCF_URL, error='m', boost_error=False)
    m = [list(r) for r in q.matrix]; n = len(m); zona = 2
    k = lado / (n + 2 * zona); d = []
    for j, fila in enumerate(m):
        i = 0
        while i < n:
            if fila[i]:
                i0 = i
                while i < n and fila[i]: i += 1
                d.append(f'M{x+(zona+i0)*k:.2f} {y+(zona+j)*k:.2f}h{(i-i0)*k:.2f}v{k:.2f}h{-(i-i0)*k:.2f}z')
            else: i += 1
    return f'<path d="{"".join(d)}" fill="{color}"/>', q.version, k


def rombos(x, y, ancho, alto, color):
    """Separador fino: los dientes de la cenefa sin las rectas de los bordes, unidos a su reflejo:
    una línea de rombos partidos por una recta central."""
    cy = y + alto / 2
    g = 5.2                    # separación de cada mitad respecto a la recta: 0,36 mm de aire entre trazos
    a = alto / 2; ai = (a - g) * 0.5 + g
    # misma pendiente que los dientes de la cenefa (11 de alto por 16 de medio paso)
    paso = 2 * (a - g) * 16 / 11; n = max(1, round(ancho / paso)); paso = ancho / n
    d = [f'M{x:.2f} {cy:.2f}H{x + ancho:.2f}']
    for sgn in (-1, 1):
        b = cy + sgn * g       # base de esta mitad, despegada de la recta
        d.append('M' + ' '.join(f'{x + i * paso / 2:.2f} {(cy + sgn * a) if i % 2 else b:.2f}' for i in range(2 * n + 1)))
        for i in range(n):   # chevrón interior
            m = x + i * paso + paso / 2
            d.append(f'M{m - paso / 4:.2f} {b:.2f}L{m:.2f} {cy + sgn * ai:.2f}L{m + paso / 4:.2f} {b:.2f}')
    return (f'<path d="{" ".join(d)}" fill="none" stroke="{color}" stroke-width="1.6" '
            f'stroke-linejoin="round" stroke-linecap="round"/>')


# Estilos de separador central. SEPARADOR elige uno: 'rombos', 'linea-rombo', 'rombos-sueltos', 'zigzag', 'circulos'
SEPARADOR = 'linea-rombo'


def separador(estilo, x, y, ancho, alto, color):
    cy = y + alto / 2; sw = 1.6
    lin = f'fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'
    if estilo == 'rombos':
        return rombos(x, y, ancho, alto, color)
    if estilo == 'linea-rombo':      # recta fina con un rombo en el centro, como un broche
        r = alto * 0.42; m = x + ancho / 2; h = 9
        return (f'<path d="M{x:.2f} {cy:.2f}H{m - r - h:.2f}M{m + r + h:.2f} {cy:.2f}H{x + ancho:.2f}" {lin}/>'
                f'<path d="M{m:.2f} {cy - r:.2f}L{m + r:.2f} {cy:.2f}L{m:.2f} {cy + r:.2f}L{m - r:.2f} {cy:.2f}Z" {lin}/>'
                f'<path d="M{m:.2f} {cy - r*0.45:.2f}L{m + r*0.45:.2f} {cy:.2f}L{m:.2f} {cy + r*0.45:.2f}L{m - r*0.45:.2f} {cy:.2f}Z" fill="{color}"/>')
    if estilo == 'rombos-sueltos':   # fila de rombos macizos pequeños, sin línea
        r = alto * 0.2; paso = r * 5; n = int(ancho // paso); x0 = x + (ancho - (n - 1) * paso) / 2
        return ''.join(f'<path d="M{x0+i*paso:.2f} {cy - r:.2f}l{r:.2f} {r:.2f}l{-r:.2f} {r:.2f}l{-r:.2f} {-r:.2f}Z" fill="{color}"/>' for i in range(n))
    if estilo == 'zigzag':           # un solo diente de sierra fino, misma pendiente que la cenefa
        a = alto * 0.22; paso = 2 * a * 2 * 16 / 11; n = max(1, round(ancho / paso)); paso = ancho / n
        pts = ' '.join(f'{x + i * paso / 2:.2f} {cy + (-a if i % 2 else a):.2f}' for i in range(2 * n + 1))
        return f'<path d="M{pts}" {lin}/>'
    if estilo == 'circulos':         # recta con círculos concéntricos espaciados (el motivo del friso)
        r = alto * 0.3; paso = ancho / 6; d = []; xs = [x + paso * (i + 0.5) for i in range(6)]
        xa = x
        for c in xs:
            d.append(f'M{xa:.2f} {cy:.2f}H{c - r - 6:.2f}'); xa = c + r + 6
        d.append(f'M{xa:.2f} {cy:.2f}H{x + ancho:.2f}')
        circ = ''.join(f'<circle cx="{c:.2f}" cy="{cy:.2f}" r="{r:.2f}" {lin}/><circle cx="{c:.2f}" cy="{cy:.2f}" r="{r*0.35:.2f}" fill="{color}"/>' for c in xs)
        return f'<path d="{" ".join(d)}" {lin}/>' + circ
    raise ValueError(estilo)


# Iconos de línea sobrios (caja 24x24, trazo), para teléfono, correo y web
ICONOS = {
    'tel': '<path d="M6.6 3.5h2.8l1.4 4-2 1.4a12 12 0 0 0 6.3 6.3l1.4-2 4 1.4v2.8a2 2 0 0 1-2 2A17 17 0 0 1 4.6 5.5a2 2 0 0 1 2-2Z"/>',
    'correo': '<rect x="3" y="5.5" width="18" height="13" rx="1.5"/><path d="M3.6 6.6 12 13l8.4-6.4"/>',
    'web': '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="3.8" ry="9"/><path d="M3 12h18M4.6 7.5h14.8M4.6 16.5h14.8"/>',
}


def icono(nombre, x, y, lado, color):
    return (f'<svg x="{x:.2f}" y="{y:.2f}" width="{lado}" height="{lado}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONOS[nombre]}</svg>')


def reverso(guias=False):
    """Crema con tinta marrón. Cenefas arriba y abajo (a sangre); la empresa ocupa el tercio superior,
    una línea de rombos parte la cara en 1/3 y 2/3, y abajo va la persona con el QR a la derecha."""
    p = [f'<rect width="{W}" height="{H}" fill="{CREMA}"/>']
    fa = 40                                   # alto de las cenefas de cierre
    p.append(friso(B + 22, MARRON, fa))
    p.append(friso(H - B - 22 - fa, MARRON, fa, girar=True))   # la de abajo, girada 180°
    arriba, abajo = B + 22 + fa, H - B - 22 - fa             # franja útil entre cenefas
    sep_alto = 24
    sy = arriba + (abajo - arriba) / 3 - sep_alto / 2        # separador en el tercio
    # --- tercio superior: pintadera, título y descriptor, centrados en el ancho útil ---
    lw = 102; tw = 350; gap = 28
    th = tw * 120 / 682
    x0 = S + ((W - 2 * S) - (lw + gap + tw)) / 2
    ly = arriba + (sy - arriba - lw) / 2
    p.append(kit('logotipo-marron', x0, ly, lw, MARRON)[0])
    tx = x0 + lw + gap
    bloque = th * 0.86 + 12 + 2 * 22                        # título (sin el aire de su caja) y dos líneas
    ty = ly + (lw - bloque) / 2 - th * 0.08
    p.append(kit('titulo-marron', tx - tw * 0.03, ty, tw, MARRON)[0])
    if DESCRIPTOR:
        palabras = DESCRIPTOR.split(); corte = len(palabras) // 2
        cx = tx - tw * 0.03 + tw / 2                        # centro del título
        for k, trozo in enumerate((' '.join(palabras[:corte]), ' '.join(palabras[corte:]))):
            dd, dw = texto(trozo, 17, 0.01, n4)
            p.append(plano(dd, cx - dw / 2, ty + th + 14 + k * 22, MARRON))
    # --- separador a todo el ancho útil ---
    p.append(separador(SEPARADOR, S, sy, W - 2 * S, sep_alto, MARRON))
    # --- dos tercios inferiores: persona a la izquierda, QR abajo a la derecha ---
    lado = 220; qx = W - S - lado; qy = abajo - 14 - lado
    cod, ver, mod = qr(qx, qy, lado, MARRON); p.append(cod)
    base = qy + 34
    nd, _ = texto(NOMBRE, 38, 0.005, n7); p.append(plano(nd, S, base, MARRON))
    cd, _ = texto(CARGO, 24, 0.01, n4);   p.append(plano(cd, S, base + 38, MARRON))
    for i, (ic, val) in enumerate((('tel', TEL), ('correo', EMAIL), ('web', WEB))):
        y = base + 98 + i * 38
        p.append(icono(ic, S - 1, y - 21, 24, BARRO))
        vd, _ = texto(val, 24, 0.005, n4); p.append(plano(vd, S + 36, y, MARRON))
    print(f'QR versión {ver}, módulo {mod/10:.2f} mm; separador en y={sy:.0f}, QR {qy:.0f}-{qy+lado:.0f}, última línea {y:.0f} (cenefa en {abajo})')
    return svg(''.join(p), 'Tarjeta Gofio Design, reverso', guias)


for n, f in (('anverso', anverso), ('reverso', reverso)):
    open(f'{OUT}/tarjeta-{n}.svg', 'w').write(f())
    open(f'{OUT}/tarjeta-{n}-guias.svg', 'w').write(f(guias=True))
open(f'{OUT}/juangonzalez.vcf', 'w', newline='').write(VCARD)   # subir a gofiodesign.eu/personal/
print('ok', OUT)
