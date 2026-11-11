"""Valida la granja generada y escribe un informe legible.

Comprueba tamaño, pozo de caída, cadena de tolvas, entidades, luces en la
plataforma, simetría y recuento de materiales.
"""
import collections
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(RAIZ, 'tools'))

import nbt  # noqa: E402
import granja  # noqa: E402

SALIDA = os.path.join(RAIZ, 'salida')
RUTA = os.path.join(RAIZ, 'estructuras', 'granja_enderman_v2.mcstructure')
C = granja.C

DIRS = {
    0: (0, -1, 0), 1: (0, 1, 0), 2: (0, 0, -1),
    3: (0, 0, 1), 4: (-1, 0, 0), 5: (1, 0, 0),
}
LUCES = {
    'minecraft:glowstone', 'minecraft:sea_lantern', 'minecraft:torch',
    'minecraft:lantern', 'minecraft:end_rod', 'minecraft:shroomlight',
    'minecraft:jack_o_lantern', 'minecraft:campfire', 'minecraft:lava',
}


def cargar(ruta):
    b = open(ruta, 'rb').read()
    root = nbt.read(b)
    sx, sy, sz = root['size']
    s = root['structure']
    d = s['palette']['default']
    pal = d['block_palette']
    nombres = [p['name'] for p in pal]
    estados = [p.get('states', {}) for p in pal]
    idx = s['block_indices'][0]

    def bloque(x, y, z):
        i = idx[x * sy * sz + y * sz + z]
        return ('minecraft:air', {}) if i < 0 else (nombres[i], estados[i])

    return dict(root=root, sx=sx, sy=sy, sz=sz, s=s, bloque=bloque, idx=idx,
                nombres=nombres, estados=estados, pal=pal)


def main():
    if not os.path.exists(RUTA):
        print('Falta la estructura; ejecuta antes build/construir.py')
        return 1
    e = cargar(RUTA)
    sx, sy, sz, bloque, s = e['sx'], e['sy'], e['sz'], e['bloque'], e['s']
    lineas = []
    errores = []
    avisos = []

    def log(txt=''):
        lineas.append(txt)

    log('# Informe de validación — granja de Enderman v2')
    log()
    log(f'- Tamaño: {sx} x {sy} x {sz}')
    if (sx, sy, sz) != (granja.SX, granja.SY, granja.SZ):
        errores.append(f'tamaño inesperado {sx}x{sy}x{sz}')

    # ------------------------------------------------------ pozo de caída
    tapados = [(x, y, z) for y in range(5, granja.Y_PLATFORM + 1)
               for x in range(C - 1, C + 2) for z in range(C - 1, C + 2)
               if bloque(x, y, z)[0] != 'minecraft:air']
    log(f'- Pozo 3x3 (Y 5-{granja.Y_PLATFORM}): '
        f'{"libre" if not tapados else f"{len(tapados)} bloques tapándolo"}')
    if tapados:
        errores.append(f'pozo tapado en {tapados[:5]}')

    # --------------------------------------------------------------- caída
    caida = granja.Y_PLATFORM - granja.Y_PAD
    log(f'- Caída: {caida} bloques (mínimo 43 para matar a un Enderman)')
    if caida < 43:
        errores.append(f'caída demasiado corta: {caida}')

    # ------------------------------------------------------ tolvas y cofre
    tolvas = {}
    cofres = set()
    for y in range(0, granja.Y_PLATFORM + 1):
        for x in range(sx):
            for z in range(sz):
                nombre, est = bloque(x, y, z)
                if nombre == 'minecraft:hopper':
                    tolvas[(x, y, z)] = int(est.get('facing_direction', 0))
                elif nombre == 'minecraft:chest':
                    cofres.add((x, y, z))
    log(f'- Tolvas: {len(tolvas)} · cofres: {len(cofres)}')
    malas = []
    for pos in tolvas:
        p, pasos = pos, 0
        vista = {pos}
        while True:
            d = tolvas.get(p)
            if d is None:
                break
            dx, dy, dz = DIRS.get(d, (0, 0, 0))
            p = (p[0] + dx, p[1] + dy, p[2] + dz)
            pasos += 1
            if p in cofres:
                break
            if p not in tolvas:
                malas.append(pos)
                break
            if p in vista:
                malas.append(pos)          # bucle
                break
            vista.add(p)
            if pasos > 100:
                malas.append(pos)
                break
    if malas:
        errores.append(f'{len(malas)} tolvas no llegan al cofre: {malas[:4]}')
        log(f'- Cadena de tolvas: {len(malas)} tolvas sin salida')
    else:
        log('- Cadena de tolvas: todas llegan al cofre doble')

    # ------------------------------------------------------------ entidades
    entidades = [dict(x) for x in s.get('entities', [])]
    ids = collections.defaultdict(list)
    for ent in entidades:
        ids[ent.get('identifier')].append(ent)
    log(f'- Entidades: {", ".join(f"{k} x{len(v)}" for k, v in ids.items()) or "ninguna"}')
    endermitas = ids.get('minecraft:endermite', [])
    if not endermitas:
        errores.append('no hay endermita')
    else:
        end = endermitas[0]
        if not end.get('CustomName'):
            errores.append('la endermita no tiene CustomName (despawnearía)')
        if 'RideID' not in end:
            errores.append('la endermita no está montada en la vagoneta')
    if not ids.get('minecraft:minecart'):
        errores.append('no hay vagoneta para la endermita')

    # ------------------------------------------------ luces en la plataforma
    luces_arriba = []
    for y in range(granja.Y_PLATFORM + 1, sy):
        for x in range(sx):
            for z in range(sz):
                n = bloque(x, y, z)[0]
                if n in LUCES:
                    luces_arriba.append((x, y, z, n))
    if luces_arriba:
        avisos.append(f'{len(luces_arriba)} fuentes de luz sobre la plataforma')
        log(f'- Luces sobre la plataforma: {len(luces_arriba)}')
    else:
        log('- Luces sobre la plataforma: ninguna (la plataforma queda oscura)')

    # ------------------------------------------------------------- simetría
    excluir = {
        (C, 57, C - 6), (C, 57, C + 6), (C - 6, 57, C), (C + 6, 57, C),
    }
    def norm(p):
        return ('hoja', ()) if 'leaves' in p[0] else p

    fallos = []
    for y in range(53, sy):
        for x in range(sx):
            for z in range(sz):
                if (x, y, z) in excluir:
                    continue
                a = norm(bloque(x, y, z))
                b = norm(bloque(2 * C - x, y, z))
                c = norm(bloque(x, y, 2 * C - z))
                if a != b or a != c:
                    fallos.append((x, y, z))
    log(f'- Simetría (Y>=53): {"perfecta" if not fallos else f"{len(fallos)} diferencias"}')
    if fallos:
        avisos.append(f'{len(fallos)} bloques asimétricos: {fallos[:4]}')

    # ------------------------------------------------------------ materiales
    conteo = collections.Counter()
    for y in range(sy):
        for x in range(sx):
            for z in range(sz):
                n = bloque(x, y, z)[0]
                if n != 'minecraft:air':
                    conteo[n] += 1
    log()
    log('## Materiales')
    log()
    log('| bloque | cantidad |')
    log('| --- | ---: |')
    for n, c in conteo.most_common():
        log(f'| {n.replace("minecraft:", "")} | {c} |')

    # -------------------------------------------------------------- vistas
    def simbolo(n):
        if n == 'minecraft:air':
            return ' '
        if 'leaves' in n:
            return '"'
        if 'glass' in n:
            return 'o'
        if 'carpet' in n or n.endswith('_wool'):
            return ','
        return {'minecraft:end_stone': '.', 'minecraft:end_stone_bricks': '=',
                'minecraft:purpur_block': '#', 'minecraft:hopper': 'H',
                'minecraft:chest': 'C', 'minecraft:glowstone': '*',
                'minecraft:sea_lantern': '*', 'minecraft:rail': '-'}.get(n, '?')

    log()
    log('## Planta de la plataforma (Y=52)')
    log()
    log('```')
    for z in range(sz):
        log(''.join(simbolo(bloque(x, granja.Y_PLATFORM, z)[0]) for x in range(sx)))
    log('```')
    log()
    log('## Corte vertical (Z=31, de arriba abajo)')
    log()
    log('```')
    for y in range(sy - 1, -1, -1):
        log(f'{y:02d} ' + ''.join(simbolo(bloque(x, y, 31)[0]) for x in range(sx)))
    log('```')
    log('° leyenda: . end_stone  = bricks  # purpur  " hojas  o cristal  '
        'H tolva  C cofre  * luz')

    log()
    if errores:
        log('## ERRORES')
        for x in errores:
            log(f'- {x}')
    else:
        log('## Sin errores')
    if avisos:
        log()
        log('## Avisos')
        for x in avisos:
            log(f'- {x}')

    os.makedirs(SALIDA, exist_ok=True)
    with open(os.path.join(SALIDA, 'informe.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas) + '\n')
    print('\n'.join(lineas[:28]))
    print(f'... informe completo en salida/informe.txt ({len(lineas)} líneas)')
    return 1 if errores else 0


if __name__ == '__main__':
    sys.exit(main())
