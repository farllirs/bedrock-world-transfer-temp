# Granjas masivas para Minecraft Bedrock (última versión) — investigación y plan

Fecha de la investigación: 10-nov-2026.
Objetivo: cambiar las granjas actuales del mundo survival `far_default` por granjas masivas y útiles, y mantener esta guía por si se borra el chat.

> **Fiabilidad.** Mucha información sobre granjas en la web es de baja calidad (blogs SEO, texto generado, tutoriales de Java presentados como si valieran para Bedrock). Cada dato lleva una etiqueta:
> - **[OK]** confirmado en la wiki o en una fuente seria.
> - **[?]** lo dice una sola fuente o hay contradicciones; probarlo antes de confiar.
> - **[Java]** funciona en Java; no asumir que sirve en Bedrock.
>
> Ninguna cifra de producción está medida por mí. Todas salen de las fuentes citadas.

---

## 1. Versión actual

- Versión más reciente encontrada: **Bedrock 26.60**, publicada el 28-oct-2026 (Drop 4 de 2026, con el bioma Ice Cave en experimentales). **[OK]**
- Hotfix anterior: 26.52 (25-sep-2026). **[OK]**
- Desde 2026 la numeración es por año (26.x). **[OK]**
- El formato `.mcstructure` pasó a versión 2 en 26.50 (preview). Las estructuras v1 se siguen cargando y se actualizan al guardarse. **[OK]**
- Pendiente: no encontré cambios de 26.50/26.60 que afecten a granjas. Confirmar leyendo el changelog completo en feedback.minecraft.net antes de construir.

---

## 2. Reglas de Bedrock que cambian el diseño de las granjas

| Tema | Regla en Bedrock | Fiabilidad |
|---|---|---|
| Golems de hierro | El pueblo necesita **≥ 20 camas y ≥ 10 aldeanos**; los golems aparecen alrededor del centro del pueblo. Las granjas de 3 aldeanos de Java no sirven. | [OK] wiki + varias guías |
| Techo del Nether | En Bedrock **no se pueden colocar bloques sobre el techo de bedrock** del Nether. Los diseños de Java "sobre el techo" (Gnembon, Ilmango, DashPum4) no funcionan. | [OK] wiki (wither) |
| Oro (piglins zombificados) | En Bedrock, si un portal se enciende y apaga muy rápido, **spawnea piglins mucho más rápido**. Por eso los diseños con portales en el Overworld superan a los de spawn natural. | [OK] wiki |
| Spawn de hostiles | Luz ≤ 7. El rendimiento depende de la **distancia de simulación** y del límite de mobs cercano. | [?] varias guías |
| Crecimiento de cultivos | Las guías dicen que en Bedrock los cultivos crecen más lento que en Java (≈ 3 veces; caña ≈ 54 min por 3 bloques frente a ≈ 18 en Java). Planear más superficie. | [?] |
| Caña de azúcar | Si se quita el agua de la base, se rompe al instante. Sirve para cosechas semiautomáticas. | [OK] |
| Zero-tick | Algunas fuentes dicen que en Bedrock siguen funcionando las granjas "zero-tick" de caña y bambú. | [?] probar primero |
| Aldeanos | Los comercios de aldeanos son más difíciles de bloquear y reiniciar que en Java. | [OK] |
| Wither skeleton | Aparecen en grupos de 2–3 en Bedrock (5 en Java). El Looting suma +2 % por nivel (máx. 8.5 % con Looting III) para la calavera. | [?] |
| Estrella del Nether | En Bedrock no desaparece sola (en Java sí). | [?] |
| Fortaleza vs. bastión | En Bedrock una región da fortaleza el 33 % de las veces (40 % en Java). | [?] |
| Golems y minecarts | Los golems de Bedrock pueden subir a minecarts y atacar a través de paredes. | [?] |

---

## 3. Catálogo de granjas (qué conviene para cada ítem del almacén)

Para cada una, "Datos reportados" son cifras de fuentes. "Lo que necesito" es lo que haría falta para colocarla en tu mundo.

### 3.1 Hierro (iron golem)
- **Mecánica:** aldea de ≥ 20 camas y ≥ 10 aldeanos en Bedrock; los golems caen a una cámara de muerte. **[OK]**
- **Datos reportados:** "600+ hierro/hora" (creador @MushoDen, edición no indicada) **[?]**; "400+ hierro/hora, diseño 26.1+" (varios videos, edición no indicada) **[?]**.
- **Riesgo:** muchos diseños de Java no sirven en Bedrock. Buscar uno hecho para Bedrock.
- **Lo que necesito:** el diseño como `.mcstructure`, o que me confirmes el nombre exacto del creador y la versión.

### 3.2 Oro y XP (piglins zombificados)
- **Mecánica en Bedrock:** un portal grande (23×23) que se enciende y se apaga rápido; los piglins caen a una zona de caída o a un matador con tridente. **[OK]**
- **Activación:** dispensador con encendedor y reloj de redstone, o lava sobre observers que actualizan trampillas. **[OK]**
- **Apagado:** dispensador con cubo de agua o de nieve polvo, con reloj. **[OK]**
- **Variantes en la wiki:** manual, de caída, de caída con "fall breaker" (da XP con espada de Looting) y automática con trident killer. **[OK]**
- **Datos de Java (no aplican):** Gnembon 130 bloques de oro/h automático y 600/h con Looting; DashPum4 1600/h; Nico is LOST/LonelyKat 750/h. **[Java]**
- **Nota:** la wiki marca esta página como desactualizada desde Java 1.21.5, por un cambio en el XP de los piglins zombificados enfadados.

### 3.3 XP de esqueletos (spawner) y mob grinder general
- Se considera la base de XP en Bedrock: barata, fiable y temprana. **[?]**
- La cámara de oscuridad general sirve para huesos, flechas, hilo, pólvora, etc.
- Mantenerla aislada, lejos de cuevas, y con la luz de alrededor controlada.

### 3.4 Pólvora (creeper)
- Plataforma de spawn con gatos para dirigir a los creepers. Pensada para cohetes y TNT.
- Dato que no pude verificar para Bedrock.

### 3.5 Enderman (perlas de ender y XP)
- Hay un tutorial marcado como "Java + Bedrock" (creador no confirmado). **[?]**
- Si se usa endermite con name tag, nombrarlo en un yunque antes de soltarlo. **[?]**
- Las granjas de baja altura suelen impedir el spawn de endermans.

### 3.5b Wither skeleton (calaveras, carbón, huesos)
- Se construye en una fortaleza del Nether sobre su caja de límites, con spawnproofing. **[OK]**
- En Bedrock rinde menos y es más sensible a la distancia de simulación. Los diseños simples suelen funcionar mejor que los "ultimate". **[?]**
- Un diseño de Java (Farmingchunk) habla de 570 calaveras/hora; no aplica a Bedrock. **[Java]**

### 3.6 Guardianes (XP, prismarina, pescado)
- Las reglas de spawn de guardianes difieren mucho entre Java y Bedrock. Probar un diseño hecho para Bedrock. **[?]**

### 3.7 Cultivos y comida
- **Trigo, zanahoria, papa, remolacha:** granja con aldeanos agricultores; funciona en Bedrock con diferencias pequeñas (pathfinding, recogida, hoppers). **[?]**
- **Melón y calabaza:** diseño con observers y pistones. Suele ser muy fiable.
- **Caña de azúcar y bambú:** observer + pistón + tolva. El bambú no necesita agua, pero su punta necesita luz ≥ 9. **[?]**
- **Cactus:** funciona en ambas ediciones, pero se pierden ítems si caen sobre otro cactus; usar canales de agua más anchos. **[?]**
- **Alga (kelp):** evitar diseños ultrarrápidos de Java; usar uno con observer. **[?]**
- **Aviso:** en Bedrock se necesita más superficie para el mismo resultado.

### 3.8 Árboles
- No investigado a fondo. Falta un diseño de Bedrock probado para tala automática.

### 3.9 Comercio con aldeanos
- Un "trading hall" ayuda a sacar libros de encantamiento y esmeraldas, pero es más difícil de montar en Bedrock. **[OK]**
- Lo ideal es que lo hagas tú dentro del juego, o que me pases una estructura que ya funcione.

### 3.10 Saqueos, abejas, slime, arena/grava, concreto
- No investigados. Quedan pendientes si los quieres.

---

## 4. Qué granjas se enlazan con el almacén

| Ítem del almacén | Granja que lo alimenta |
|---|---|
| hierro, lingotes, pepitas | hierro (golems) |
| oro, pepitas de oro, carne podrida | oro (piglins zombificados) |
| huesos, flechas, hilo, pólvora, arañas | grinder general / spawner |
| perlas de ender, ender eyes | enderman |
| calaveras, carbón | wither skeleton |
| trigo, zanahoria, papa, remolacha, melón, calabaza | cultivos |
| caña, bambú, cactus, alga | cultivos de torre |

---

## 5. Pistas de creadores (sin verificar la edición)

- **MushoDen** — granja de hierro (600+/h). **[?]**
- **@C.5.** — granja de oro y XP (1000+ bloques de oro/h; el creador y la edición no están claros). **[?]**
- **Shulkercraft** — trading hall. **[?]**
- **Vanished** — "la mejor granja de hierro Bedrock 1.21" (video en español/portugués). **[?]**
- **silentwisperer** — mob farm "split density" para 1.21. **[?]**
- **wattles** — creeper farm 1.21. **[?]**
- **aJack** — Iron Farm House 4.0, marcado Java/Bedrock. **[?]**

Recomendación: abrir el video de cada uno y comprobar que dice "Bedrock" y la versión antes de pedirme que lo coloque.

---

## 6. Plan de trabajo con tus granjas

### Qué me tienes que pasar
1. El mundo **actual** (`.mcworld`) justo antes de empezar. Si juegas entre medias, perderías esos cambios al sustituirlo.
2. Por cada granja a reemplazar: **dimensión**, **esquina mínima y máxima** (X Y Z). Así leo yo los bloques directamente del archivo.
3. El diseño nuevo como **`.mcstructure`** (o un mundo/addon donde esté construido). Yo no puedo descargar diseños de internet desde este entorno.
4. Qué granja quieres en cada hueco.

### Sobre el video
No puedo revisar videos de forma fiable. Las coordenadas sirven más: puedo extraer los bloques de tu mundo y ver qué hay. Si quieres, manda capturas como apoyo.

### Cómo lo hago
- Hago una copia del mundo, borro el área vieja, pego la estructura nueva y guardo un `.mcworld` nuevo. Es el mismo método que usé con el almacén.
- Aviso de qué cambié, con coordenadas.
- Una granja que no arranca no se arregla con el archivo: hay que probarla en el juego (aldeanos, camas, luz, límites de spawn).
- **Siempre haz copia de seguridad antes de abrir el mundo nuevo.**

---

## 7. Notas técnicas de lo ya hecho (para reproducirlo si se borra el chat)

### Almacén
- Estructura `almacen_salon.mcstructure`: tamaño 29×31×51 (X, Y, Z), guardada con origen 1950 62 1840.
- Colocada con su esquina en **1951 62 1840**. Ocupa X 1951–1979, Y 62–92, Z 1840–1890.
- Se borró lo que había desde Y=63 en X 1951–1987, Z 1840–1900. El suelo de Y=62 (tierra y pasto) se conserva donde la estructura no lo cubre.
- Se quitaron 4 tablones de roble sueltos del suelo viejo.
- Contenido: 540 cofres dobles (1080 cofres), 540 marcos, 35 letreros. Niveles Y = 63, 64, 65 (planta baja, Overworld) y 69, 70, 71 (piso alto, Nether/End).
- Archivos entregados: `far_default_nuevo.mcworld`, `catalogo_cofres.md`, `catalogo_cofres.csv`.
- Texture pack del mundo quitado (pesaba unos 4 MB; el peso real son los chunks, ~114 MB originales).

### Modelo de cantidades en los cofres
- Cantidad = tasa por día × 200 días × multiplicador de encantamiento × 0.6 (lo que sigue guardado).
- Fortuna III ×2.2 (minerales), redstone ×1.75; Looting III ×2.5 (mobs).
- Bloques compactados = 20 % del mineral / 9.
- Herramientas y armaduras: cantidades fijas pequeñas. Un elytra, un huevo de dragón, 6 beacons, 6 nether stars.
- Secciones: máximo 8 cofres por ítem; si se llena, otro cofre con el mismo ítem en el marco.
- Resultado: 377 cofres dobles llenos (233 ítems distintos), 163 libres.

### Cómo se edita el mundo (método)
- No había librería de LevelDB ni internet. Escribí un lector/escritor propio:
  - Lectura: `.ldb` (bloques con compresión raw zlib, tipo 4), `.log` y MANIFEST.
  - Escritura: tablas nuevas (~2 MB), todas en el nivel 3, comparador `leveldb.BytewiseComparator`, CRC32C enmascarado, `MANIFEST-013790`, `CURRENT`. Se reemplazan todos los archivos viejos.
- Subchunks (clave: x, z int32 LE + tag 47 + índice): versión 9, almacenamiento con paleta NBT little-endian. Orden de índice: `x*256 + z*16 + y`.
- Block entities: tag 49, NBT concatenados. Cofres con lista `Items` (Count, Damage, Name, Slot, WasPickedUp); marcos con compound `Item`.
- Entidades: digp y actorprefix (usados para quitar los tablones).
- Limitación: no pude abrir el resultado en Minecraft. Probar primero en una copia.

---

## 8. Fuentes consultadas

- Changelog Bedrock 26.60 (Nintendo Everything): https://nintendoeverything.com/minecraft-26-60-update-out-now-patch-notes/
- Changelog Bedrock 26.52 hotfix: https://feedback.minecraft.net/hc/en-us/articles/49175370527501-Minecraft-Bedrock-Edition-26-52-Hotfix-Changelog
- Preview 26.50.24 (formato mcstructure v2): https://www.minecraft.net/nb-no/article/minecraft-preview-26-50-24
- Wiki — Tutorial: Zombified Piglin farming (espejo, nov-2025): https://wiki.ronlab.site/content/minecraftwiki_en_all_maxi_2025-11/Gold_farm
- Wiki — Tutorial: Iron Golem farming: https://wiki.ronlab.site/content/minecraftwiki_en_all_maxi_2025-11/Iron_farm
- Wiki — Tutorial: Defeating the wither (techo del Nether en Bedrock): https://wiki.ronlab.site/content/minecraftwiki_en_all_maxi_2025-11/Tutorial%3ADefeating_the_wither
- Wiki — Tutorial: Wither Skeleton farming: https://wiki.ronlab.site/content/minecraftwiki_en_all_maxi_2025-11/Tutorials/Wither_Skeleton_farming
- Sportskeeda — iron golem spawning (Bedrock): https://sportskeeda.com/minecraft/minecraft-iron-golem-spawning-explained
- WiseHosting — mejores granjas 1.21+: https://wisehosting.com/blog/best-minecraft-farms-to-build-in-121
- Gamertag Mythras — granjas automáticas (cultivos Bedrock vs Java): https://gamertagmythras.com/blog/minecraft/minecraft-automatic-farms-guide
- Akliz — mejores mob farms vanilla: https://www.akliz.net/blog/posts/best-vanilla-mob-farms
- Minecraft.how — wither skull farm 2026: https://minecraft.how/blog/post/minecraft-wither-skull-farm
- xgamingserver — guía de fortalezas y de wither: https://xgamingserver.com/blog/minecraft-nether-fortress-guide/ y https://xgamingserver.com/blog/minecraft-wither-boss-guide/

Varias de estas fuentes son blogs con contenido de calidad desigual. Las que más peso tienen son la wiki y los changelogs oficiales.

---

## 9. Contabilidad del inventario al cambiar granjas (para no hacer trampa)

Idea: lo que se quita de las granjas viejas entra al inventario del almacén, y lo que cuesta la granja nueva sale de él. Así el almacén sigue siendo el de un survival real.

### 9.1 Qué se guarda en cada cambio (el "libro mayor")
Cuando se localice una granja y se escaneen sus chunks, antes de borrar nada se guardan tres archivos:
1. **`ledger_eliminado.csv`**: bloques de la granja vieja, contados por tipo (nombre + estados que importen) y por granja. Incluye los ítems dentro de contenedores (tolvas, cofres, barriles, hornos, dispensadores, goteros) y los ítems sueltos en el suelo.
2. **`ledger_nuevo.csv`**: bloques de la estructura nueva, contados igual (los contenedores nuevos salen vacíos).
3. **`ledger_ajustes.csv`**: qué se sumó o restó en cada cofre del almacén (coordenadas, ítem, cantidad antes y después).

Además se actualizan `catalogo_cofres.md` y `catalogo_cofres.csv`.

### 9.2 Cálculo (sumar, restar, multiplicar y dividir)
1. Pasar cada bloque o ítem a su **ítem real** (el que se obtiene al picarlo y el que hace falta para colocarlo).
2. Convertir todo a **unidades base** con las recetas reales: 9 lingotes = 1 bloque (×9 / ÷9), 1 tronco = 4 tablones (×4 / ÷4), 4 pepitas... etc.
3. `neto = recuperado − costo` por cada unidad base.
   - Si `neto > 0`: sobra material y se **suma** al cofre de ese ítem (o a una sección nueva si se llena).
   - Si `neto < 0`: falta material y se **resta** del almacén, empezando por la última sección del ítem.
4. Convertir el neto de vuelta al ítem del cofre (÷9, ÷4, etc.).

### 9.3 Reglas por defecto (confírmalas o cámbialas)
- **Recuperado** = lo que realmente se obtiene al picar con tus herramientas. Con Silk Touch, el bloque; sin él, el drop normal (la piedra da cobblestone, el cristal no da nada). No se recupera: agua, lava, aire, bedrock, spawners.
- **Costo** = un ítem por cada bloque colocado de la granja nueva.
- **Conversión entre materiales:** solo con recetas reales. Cobblestone → piedra cuesta combustible; por defecto no lo cobro, pero puedo descontarlo si quieres.
- **Faltantes:** si un material no alcanza en el almacén, queda en una lista de pendientes y decides: sustituir por un bloque equivalente, dejar hueco o conseguirlo tú.
- **Producción:** las granjas nuevas no regalan nada retroactivo. El almacén no se rellena de más por el rendimiento futuro.
- **Aldeanos y animales:** se trasladan, no se cuentan como material. Dime si quieres que los mueva o los borre.

### 9.4 Orden de trabajo
1. Backup del mundo.
2. Escanear la granja vieja y generar `ledger_eliminado.csv`.
3. Contar la estructura nueva y generar `ledger_nuevo.csv`.
4. Calcular el neto y mostrártelo **antes** de tocar el mundo, para que lo apruebes.
5. Hacer el intercambio (ver `intercambio_estructuras_bedrock.md`) y ajustar los cofres en la misma pasada.
6. Entregarte el mundo nuevo, el libro mayor y los catálogos actualizados.
