"""Granja de Enderman v2 — 'Santuario del Ojo'.

Medidas locales: 63 x 59 x 63 (X, Y, Z). El centro es la columna 31.
Capas (Y local):
  0-2    base escalonada de hojas
  3      suelo de la sala de recolección (45x45)
  4      alfombra del ojo + meseta de tolvas + cofre doble
  5-11   sala (paredes) / el pozo baja hasta aquí
  12     techo de hojas
  13-47  torre decorada con el pozo de 3x3 dentro
  48-51  faldón de hojas bajo la plataforma
  52     plataforma de spawn de 63x63 con agujero de 3x3
  53-54  muro de hojas (2 de alto)
  55-58  cuatro farolillos de cristal (uno con la endermita)
La caída es de 52 - 4 = 48 bloques: el Enderman muere al impactar.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'tools'))

import nbtwrite as W  # noqa: E402
from estructura import Grid  # noqa: E402
from bloques import (  # noqa: E402
    AIR, END_STONE, BRICK, PURPUR, OAK, AZALEA, FLOWER, MANGROVE, CHERRY,
    GLASS, MAGENTA_GLASS, PURPLE_GLASS, GLOWSTONE, SEA_LANTERN,
    C_WHITE, C_BLACK, C_GREEN, C_MAGENTA, C_PURPLE,
    HOPPER, CHEST, RAIL, EAST, NORTH, SOUTH,
)

SX = SZ = 63
SY = 59
C = 31

Y_FLOOR = 3          # bloques del suelo de la sala (se camina en Y_FLOOR+1)
Y_PAD = 4            # meseta de tolvas
Y_CEIL = 12          # techo de hojas
Y_TOWER0, Y_TOWER1 = 13, 47
Y_PLATFORM = 52
Y_WALL = (53, 54)


def _leaf(x, y, z):
    """Mezcla de hojas con patrón estable: da textura sin romper la simetría."""
    h = (x * 37 + z * 17 + y * 11) % 23
    if h < 6:
        return AZALEA
    if h == 6:
        return FLOWER
    if h < 12:
        return MANGROVE
    if h == 12 and (x + z) % 9 == 0:
        return CHERRY
    return OAK


def _tower_width(y):
    if 13 <= y <= 16:
        return 7   # 15x15
    if 17 <= y <= 21:
        return 6   # 13x13
    if 22 <= y <= 27:
        return 5   # 11x11
    if 28 <= y <= 34:
        return 4   # 9x9
    if 35 <= y <= 39:
        return 5
    if 40 <= y <= 47:
        return 6
    return 0


def _eye_half_height(dx):
    a = abs(dx)
    if a > 20:
        return -1
    t = a / 20.0
    return int(round(13.5 * (1.0 - t * t) ** 0.75))


def construir(endermite_nombre='Endermita'):
    g = Grid(SX, SY, SZ)

    def cheb(x, z):
        return max(abs(x - C), abs(z - C))

    def square(y, dmax, blk):
        for x in range(C - dmax, C + dmax + 1):
            for z in range(C - dmax, C + dmax + 1):
                g.set(x, y, z, blk)

    # ---------------------------------------------------------------- base
    for x in range(SX):
        for z in range(SZ):
            d = cheb(x, z)
            if 17 <= d <= 20:
                g.set(x, 0, z, _leaf(x, 0, z))
            if 19 <= d <= 22:
                g.set(x, 1, z, _leaf(x, 1, z))
    square(Y_FLOOR, 22, END_STONE)          # suelo de la sala (45x45)

    # ------------------------------------------------------------ paredes
    for y in range(4, 12):
        for x in range(C - 22, C + 23):
            for z in range(C - 22, C + 23):
                if cheb(x, z) != 22:
                    continue
                if y in (7, 8) and (x + z) % 6 == 0:
                    blk = MAGENTA_GLASS if (x + z) % 12 == 0 else PURPLE_GLASS
                elif y == 10:
                    blk = PURPUR
                elif y == 4:
                    blk = END_STONE
                else:
                    blk = BRICK
                g.set(x, y, z, blk)

    # Cuatro entradas: una por lado, 5 de ancho y 4 de alto.
    for y in range(4, 8):
        for t in range(-2, 3):
            g.set(C + t, y, C - 22, AIR)
            g.set(C + t, y, C + 22, AIR)
            g.set(C - 22, y, C + t, AIR)
            g.set(C + 22, y, C + t, AIR)
    # Marco de purpur de las entradas.
    for t in range(-3, 4):
        for (x, z) in ((C + t, C - 22), (C + t, C + 22),
                       (C - 22, C + t), (C + 22, C + t)):
            g.set(x, 8, z, PURPUR)
            if abs(t) == 3:
                for y in range(4, 8):
                    g.set(x, y, z, PURPUR)

    # ------------------------------------------------------------- techo
    for x in range(C - 22, C + 23):
        for z in range(C - 22, C + 23):
            g.set(x, Y_CEIL, z, _leaf(x, Y_CEIL, z))

    # -------------------------------------------- suelo: luz escondida
    # Las alfombras no bloquean la luz, así que el glowstone va debajo del
    # ojo: la sala queda iluminada y la fuente no se ve.
    for x in range(C - 22, C + 23):
        for z in range(C - 22, C + 23):
            d = cheb(x, z)
            if d == 22:
                g.set(x, Y_FLOOR, z, BRICK)
            elif d == 21 or (x + z) % 3 == 0:
                g.set(x, Y_FLOOR, z, GLOWSTONE)
            else:
                g.set(x, Y_FLOOR, z, END_STONE)

    # --------------------------------------------------------- ojo del End
    # Alfombras encima del suelo (nivel de paseo).
    for dx in range(-20, 21):
        h = _eye_half_height(dx)
        if h < 0:
            continue
        for dz in range(-h, h + 1):
            x, z = C + dx, C + dz
            r2 = dx * dx + dz * dz
            if abs(dz) >= h - 1:
                blk = C_BLACK if (abs(dx) + abs(dz)) % 3 else C_MAGENTA
            elif r2 <= 16:
                blk = C_BLACK                       # pupila
            elif r2 <= 56:
                blk = C_GREEN                       # iris
            elif r2 <= 90:
                blk = C_PURPLE                      # anillo del iris
            else:
                blk = C_WHITE                       # esclerótica
            if abs(dx) >= 15 and abs(dz) <= 1:
                blk = C_MAGENTA                     # destello del End
            g.set(x, Y_FLOOR + 1, z, blk)

    # ------------------------------------------------------ meseta de tolvas
    # Las 9 tolvas drenan hacia el este, fuera del ojo, a un cofre doble.
    pad = {
        (C - 1, C - 1): EAST, (C - 1, C): EAST, (C - 1, C + 1): EAST,
        (C, C - 1): SOUTH, (C, C): EAST, (C, C + 1): NORTH,
        (C + 1, C - 1): SOUTH, (C + 1, C): EAST, (C + 1, C + 1): NORTH,
    }
    for (x, z), d in pad.items():
        g.set(x, Y_PAD, z, HOPPER(d))
    g.set(C + 2, Y_PAD, C, HOPPER(EAST))
    g.set(C + 3, Y_PAD, C, HOPPER(EAST))

    # cofre doble (dos cofres emparejados)
    for i, x in enumerate((C + 4, C + 5)):
        other = C + 5 if i == 0 else C + 4
        g.set(x, Y_PAD, C, CHEST('west'))
        g.be(x, Y_PAD, C, [
            W.string_tag('id', 'Chest'),
            W.compound_list('Items', []),
            W.byte_tag('isMovable', 1),
            W.byte_tag('Findable', 0),
            W.int_tag('pairx', other),
            W.int_tag('pairz', C),
        ])

    # ------------------------------------------------------------- torre
    for y in range(Y_TOWER0, Y_TOWER1 + 1):
        w = _tower_width(y)
        square(y, w, END_STONE)
    for y in range(Y_TOWER0, Y_TOWER1 + 1):
        w = _tower_width(y)
        for x in range(C - w, C + w + 1):
            for z in range(C - w, C + w + 1):
                if cheb(x, z) != w:
                    continue
                ax, az = abs(x - C), abs(z - C)
                if ax == w and az == w:
                    blk = PURPUR                       # esquinas
                elif y % 7 == 0:
                    blk = BRICK                        # fajas
                elif y % 7 == 3 and (ax + az) % 4 == 0:
                    blk = MAGENTA_GLASS                # ventanas
                elif y % 7 == 3 and (ax + az) % 4 == 2:
                    blk = PURPLE_GLASS
                else:
                    continue
                g.set(x, y, z, blk)
    # collares de hojas en los escalones (que no queden repisas donde spawnear)
    for y, w in ((16, 7), (21, 6), (27, 5)):
        for x in range(C - w, C + w + 1):
            for z in range(C - w, C + w + 1):
                if cheb(x, z) == w:
                    g.set(x, y, z, _leaf(x, y, z))
    # remate superior, todo de hojas
    for x in range(C - 6, C + 7):
        for z in range(C - 6, C + 7):
            g.set(x, Y_TOWER1, z, _leaf(x, Y_TOWER1, z))

    # ---------------------------------------------------------- faldón
    for y, d0, d1 in ((51, 26, 30), (50, 24, 28), (49, 22, 26), (48, 20, 24)):
        for x in range(C - d1, C + d1 + 1):
            for z in range(C - d1, C + d1 + 1):
                if d0 <= cheb(x, z) <= d1:
                    g.set(x, y, z, _leaf(x, y, z))

    # ------------------------------------------------------- plataforma
    for x in range(SX):
        for z in range(SZ):
            d = cheb(x, z)
            if d == 31:
                blk = PURPUR
            elif d in (8, 16, 24):
                blk = BRICK
            elif abs(x - C) == abs(z - C):
                blk = BRICK
            elif d <= 3:
                blk = BRICK
            else:
                blk = END_STONE
            g.set(x, Y_PLATFORM, z, blk)

    # muro de hojas de 2 de alto (los Enderman no lo saltan)
    for y in Y_WALL:
        for x in range(SX):
            for z in range(SZ):
                if cheb(x, z) == 31:
                    g.set(x, y, z, _leaf(x, y, z))

    # jardincillos en las cuatro esquinas
    for (sx, sz) in ((C - 27, C - 27), (C - 27, C + 27),
                     (C + 27, C - 27), (C + 27, C + 27)):
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                g.set(sx + dx, 53, sz + dz, _leaf(sx + dx, 53, sz + dz))
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                g.set(sx + dx, 54, sz + dz, _leaf(sx + dx, 54, sz + dz))
        g.set(sx, 55, sz, _leaf(sx, 55, sz))

    # ------------------------------------------------------- farolillos
    # Cuatro farolillos de cristal alrededor del pozo; uno lleva la endermita.
    for (lx, lz) in ((C, C - 6), (C, C + 6), (C - 6, C), (C + 6, C)):
        for y in range(53, 56):
            g.set(lx, y, lz, BRICK)
        for dx in range(-1, 2):
            for dz in range(-1, 2):
                g.set(lx + dx, 56, lz + dz, _leaf(lx + dx, 56, lz + dz))
                g.set(lx + dx, 58, lz + dz, GLASS)
                if (dx, dz) != (0, 0):
                    g.set(lx + dx, 57, lz + dz, GLASS)

    ex, ez = C, C - 6
    g.set(ex, 57, ez, RAIL)
    g.entity('minecraft:minecart', (ex + 0.5, 57.06, ez + 0.5), 1001,
             [W.byte_tag('Persistent', 1)])
    g.entity('minecraft:endermite', (ex + 0.5, 57.20, ez + 0.5), 1002, [
        W.byte_tag('Persistent', 1),
        W.byte_tag('NaturalSpawn', 1),
        W.int_tag('Lifetime', 0),
        W.string_tag('CustomName', endermite_nombre),
        W.byte_tag('CustomNameVisible', 0),
        W.long_tag('RideID', 1001),
    ])

    # ------------------------------------------------- pozo de caída
    # Se cava al final para que nada lo tape: 3x3 desde el suelo de la sala
    # hasta el agujero de la plataforma.
    for y in range(5, Y_PLATFORM + 1):
        for x in range(C - 1, C + 2):
            for z in range(C - 1, C + 2):
                g.set(x, y, z, AIR)

    return g
