"""Genera las estructuras, los comandos de colocación y el paquete descargable.

Uso:
    python build/construir.py [--config config.json]
"""
import argparse
import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import estructura  # noqa: E402
import granja  # noqa: E402
import puente  # noqa: E402

ESTRUCTURAS = os.path.join(RAIZ, 'estructuras')
SALIDA = os.path.join(RAIZ, 'salida')

CONFIG_DEFECTO = {
    "granja": {"centro_x": 0, "centro_z": -520, "y_base": 64},
    "puente": {"lado": "norte", "desde_x": 0, "desde_z": -100},
}


def cargar_config(ruta):
    cfg = json.loads(json.dumps(CONFIG_DEFECTO))
    if ruta and os.path.exists(ruta):
        with open(ruta, encoding='utf-8') as f:
            datos = json.load(f)
        for seccion in ('granja', 'puente'):
            cfg[seccion].update(datos.get(seccion, {}))
    return cfg


def tiles_del_puente(largo_total):
    """Devuelve (n_piezas, resto)."""
    n, resto = divmod(largo_total, puente.LARGO)
    return n, resto


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default=os.path.join(RAIZ, 'config.json'))
    args = ap.parse_args()
    cfg = cargar_config(args.config)

    os.makedirs(ESTRUCTURAS, exist_ok=True)
    os.makedirs(SALIDA, exist_ok=True)

    # ------------------------------------------------------------- granja
    g = granja.construir()
    ruta_granja = os.path.join(ESTRUCTURAS, 'granja_enderman_v2.mcstructure')
    peso = estructura.write(g, ruta_granja)
    print(f'granja: {g.sx}x{g.sy}x{g.sz}, {len(g.blocks)} bloques, '
          f'{peso/1024/1024:.2f} MiB -> {ruta_granja}')

    # ------------------------------------------------------------- puente
    piezas = []
    for eje in ('z', 'x'):
        nombre = f'puente_{eje}.mcstructure'
        ruta = os.path.join(ESTRUCTURAS, nombre)
        estructura.write(puente.construir(puente.LARGO, eje), ruta)
        piezas.append(nombre)

    # --------------------------------------------------- comandos y cálculo
    cx = int(cfg['granja']['centro_x'])
    cz = int(cfg['granja']['centro_z'])
    yb = int(cfg['granja']['y_base'])
    lado = cfg['puente']['lado'].lower()
    desde_x = int(cfg['puente']['desde_x'])
    desde_z = int(cfg['puente']['desde_z'])

    # Esquina de la estructura (local 0,0,0) y nivel del suelo de la sala.
    esquina = (cx - granja.C, yb, cz - granja.C)
    suelo = yb + granja.Y_FLOOR
    carga_puente_y = suelo - 1          # el tablero está en la capa local 1

    pared = {
        'norte': ('z', cz - 22),
        'sur': ('z', cz + 22),
        'oeste': ('x', cx - 22),
        'este': ('x', cx + 22),
    }
    if lado not in pared:
        raise SystemExit(f"lado desconocido: {lado}")
    eje, muro = pared[lado]
    inicio = desde_x if eje == 'x' else desde_z
    signo = -1 if muro < inicio else 1
    total = abs(muro - inicio) + 1
    n, resto = tiles_del_puente(total)

    comandos = [
        '# Granja de Enderman v2 - comandos de colocación',
        '# Requiere trucos activos y los .mcstructure dentro de <mundo>/structures/',
        '# (el .mcworld de la carpeta ya los lleva dentro).',
        '',
        '# --- 1. Granja (la esquina es su bloque 0,0,0) ---',
        f'/structure load granja_enderman_v2 {esquina[0]} {esquina[1]} {esquina[2]}',
        '',
        f'# --- 2. Puente hacia el {lado} ({total} bloques) ---',
        f'#     el tablero queda al nivel y={suelo}',
    ]

    linea = cx if eje == 'z' else cz
    for i in range(n):
        if eje == 'z':
            z0 = inicio - 12 * i - 11 if signo < 0 else inicio + 12 * i
            comandos.append(
                f'/structure load puente_z {linea - 5} {carga_puente_y} {z0}')
        else:
            x0 = inicio - 12 * i - 11 if signo < 0 else inicio + 12 * i
            comandos.append(
                f'/structure load puente_x {x0} {carga_puente_y} {linea - 5}')
    if resto:
        nombre_resto = f'puente_{eje}_resto.mcstructure'
        estructura.write(puente.construir(resto, eje),
                         os.path.join(ESTRUCTURAS, nombre_resto))
        piezas.append(nombre_resto)
        if eje == 'z':
            z0 = muro if signo < 0 else muro - resto + 1
            comandos.append(
                f'/structure load puente_{eje}_resto {linea - 5} {carga_puente_y} {z0}')
        else:
            x0 = muro if signo < 0 else muro - resto + 1
            comandos.append(
                f'/structure load puente_{eje}_resto {x0} {carga_puente_y} {linea - 5}')

    comandos += [
        '',
        '# --- 3. Comprobaciones ---',
        f'#     centro de la granja: {cx} {cz}',
        f'#     plataforma de spawn: y={yb + granja.Y_PLATFORM}',
        f'#     muro del puente: {"z" if eje == "z" else "x"}={muro}',
        '#     distancia mínima recomendada a la isla del dragón: 300-400 bloques',
        '#     desde su bloque más lejano.',
    ]
    ruta_comandos = os.path.join(SALIDA, 'comandos.txt')
    with open(ruta_comandos, 'w', encoding='utf-8') as f:
        f.write('\n'.join(comandos) + '\n')

    # ------------------------------------------------------------ resumen
    conteo = g.count()
    resumen = [
        '# Granja de Enderman v2 — resumen de construcción',
        '',
        f'- Tamaño: {g.sx} x {g.sy} x {g.sz} (X, Y, Z)',
        f'- Bloques colocados: {len(g.blocks):,}'.replace(',', '.'),
        f'- Entidades: {len(g.entities)} (vagoneta + endermita)',
        f'- Centro: {cx}, {cz} · base Y={yb} · plataforma Y={yb + granja.Y_PLATFORM}',
        f'- Caída de los Enderman: {granja.Y_PLATFORM - granja.Y_PAD} bloques',
        f'- Puente: {total} bloques hacia el {lado} '
        f'({n} piezas de {puente.LARGO}' + (f' + resto de {resto})' if resto else ')'),
        '',
        '## Materiales',
        '',
        '| bloque | cantidad |',
        '| --- | ---: |',
    ]
    for nombre, c in sorted(conteo.items(), key=lambda kv: -kv[1]):
        resumen.append(f'| {nombre.replace("minecraft:", "")} | {c} |')
    with open(os.path.join(SALIDA, 'RESUMEN.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(resumen) + '\n')

    # --------------------------------------------------------------- zip
    ruta_zip = os.path.join(SALIDA, 'granja_enderman_v2.zip')
    with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as z:
        for f_ in sorted(os.listdir(ESTRUCTURAS)):
            z.write(os.path.join(ESTRUCTURAS, f_), 'structures/' + f_)
        z.write(ruta_comandos, 'comandos.txt')
        z.write(os.path.join(SALIDA, 'RESUMEN.md'), 'RESUMEN.md')
        leeme = os.path.join(RAIZ, 'README.md')
        if os.path.exists(leeme):
            z.write(leeme, 'README.md')

    print(f'puente: {total} bloques, {n} piezas + resto {resto}')
    print(f'comandos -> {ruta_comandos}')
    print(f'paquete  -> {ruta_zip}')


if __name__ == '__main__':
    main()
