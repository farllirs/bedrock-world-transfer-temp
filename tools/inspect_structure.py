"""Reads a Bedrock .mcstructure (little-endian NBT) and prints a report."""
import sys, collections
sys.path.insert(0, 'tools')
import nbt

path = sys.argv[1] if len(sys.argv) > 1 else 'granja_enderman_mega.mcstructure'
b = open(path, 'rb').read()
root = nbt.read(b)
s = root['structure']
SX, SY, SZ = root['size']
d = s['palette']['default']
pal = d['block_palette']
names = [p['name'] for p in pal]
states = [p.get('states') for p in pal]
layer0 = s['block_indices'][0]
layer1 = s['block_indices'][1] if len(s['block_indices']) > 1 else [-1] * len(layer0)

print(f'file            : {path}')
print(f'size (X,Y,Z)    : {SX} x {SY} x {SZ}')
print(f'palette entries : {len(pal)}')
print(f'format_version  : {root.get("format_version")}')
print(f'world origin    : {root.get("structure_world_origin")}')
print(f'entities        : {[e.get("identifier") for e in s.get("entities", [])]}')

def at(x, y, z):
    return layer0[x * SY * SZ + y * SZ + z]

cnt = collections.Counter()
per_y = collections.Counter()
for x in range(SX):
    for y in range(SY):
        for z in range(SZ):
            i = at(x, y, z)
            if i >= 0:
                cnt[names[i]] += 1
                if names[i] != 'minecraft:air':
                    per_y[y] += 1

tot = sum(v for k, v in cnt.items() if k != 'minecraft:air')
print(f'non-air blocks  : {tot}')
print('\n--- blocks by name ---')
for n, c in cnt.most_common():
    print(f'{c:6d}  {n}')

print('\n--- non-air blocks per Y layer ---')
for y in range(SY):
    if per_y[y]:
        print(f'Y+{y:02d}: {per_y[y]:5d}')

# block entities
bpd = d.get('block_position_data') or {}
print(f'\n--- block entities ({len(bpd)}) ---')
be_count = collections.Counter()
for k, v in bpd.items():
    if isinstance(v, dict) and 'block_entity_data' in v:
        be = v['block_entity_data']
        be_count[be.get('id', '?')] += 1
        if len(be_count) < 40:
            sm = {kk: vv for kk, vv in be.items() if kk in ('id', 'x', 'y', 'z', 'identifier', 'Item', 'Items', 'pairx', 'pairz', 'SpawnX')}
            print(k, sm)
for n, c in be_count.items():
    print(f'   {c:4d} x {n}')

# palette entries actually used
print('\n--- palette with states ---')
for i, n in enumerate(names):
    if cnt.get(n) and states[i]:
        print(f'{i:3d} {n} {states[i]}')

# ascii maps of the busiest layers
def charmap():
    used = sorted({names[at(x, y, z)] for x in range(SX) for y in range(SY) for z in range(SZ)}
                  - {'minecraft:air'})
    chars = '.123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    m = {n: chars[min(i + 1, len(chars) - 1)] for i, n in enumerate(used)}
    return m

m = charmap()
busy = sorted(per_y.items(), key=lambda kv: -kv[1])[:14]
print('\n--- ascii of busiest layers (rows = Z, cols = X) ---')
for y, _c in sorted(busy, key=lambda kv: -kv[0]):
    print(f'\n=== Y+{y} ===')
    for z in range(SZ):
        row = ''.join(m.get(names[at(x, y, z)], '.') if at(x, y, z) >= 0 else ' ' for x in range(SX))
        if row.strip():
            print(f'z{z:02d} {row}')
print('\nlegend: ' + ', '.join(f'{v}={k}' for k, v in m.items()))
