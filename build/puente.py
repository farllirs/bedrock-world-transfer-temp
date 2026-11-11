"""Puente de hojas: pieza repetible de 11 de ancho, 7 de alto y N de largo.

El tablero queda en la capa local y=1, así que se carga en el mundo en
(altura_del_suelo - 1).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from estructura import Grid  # noqa: E402
from bloques import (  # noqa: E402
    BRICK, PURPUR, SEA_LANTERN, AZALEA, FLOWER, MANGROVE, OAK,
)

ANCHO = 11
ALTO = 7
LARGO = 12


def _leaf(u, y, v):
    h = (u * 29 + v * 13 + y * 7) % 17
    if h < 4:
        return AZALEA
    if h == 4:
        return FLOWER
    if h < 8:
        return MANGROVE
    return OAK


def _pieza(largo):
    g = Grid(ANCHO, ALTO, largo)
    medio = ANCHO // 2
    for v in range(largo):
        for u in range(ANCHO):
            a = abs(u - medio)
            if a <= 4:
                g.set(u, 0, v, _leaf(u, 0, v))          # panza
            g.set(u, 1, v, BRICK if a <= 1 else _leaf(u, 1, v))  # tablero
            if 3 <= a <= 5:
                g.set(u, 2, v, _leaf(u, 2, v))          # seto bajo
            if 4 <= a <= 5:
                g.set(u, 3, v, _leaf(u, 3, v))          # seto alto
            if v % LARGO == 0:                          # arco
                if a == 5:
                    g.set(u, 4, v, PURPUR)
                    g.set(u, 5, v, PURPUR)
                if a <= 5:
                    g.set(u, 6, v, _leaf(u, 6, v))
            if v % LARGO == LARGO // 2 and a == 2:      # faroles
                g.set(u, 2, v, SEA_LANTERN)
    return g


def _transponer(g):
    t = Grid(g.sz, g.sy, g.sx)
    for (x, y, z), b in g.blocks.items():
        t.set(z, y, x, b)
    return t


def construir(largo=LARGO, eje='z'):
    """eje='z' -> el puente avanza en Z; eje='x' -> avanza en X."""
    g = _pieza(largo)
    return g if eje == 'z' else _transponer(g)
