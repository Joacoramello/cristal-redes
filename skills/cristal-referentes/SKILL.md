---
name: cristal-referentes
description: Investiga qué hacen otras cuentas del rubro (químicas, limpieza, piletas, comercios de Córdoba) - rankea sus reels por cuánto le ganó cada uno a su propia cuenta, nombra la fórmula de hook y lo convierte en hooks que Cristal puede grabar. Usala para "qué hacen otras cuentas del rubro", "buscá videos virales de limpieza o piletas", "analizá esta cuenta ajena", "armá referentes para Cristal", "por qué explotó este reel de otro".
---

# cristal-referentes

La skill de investigación. Las demás escriben; esta mira. Una vez por mes, no todos los días: las fórmulas duran una temporada.

Una herramienta vive en esta carpeta (con su propia copia de `hookscore.py` y `hooks.json`):

```bash
python3 <carpeta>/swipe.py capturados.tsv --md referentes.md
```

## La única idea que hace que esto valga la pena

**Las vistas solas no prueban nada.** Una cuenta de dos millones que hace 400 mil vistas tuvo un martes tranquilo. Una de cuatro mil que hace 400 mil encontró algo, y ese algo se puede copiar.

Todo se ordena por el **múltiplo**: vistas divididas por la mediana reciente de esa misma cuenta. Arriba de 3x es señal. Abajo de 1,5x es un día normal de esa cuenta y no enseña nada, por grande que se vea el número.

Elegí cuentas de hasta unas **10 veces el tamaño de Cristal**. Una fórmula que funciona con dos millones de seguidores muchas veces funciona porque tiene dos millones.

## Paso 1: elegir las cuentas

Pedile a Joaco de 6 a 12 cuentas, o proponé categorías y pedí que él elija (no inventes @):

- **4 directas**: químicas, distribuidoras de limpieza, casas de piletas, de Argentina, un poco más adelante que Cristal.
- **4 adyacentes**: otro rubro, mismo público. Ferreterías, viveros, bazares, mantenimiento de piletas, limpieza profesional. De acá salen formatos antes de que los tenga el rubro.
- **2 a 4 grandes**: cuentas mucho más grandes de limpieza ("cleantok" en español), solo por el formato, nunca por la frecuencia ni el tono.

Pedile también que abra sus **Guardados** de Instagram: es el corpus más rápido y ya está filtrado por su gusto.

## Paso 2: ir a mirar

Usá el navegador que haya en esta sesión (Claude in Chrome o el navegador de la app de escritorio), con Joaco presente y su sesión. No hay API para esto y no hace falta: el volumen es chico.

**Reglas que no se negocian:**

- **Nunca iniciar sesión por Joaco ni pedirle la contraseña.** Si una página pide login, él es el que ya está logueado.
- **Esto es leer, no scrapear.** Diez cuentas, una docena de reels cada una, a velocidad humana. Juntar automáticamente en volumen viola los términos de Instagram y restringe cuentas. Nada de crawlers, servicios de scraping ni procesos en segundo plano.
- **Se copia la fórmula, nunca el video.** La forma del hook, la estructura, el largo, el ritmo de cortes. No el guion, ni la voz, ni la edición. Cada fila con su cuenta de origen.

Si no hay navegador, que Joaco pegue los datos o mande capturas.

**Qué anotar por reel** (con las palabras del creador):

| campo | nota |
|---|---|
| cuenta | el @ |
| seguidores | del perfil |
| mediana | mirando los últimos 12 reels, el del medio en vistas |
| vistas | este reel |
| hook | la primera línea hablada, textual, con errores incluidos |
| en pantalla | el primer texto que aparece, si es distinto del hablado |
| formato | reel, carrusel |
| largo | segundos |
| cta | qué pidió al final |

La mediana es lo importante. Sin ella se vuelve a ordenar por seguidores, que es justo lo que esto viene a evitar.

**Si Instagram no muestra lo suficiente:** la misma gramática de hooks corre en YouTube Shorts, donde las vistas son públicas y no hace falta login. Es un segundo corpus legítimo: mirá la pestaña Shorts del canal en el navegador (vistas de cada uno) y anotá la primera frase de cada video. Desde el entorno de trabajo de Claude YouTube no suele estar al alcance (la red está restringida), así que no cuentes con `yt-dlp` acá; si Joaco lo tiene en su computadora, sirve: `yt-dlp --flat-playlist -J "https://www.youtube.com/@CANAL/shorts"` da las vistas, y `--write-auto-subs --sub-langs "es.*" --skip-download` los subtítulos, de los que el hook son las palabras de antes de los 3 segundos.

## Paso 3: rankear

Llená un TSV con encabezado (acepta `k` y `mil`: "18k", "3.000") y corré el script:

```
cuenta	seguidores	mediana	vistas	hook	en_pantalla	formato	largo	cta
@alguien	4800	1200	38000	nadie te dice que la lavandina se vence	SE VENCE	reel	24	comentá LAVANDINA
```

```bash
python3 <carpeta>/swipe.py capturados.tsv --md referentes.md
```

Calcula el múltiplo, nombra la fórmula con las mismas 30 de `cristal-reel`, puntúa cada hook y muestra qué separa el tercio de arriba del de abajo.

## Paso 4: decir qué significa, con cuidado

Tres cosas y nada más:

1. **Qué fórmulas aparecen de más** en el tercio de arriba, con cantidades. Dos fórmulas que aparecen cuatro veces cada una en seis cuentas es un hallazgo. Una que aparece dos veces, no.
2. **Qué tiene en común el tercio de arriba** que no tiene el de abajo: largo del hook, si el resultado es visual, si el primer cuadro se mueve, dónde está el pedido.
3. **Los sin clasificar.** Cada hook que el clasificador no reconoce es ruido o una fórmula que todavía no está en `hooks.json`. Leelos a mano: es la columna más valiosa. Si aparece una fórmula nueva dos o más veces, proponela para la próxima versión de `hooks.json`.

Después decí el tamaño de la muestra y la confianza, en palabras. Cuarenta reels en seis cuentas sostienen algo. Doce no, y decirlo es la diferencia entre investigar y leer el horóscopo.

## Paso 5: convertirlo en algo para grabar

Para las tres fórmulas de arriba, escribí **la versión de Cristal**: su producto, su mostrador, su número real (o `{{dato}}`), con la forma que funciona. Pasáselas a `cristal-reel` con la fórmula ya elegida.

Nunca "hacé un reel como este". Una línea de hook que Joaco podría decir mañana en el local.

## Guardar

Con el OK de Joaco, guardá cada reel en la colección `referentes` del tablero (con `fecha_captura` y `multiplo`), en un solo `batch`. `cristal-reel` y `cristal-plan` lo leen: después de esto el resto del paquete trabaja con evidencia del rubro y no con reglas por defecto.

Nada se publica, sigue, likea ni manda desde esta skill. Solo lee.
