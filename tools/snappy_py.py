"""Descompresor Snappy en Python puro (bloques de LevelDB).

Sirve de respaldo cuando no está libsnappy en el sistema (por ejemplo en un
runner de GitHub Actions sin paquetes extra).
"""


def _varint(b, o):
    r = 0
    s = 0
    while True:
        c = b[o]
        o += 1
        r |= (c & 0x7f) << s
        if c < 0x80:
            return r, o
        s += 7


def _copy(out, off, ln):
    start = len(out) - off
    if start < 0 or off <= 0:
        raise ValueError('offset inválido')
    if off >= ln:
        out += out[start:start + ln]
    else:
        for i in range(ln):
            out.append(out[start + i])


def uncompress(data):
    n, o = _varint(data, 0)
    out = bytearray()
    while o < len(data):
        tag = data[o]
        o += 1
        t = tag & 3
        if t == 0:                                   # literal
            ln = tag >> 2
            if ln < 60:
                ln += 1
            else:
                extra = ln - 59
                ln = int.from_bytes(data[o:o + extra], 'little') + 1
                o += extra
            out += data[o:o + ln]
            o += ln
        elif t == 1:                                 # copia, offset 1 byte
            ln = ((tag >> 2) & 7) + 4
            off = ((tag >> 5) << 8) | data[o]
            o += 1
            _copy(out, off, ln)
        elif t == 2:                                 # copia, offset 2 bytes
            ln = (tag >> 2) + 1
            off = data[o] | (data[o + 1] << 8)
            o += 2
            _copy(out, off, ln)
        else:                                        # copia, offset 4 bytes
            ln = (tag >> 2) + 1
            off = int.from_bytes(data[o:o + 4], 'little')
            o += 4
            _copy(out, off, ln)
    if len(out) != n:
        raise ValueError(f'snappy: tamaño {len(out)} != {n}')
    return bytes(out)
