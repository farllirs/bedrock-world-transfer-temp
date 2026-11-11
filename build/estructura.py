"""Modelo de una estructura 3D y escritor de .mcstructure (Bedrock)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'tools'))
import nbtwrite as W  # noqa: E402

AIR = ('minecraft:air', ())
# Versión de estados de bloque de la 26.x (la misma que usaba el .mcstructure viejo,
# que carga bien en el juego).
VERSION = 18168865


class Grid:
    def __init__(self, sx, sy, sz):
        self.sx, self.sy, self.sz = sx, sy, sz
        self.blocks = {}
        self.bes = {}
        self.entities = []

    def inside(self, x, y, z):
        return 0 <= x < self.sx and 0 <= y < self.sy and 0 <= z < self.sz

    def set(self, x, y, z, block):
        if not self.inside(x, y, z):
            return
        if block is None or block == AIR:
            self.blocks.pop((x, y, z), None)
            self.bes.pop((x, y, z), None)
        else:
            self.blocks[(x, y, z)] = block

    def get(self, x, y, z):
        return self.blocks.get((x, y, z), AIR)

    def box(self, x0, x1, y0, y1, z0, z1, block):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    self.set(x, y, z, block)

    def clear(self, x0, x1, y0, y1, z0, z1):
        self.box(x0, x1, y0, y1, z0, z1, AIR)

    def be(self, x, y, z, entries):
        self.bes[(x, y, z)] = entries

    def entity(self, identifier, pos, unique_id, extra=()):
        e = [
            W.string_tag('identifier', identifier),
            W.float_list('Pos', pos),
            W.float_list('Rotation', [0.0, 0.0]),
            W.float_tag('FallDistance', 0.0),
        ]
        e += list(extra)
        e += [W.long_tag('UniqueID', unique_id)]
        self.entities.append(e)

    def count(self):
        out = {}
        for b in self.blocks.values():
            out[b[0]] = out.get(b[0], 0) + 1
        return out


def _state_tags(states):
    out = []
    for k, v in states:
        out.append(W.string_tag(k, v) if isinstance(v, str) else W.int_tag(k, v))
    return W.compound('states', out)


def write(grid, path, world_origin=(0, 0, 0)):
    sx, sy, sz = grid.sx, grid.sy, grid.sz
    palette = []
    index = {}

    def pal_id(block):
        if block not in index:
            index[block] = len(palette)
            palette.append(block)
        return index[block]

    pal_id(AIR)
    n = sx * sy * sz
    layer0 = [-1] * n
    for (x, y, z), b in grid.blocks.items():
        layer0[x * sy * sz + y * sz + z] = pal_id(b)

    bpd = []
    for (x, y, z), entries in sorted(grid.bes.items()):
        i = x * sy * sz + y * sz + z
        data = list(entries) + [
            W.int_tag('x', x), W.int_tag('y', y), W.int_tag('z', z),
        ]
        bpd.append(W.compound(str(i), [W.compound('block_entity_data', data)]))

    pal_entries = []
    for name, states in palette:
        pal_entries.append([
            W.string_tag('name', name),
            _state_tags(states),
            W.int_tag('version', VERSION),
        ])

    structure = W.compound('structure', [
        W.int_lists('block_indices', [layer0, [-1] * n]),
        W.compound_list('entities', grid.entities),
        W.compound('palette', [
            W.compound('default', [
                W.compound_list('block_palette', pal_entries),
                W.compound('block_position_data', bpd),
            ]),
        ]),
    ])
    root = W.compound('', [
        W.int_tag('format_version', 1),
        W.int_list('size', [sx, sy, sz]),
        structure,
        W.int_list('structure_world_origin', list(world_origin)),
    ])
    with open(path, 'wb') as f:
        f.write(root)
    return len(root)
