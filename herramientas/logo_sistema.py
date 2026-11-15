import math, sys, io
f = lambda v: ("%.3f" % v).rstrip("0").rstrip(".")
sq = math.sqrt


def letters(R, w, split, bar_x, bar_y=62):
    """G como silueta cerrada (corte superior vertical a 90º) y D en trazo; ambas con banda w."""
    xr = 60 + split / 2
    Ro, Ri = R + w / 2, R - w / 2
    x_edge = 60 - split / 2 + w / 2
    xw = x_edge - w
    top_o = 60 - sq(Ro ** 2 - (60 - x_edge) ** 2); bot_o = 60 + sq(Ro ** 2 - (60 - x_edge) ** 2)
    top_i = 60 - sq(Ri ** 2 - (60 - x_edge) ** 2); bot_i = 60 + sq(Ri ** 2 - (60 - xw) ** 2)
    G = ("M%s %sA%s %s 0 0 0 %s %sV%sH%sV%sH%sV%sA%s %s 0 0 1 %s %sZ"
         % (f(x_edge), f(top_o), f(Ro), f(Ro), f(x_edge), f(bot_o), f(bar_y - w / 2), f(bar_x), f(bar_y + w / 2),
            f(xw), f(bot_i), f(Ri), f(Ri), f(x_edge), f(top_i)))
    h = sq(R ** 2 - (split / 2) ** 2)
    D = "M%s %sA%s %s 0 0 1 %s %sZ" % (f(xr), f(60 - h), f(R), f(R), f(xr), f(60 + h))
    return ('<path d="%s" fill="currentColor"/><path d="%s" fill="none" stroke="currentColor" stroke-width="%s" stroke-linejoin="miter"/>'
            % (G, D, f(w)))


def sierra(lw, w, gap=5.0, r_out=56.5, n=26):
    """Versión principal. lw: línea del anillo; banda de dientes = w (trazo de las letras)."""
    r_in = r_out - w
    zig = []
    for i in range(2 * n + 1):
        a = math.pi * i / n - math.pi / 2
        r = r_out if i % 2 else r_in
        zig.append("%s %s" % (f(60 + r * math.cos(a)), f(60 + r * math.sin(a))))
    ring = ('<g fill="none" stroke="currentColor" stroke-width="%s" stroke-linejoin="round">'
            '<circle cx="60" cy="60" r="%s"/><circle cx="60" cy="60" r="%s"/><path d="M%s"/></g>'
            % (f(lw), f(r_out), f(r_in), " ".join(zig)))
    R = (r_in - lw / 2) - gap - w / 2
    split = gap + w
    bar_x = 60 - split / 2 + w / 2 - 0.5 * (R + w / 2)
    return ring + letters(R, w, split, bar_x)


def pequeno(lw=8.5 / 4, w=8.5, gap=5.0, r_out=56.5):
    """16 px: solo el GD, sin dientes ni anillo. Son las letras de la versión principal escaladas
    hasta llenar el cuadrado, así que trazo y separación guardan la misma proporción."""
    r_in = r_out - w
    R = (r_in - lw / 2) - gap - w / 2
    k = 60 / (R + w / 2)
    R2, w2, gap2 = R * k, w * k, gap * k
    split = gap2 + w2
    bar_x = 60 - split / 2 + w2 / 2 - 0.5 * (R2 + w2 / 2)
    return letters(R2, w2, split, bar_x, bar_y=60 + 2 * k)


# Actual (antes de esta ronda), para comparar
def actual():
    n = 26; r_in, r_out = 47, 56.5
    zig = []
    for i in range(2 * n + 1):
        a = math.pi * i / n - math.pi / 2
        r = r_out if i % 2 else r_in
        zig.append("%s %s" % (f(60 + r * math.cos(a)), f(60 + r * math.sin(a))))
    ring = ('<g fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round">'
            '<circle cx="60" cy="60" r="56.5"/><circle cx="60" cy="60" r="47"/><path d="M%s"/></g>' % " ".join(zig))
    return ring + letters(36.65, 8.5, 13.5, 38.5)


principal = sierra(lw=8.5 / 4, w=8.5)
chico = pequeno()

if len(sys.argv) > 2:
    io.open(sys.argv[2], "w", encoding="utf-8").write(principal)
    io.open(sys.argv[3], "w", encoding="utf-8").write(chico)

S = lambda body, s: '<svg viewBox="0 0 120 120" width="%d" height="%d">%s</svg>' % (s, s, body)
row = lambda body, small: "".join(S(body, s) for s in (240, 48, 32)) + S(small, 16) + '<span class="claro">%s</span>' % S(small, 16) + '<span class="claro">%s</span>' % S(body, 48)
html = '''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Logotipo proporciones</title>
<style>body{margin:0;padding:32px;background:#8b421e;color:#efe4cf;font-family:Nunito,system-ui,sans-serif}
h2{font-weight:700;font-size:1.1rem;margin:28px 0 12px}p{max-width:70ch}
.fila{display:flex;align-items:center;gap:28px;flex-wrap:wrap}.claro{background:#efe4cf;color:#554242;padding:8px;border-radius:6px;display:inline-block}
svg{display:block}.zoom svg{image-rendering:pixelated}</style></head><body>
<h1 style="font-weight:400">Proporciones del logotipo</h1>
<h2>Antes · línea 2,2 · letras 8,5 · banda de dientes 9,5</h2><div class="fila">%s</div>
<h2>Proporcional · línea 2,125 · letras 8,5 (= 4 líneas) · banda de dientes 8,5 (= trazo de las letras)</h2><div class="fila">%s</div>
<h2>Versión de 16 px: solo el GD, con el trazo proporcional · tamaño real y ampliada ×8</h2>
<div class="fila">%s%s<span class="claro">%s</span></div>
<p>Las letras de la versión principal escaladas hasta llenar el cuadrado: el trazo sigue siendo el 10 %% del diámetro de las letras y la separación entre G y D crece en la misma proporción.</p>
</body></html>''' % (row(actual(), chico), row(principal, chico), S(chico, 16), S(chico, 128), S(chico, 128))
io.open(sys.argv[1], "w", encoding="utf-8").write(html)
print("ok")
