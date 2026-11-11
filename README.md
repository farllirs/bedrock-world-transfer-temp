# Granja de Enderman — End (Bedrock)

Granja de Enderman para Minecraft Bedrock **26.x**, en el End, rediseñada desde
cero a partir de la estructura vieja (`granja_enderman_mega.mcstructure`).

- **Santuario del Ojo**: plataforma de spawn de 63×63 sobre una torre decorada,
  con faldón de hojas, base escalonada, cuatro entradas y cuatro farolillos de
  cristal.
- **Sala de recolección** con un ojo del End gigante dibujado con alfombras de
  lana (pupila, iris, esclerótica y destellos magenta) y luz debajo del piso.
- **Señuelo de endermita** en vagoneta, con name tag, dentro de un farolillo de
  cristal (no puede morir ni despawnear).
- **Caída de 48 bloques** hasta una meseta de 9 tolvas que drena a un cofre doble.
- **Simetría** perfecta (comprobada en la validación) salvo la endermita y el
  desagüe de las tolvas, que son funcionales.

## Contenido del repositorio

| ruta | qué es |
| --- | --- |
| `build/granja.py` | geometría de la granja (63 × 59 × 63) |
| `build/puente.py` | pieza repetible del puente de hojas (11 × 7 × 12) |
| `build/estructura.py` | modelo 3D + escritor de `.mcstructure` |
| `build/construir.py` | genera estructuras, comandos, resumen y zip |
| `build/validar.py` | comprueba caída, tolvas, entidades, luces y simetría |
| `build/empaquetar_mundo.py` | mete las estructuras dentro de un `.mcworld` |
| `config.json` | coordenadas del centro, altura base y puente |
| `estructuras/` | `.mcstructure` generados (también se suben como artefacto) |
| `salida/` | `comandos.txt`, `informe.txt`, `RESUMEN.md` y el zip |
| `.github/workflows/construir.yml` | compilación automática en GitHub Actions |

## Compilar

Local (solo hace falta Python 3.10+, sin dependencias):

```bash
python build/construir.py     # genera estructuras + comandos + zip
python build/validar.py       # informe y comprobaciones (falla si hay errores)
```

En GitHub: cada push a `main` ejecuta el workflow **Construir granja de
Enderman** y deja el paquete en *Actions → run → Artifacts*.

## Instalar en el mundo

**Opción A — con el mundo ya empaquetado (lo que devuelve Actions).**
Si subes tu `.mcworld` a la carpeta `world/`, el workflow genera
`salida/far_default_nuevo.mcworld` con las estructuras ya dentro de
`structures/`. Abre ese mundo y ejecuta los comandos de `salida/comandos.txt`.

**Opción B — a mano.**
1. Copia los `.mcstructure` de `estructuras/` a `<tu mundo>/structures/`.
2. Entra al mundo (con trucos) y ejecuta los comandos de `salida/comandos.txt`.

**Siempre haz copia de seguridad del mundo antes de tocar nada.**

## Coordenadas y la regla de los 300–400 bloques

Por defecto (`config.json`):

```json
{
  "granja":  { "centro_x": 0, "centro_z": -520, "y_base": 64 },
  "puente":  { "lado": "norte", "desde_x": 0, "desde_z": -100 }
}
```

- El centro de la granja queda en `(0, -520)`; su borde más cercano a la isla
  está en `z = -489`, unos **389 bloques** del borde de la isla del dragón
  (`z ≈ -100`), dentro del margen de 300–400 que pediste.
- La granja se coloca con su esquina en `(centro_x - 31, y_base, centro_z - 31)`.
- El puente va del borde de la isla (`desde_*`) al muro de la granja
  (`centro ± 22`), así que su longitud se calcula sola.
- `y_base` hay que ajustarlo para que **el tablero del puente quede al nivel del
  suelo de la isla**: el suelo de la sala está en `y_base + 3`. El puente se
  carga en `y_base + 2`.

Si cambias de lado (`norte`, `sur`, `este`, `oeste`), el script elige la variante
`puente_z` o `puente_x`; no hace falta rotar nada.

## Cómo funciona la granja

1. Los Enderman aparecen en la plataforma (solo hay superficie spawneable en la
   plataforma: el resto es hoja, cristal o está iluminado).
2. La endermita con name tag, en vagoneta dentro del farolillo de cristal del
   centro, los atrae. Los Enderman se acercan al pozo de 3×3.
3. Caen **48 bloques** y mueren al impactar en la meseta de tolvas.
4. Las 9 tolvas drenan hacia el este y el cofre doble recoge las perlas.

Es una granja **automática**: no da XP (no hay cámara de matar). Si la quieres
con XP hay que dejar la caída en 43 bloques y añadir una cámara de golpeo.

## Materiales

`salida/RESUMEN.md` lleva la lista completa. En resumen: ~9.000 end stone,
~8.200 hojas (roble, azalea, azalea florida, manglejo y cerezo), ~1.800
ladrillos del End, ~600 purpur, 168 glowstone, 2 cofres, 11 tolvas, 1 vagoneta,
1 raíl y las lanas del ojo.

## Limitaciones

- No he podido abrir el `.mcworld` en Minecraft desde aquí: valido el formato
  releyendo el `.mcstructure` y comparándolo con el que ya te funcionaba, pero
  la prueba final es abrirlo en el juego (haz copia antes).
- La granja está pensada para 26.x; el formato `.mcstructure` v1 que genera es
  el mismo que el de tu estructura anterior.
- `salida/informe.txt` incluye una planta de la plataforma y un corte vertical
  en ASCII para revisar el diseño sin abrir el juego.
