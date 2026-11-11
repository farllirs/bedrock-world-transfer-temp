"""Escritor NBT little-endian (formato Bedrock) para generar .mcstructure.

No usa dependencias externas: solo struct. Los helpers construyen los tags
tal como los espera Minecraft Bedrock (nombres con longitud uint16 LE).
"""
import struct

T_BYTE = 1
T_SHORT = 2
T_INT = 3
T_LONG = 4
T_FLOAT = 5
T_DOUBLE = 6
T_BYTE_ARRAY = 7
T_STRING = 8
T_LIST = 9
T_COMPOUND = 10
T_INT_ARRAY = 11


def s(text):
    b = text.encode('utf-8')
    return struct.pack('<H', len(b)) + b


def i8(v):
    return struct.pack('<b', v)


def i16(v):
    return struct.pack('<h', v)


def i32(v):
    return struct.pack('<i', v)


def i64(v):
    return struct.pack('<q', v)


def f32(v):
    return struct.pack('<f', v)


def tag(t, name, payload=b''):
    return bytes([t]) + s(name) + payload


def byte_tag(name, v):
    return tag(T_BYTE, name, i8(v))


def int_tag(name, v):
    return tag(T_INT, name, i32(v))


def long_tag(name, v):
    return tag(T_LONG, name, i64(v))


def float_tag(name, v):
    return tag(T_FLOAT, name, f32(v))


def string_tag(name, v):
    return tag(T_STRING, name, s(v))


def int_list(name, values):
    return tag(T_LIST, name,
               bytes([T_INT]) + i32(len(values)) + b''.join(i32(v) for v in values))


def float_list(name, values):
    return tag(T_LIST, name,
               bytes([T_FLOAT]) + i32(len(values)) + b''.join(f32(v) for v in values))


def int_lists(name, lists):
    """Lista de listas de int (block_indices del .mcstructure)."""
    body = b''.join(bytes([T_INT]) + i32(len(l)) + b''.join(i32(v) for v in l)
                    for l in lists)
    return tag(T_LIST, name, bytes([T_LIST]) + i32(len(lists)) + body)


def compound(name, entries):
    return tag(T_COMPOUND, name, b''.join(entries) + b'\x00')


def compound_list(name, entries):
    """Lista de compuestos. Cada entrada es una lista de tags ya construidos."""
    body = b''.join(b''.join(e) + b'\x00' for e in entries)
    return tag(T_LIST, name, bytes([T_COMPOUND]) + i32(len(entries)) + body)
