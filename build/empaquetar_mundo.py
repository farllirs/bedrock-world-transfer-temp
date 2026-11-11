"""Mete los .mcstructure dentro de un .mcworld para que viajen con el mundo.

Si en world/ hay uno o más .mcworld, se generan copias en salida/ con la
carpeta structures/ dentro. Así el mundo descargado ya trae las estructuras
y basta con ejecutar los comandos de salida/comandos.txt.
"""
import glob
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(HERE)
ESTRUCTURAS = os.path.join(RAIZ, 'estructuras')
SALIDA = os.path.join(RAIZ, 'salida')


def inyectar(mundo, destino):
    nombres = sorted(os.path.basename(p) for p in
                     glob.glob(os.path.join(ESTRUCTURAS, '*.mcstructure')))
    dentro = {f'structures/{n}' for n in nombres}
    with zipfile.ZipFile(mundo) as zin, \
            zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename in dentro:
                continue                     # se reemplaza por la versión nueva
            zout.writestr(item, zin.read(item.filename))
        for n in nombres:
            with open(os.path.join(ESTRUCTURAS, n), 'rb') as f:
                zout.writestr(f'structures/{n}', f.read())
    return len(nombres)


def main():
    mundos = sorted(glob.glob(os.path.join(RAIZ, 'world', '*.mcworld')))
    if not mundos:
        print('No hay ningún .mcworld en world/: solo se generan estructuras.')
        return 0
    os.makedirs(SALIDA, exist_ok=True)
    for mundo in mundos:
        if not zipfile.is_zipfile(mundo):
            print(f'AVISO: {mundo} no parece un .mcworld (¿es un zip?)')
            continue
        destino = os.path.join(SALIDA, 'far_default_nuevo.mcworld')
        n = inyectar(mundo, destino)
        print(f'{os.path.basename(mundo)} -> {destino} ({n} estructuras dentro)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
