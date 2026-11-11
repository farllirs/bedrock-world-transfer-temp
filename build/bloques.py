"""Bloques de Bedrock usados por la granja y el puente.

Cada bloque es una tupla (nombre, estados) donde estados son pares
(clave, valor) ordenados, para poder meterlos en la paleta del .mcstructure.
"""


def B(name, **states):
    return (name, tuple(sorted(states.items())))


# --- estructura ---
AIR = B('minecraft:air')
END_STONE = B('minecraft:end_stone')
BRICK = B('minecraft:end_stone_bricks')
PURPUR = B('minecraft:purpur_block')
OBSIDIAN = B('minecraft:obsidian')

# --- vegetación (no permite spawns) ---
OAK = B('minecraft:oak_leaves', persistent_bit=1, update_bit=0)
AZALEA = B('minecraft:azalea_leaves', persistent_bit=1, update_bit=0)
FLOWER = B('minecraft:azalea_leaves_flowered', persistent_bit=1, update_bit=0)
MANGROVE = B('minecraft:mangrove_leaves', persistent_bit=1, update_bit=0)
CHERRY = B('minecraft:cherry_leaves', persistent_bit=1, update_bit=0)

# --- cristal / luz ---
GLASS = B('minecraft:glass')
MAGENTA_GLASS = B('minecraft:magenta_stained_glass')
PURPLE_GLASS = B('minecraft:purple_stained_glass')
GLOWSTONE = B('minecraft:glowstone')
SEA_LANTERN = B('minecraft:sea_lantern')

# --- lana y alfombras (el ojo del End) ---
WHITE = B('minecraft:white_wool')
BLACK = B('minecraft:black_wool')
GREEN = B('minecraft:green_wool')
MAGENTA = B('minecraft:magenta_wool')
PURPLE = B('minecraft:purple_wool')
LGRAY = B('minecraft:light_gray_wool')

C_WHITE = B('minecraft:white_carpet')
C_BLACK = B('minecraft:black_carpet')
C_GREEN = B('minecraft:green_carpet')
C_MAGENTA = B('minecraft:magenta_carpet')
C_PURPLE = B('minecraft:purple_carpet')
C_LGRAY = B('minecraft:light_gray_carpet')

# --- mecánica ---
# facing_direction: 0=abajo, 1=arriba, 2=norte(-Z), 3=sur(+Z), 4=oeste(-X), 5=este(+X)
DOWN, UP, NORTH, SOUTH, WEST, EAST = 0, 1, 2, 3, 4, 5


def HOPPER(d):
    return B('minecraft:hopper', facing_direction=d, toggle_bit=0)


def CHEST(direction):
    return B('minecraft:chest', **{'minecraft:cardinal_direction': direction})


RAIL = B('minecraft:rail', rail_direction=0)
