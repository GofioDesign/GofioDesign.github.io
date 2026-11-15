import math
f = lambda v: f"{v:.1f}".rstrip('0').rstrip('.')
# Cuadrado dual: cuadrado, borde interior, doble diagonal, mitad inferior derecha con trama de puntos
dots = []
for y in range(40, 101, 8):
    for x in range(40, 101, 8):
        if x + y >= 148 and x <= 100 and y <= 100:
            dots.append(f'<circle cx="{x}" cy="{y}" r="1.9"/>')
cuadrado = ('<symbol id="p-cuadrado" viewBox="0 0 120 120">'
  '<g fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round">'
  '<rect x="6" y="6" width="108" height="108" rx="5"/><rect x="16" y="16" width="88" height="88" rx="2"/>'
  '<path d="M16 104 104 16M28 104 104 28"/></g>'
  '<g fill="currentColor">' + ''.join(dots) + '</g></symbol>')
# Circulo de la unidad: anillos, corona de trazos oblicuos, centro
ticks = []
for i in range(28):
    a = 2 * math.pi * i / 28; b = a + math.radians(14)
    x1, y1 = 60 + 43 * math.cos(a), 60 + 43 * math.sin(a)
    x2, y2 = 60 + 51 * math.cos(b), 60 + 51 * math.sin(b)
    ticks.append(f'M{f(x1)} {f(y1)} {f(x2)} {f(y2)}')
circulo = ('<symbol id="p-circulo" viewBox="0 0 120 120">'
  '<g fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">'
  '<circle cx="60" cy="60" r="54"/><circle cx="60" cy="60" r="40"/>'
  f'<path d="{" ".join(ticks)}"/>'
  '<circle cx="60" cy="60" r="27"/><circle cx="60" cy="60" r="16"/></g>'
  '<circle cx="60" cy="60" r="5" fill="currentColor"/></symbol>')
# Triangulo divino: triangulo con bandas horizontales y triangulo invertido liso en el centro
segs = []
for y in range(23, 98, 7):
    hw = (y - 10) / 90 * 52 - 4.5
    if hw <= 2: continue
    L, R = 60 - hw, 60 + hw
    if y > 55:
        ihw = (100 - y) / 45 * 26 + 4.5
        if L < 60 - ihw: segs.append(f'M{f(L)} {y}H{f(60 - ihw)}')
        if 60 + ihw < R: segs.append(f'M{f(60 + ihw)} {y}H{f(R)}')
    elif y < 51:
        segs.append(f'M{f(L)} {y}H{f(R)}')
triangulo = ('<symbol id="p-triangulo" viewBox="0 0 120 120">'
  '<g fill="none" stroke="currentColor" stroke-linejoin="round">'
  '<path stroke-width="2.5" d="M60 8 113 101H7Z"/><path stroke-width="2.5" d="M34 55H86L60 101Z"/>'
  f'<path stroke-width="1.8" stroke-linecap="round" d="{"".join(segs)}"/></g></symbol>')
print(cuadrado); print(circulo); print(triangulo)
