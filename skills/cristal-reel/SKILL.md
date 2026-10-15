---
name: cristal-reel
description: Guiones de reels (Instagram, TikTok, Shorts) para Química Cristal - tres hooks puntuados de 30 fórmulas del rubro, guion en voseo, texto en pantalla y hoja de tiempos, con precios de Odoo. Usala para cualquier reel o video de Cristal y para cualquier reel de limpieza, pileta, cloro, lavandina, promo, camión o mostrador aunque no diga Cristal ("hacé un reel de la pileta verde", "guion de la promo", "qué digo en este video"). Para la marca personal de Joaco u otros temas, reel-creator.
---

# cristal-reel

Convierte una idea en un reel de Química Cristal que alguien mira hasta el final y que termina en un WhatsApp.

Dos herramientas viven en esta carpeta y funcionan de verdad. Usalas: no evalúes el hook a ojo ni adivines el largo.

```bash
python3 <carpeta>/hookscore.py hooks.txt               # rankea los hooks (uno por línea)
python3 <carpeta>/hookscore.py --hook "una línea"       # puntúa uno solo
python3 <carpeta>/beats.py guion.txt --target 30        # hoja de tiempos antes de grabar
```

`<carpeta>` es la "Base directory" que te da la herramienta Skill al cargar esta skill. Los archivos de trabajo (hooks.txt, guion.txt) escribilos en tu carpeta de trabajo, no en la de la skill.

## Antes de escribir

1. **Cargá `cristal-marca`** y leé `marca.md`, `negocio.md` y `config/marca` del tablero. La voz es la de Joaco hablando en el local: si el guion no lo diría él, no sirve, porque lo tiene que decir en voz alta.
2. **Leé `hooks.json`** de esta carpeta: 30 fórmulas con plantilla, ejemplo del rubro, versión en pantalla, para qué sirve, cómo se arruina y para qué segmentos. Las 27 a 30 son propias del rubro (la cuenta, el mito, detrás de escena, precio en pantalla).
3. **Leé el tablero**: las publicaciones de las últimas dos semanas (no repetir fórmula ni tema) y los `referentes` (si hay, son la evidencia de qué funciona en el rubro ahora y mandan sobre las fórmulas por defecto).
4. **Definí segmento y pedido.** Un reel es para un segmento (consumidor final, mayorista, ruta camión, gastronómicos/institucional) y termina en una acción. Si Joaco no lo dijo, preguntalo junto con lo que falte, en una sola tanda.
5. **Si la idea es flaca, no la rellenes.** Un reel necesita una cosa concreta y verdadera: qué pasó, con qué producto, cuánto costó o rindió. Preguntá eso antes de escribir.
6. **Si hay precio o producto**, consultá Odoo (procedimiento en `negocio.md`): precio de la lista que corresponde al segmento y stock. Sin consulta, el guion lleva `{{precio}}`.

## La forma

Un reel se decide en los dos primeros segundos y se sostiene en los cinco siguientes.

```
0:00 - 0:02   HOOK      la afirmación. Línea hablada y línea en pantalla, escritas por
                        separado. Movimiento en el primer cuadro: la mano echando el
                        producto, el bidón entrando a cuadro, la grasa. No una cara quieta.
0:02 - 0:07   LO QUE ESTÁ EN JUEGO   por qué le importa al que mira. Una línea.
0:07 - ...    EL CUERPO una idea por bloque, y el plano cambia en cada bloque.
ÚLTIMOS 3s    EL PAGO   lo que prometió el hook, y el único pedido.
ÚLTIMA LÍNEA  EL LOOP   repetí una palabra del hook para que la segunda vista cierre.
```

Largo: entre 15 y 45 segundos. A 150 palabras por minuto: 30 s ≈ 75 palabras, 45 s ≈ 110. Para el formato "precio en pantalla" (candidato a anuncio), 15 a 25 segundos.

## Formatos que sirven para Cristal

Elegí uno y decí en una línea por qué encaja.

| Formato | Estructura | Largo | Segmento típico |
|---|---|---|---|
| **Antes y después** | Plano sucio → producto en acción → plano limpio, misma luz y encuadre. La palabra va de subtítulo | 15-25 s | todos |
| **Demo en frío** | Arranca con la mano ya trabajando. Resultado visible antes del segundo 5 | 15-30 s | gastronómicos, CF |
| **La cuenta** | Precio del bidón → dilución de la etiqueta → litros que hace → precio por litro contra el súper. Números en pantalla | 25-40 s | CF, mayorista |
| **El mito** | Creencia → "falso" → por qué, en una frase → qué hacer en su lugar | 20-35 s | CF |
| **Pregunta del mostrador** | La pregunta textual como llega → respuesta corta → tabla o dato para guardar | 20-40 s | CF |
| **Detrás de escena** | Fábrica o depósito, proceso en planos cortos, cero receta | 20-40 s | mayorista, todos |
| **Precio en pantalla** | Joaco en el local con el cartel: producto, precio, qué trae, cómo pedirlo. El formato que ganó en la pauta | 15-25 s | CF, ruta camión |
| **Lista con favorito** | "Tres que todo bar necesita, el tercero casi nadie lo tiene" | 30-45 s | gastronómicos, institucional |
| **Llamado al grupo + preventa** | "Si tenés almacén en {pueblo}..." → qué lleva el camión → fecha de cierre | 20-30 s | ruta camión, mayorista |

## El proceso

**1. Tres hooks, no uno.** Elegí tres fórmulas distintas de `hooks.json` que de verdad encajen con la idea y escribí para cada una la línea hablada y la de pantalla. Tres fórmulas distintas, no tres versiones de la misma.

**2. Puntuarlos.** Las tres líneas habladas en un archivo, una por línea, y `hookscore.py`. Mostrá el ranking. Si el primero está abajo de 50, todavía no hay hook y editar no lo arregla: cambiá de fórmula o pedí el dato concreto que falta. El puntaje caza saludos, preámbulos, tuteo, hooks sin nada concreto y hooks largos; no predice cuál de dos hooks buenos va a funcionar. Decilo así si Joaco pregunta.

**3. Escribir el guion** con el hook ganador. Lenguaje hablado, como habla Joaco, frases cortas, nada que haya que ensayar.

**4. Cronometrarlo.** `beats.py guion.txt --target {segundos}` (con `--wpm` si `config/marca` tiene `ritmo_ppm`). Arreglá cada aviso: hook de más de 3 s, bloques de más de 4 s, rachas sin nada concreto, falta de loop. Volvé a correrlo hasta que salga limpio.

**5. Humanizarlo.** Pasá el guion por `cristal-humano` antes de mostrarlo. Una línea que suena escrita se nota apenas alguien la dice.

**6. Entregar** con el formato de abajo.

**7. Anotar.** Si Joaco dice que sí, guardalo en `publicaciones` del tablero con `estado: "listo"` (fecha prevista, formato, segmento, `pilar` de la lista del tablero, `formula_id` y `formula`, `largo_s` que dio `beats.py`, hook, en pantalla, cta, mensaje de WhatsApp, producto y precio si hay). Nada se publica: él lo graba y lo sube.

## Texto en pantalla (es un guion aparte)

- **Seis palabras o menos por placa.** Se lee a un brazo de distancia, por alguien que todavía no está escuchando.
- **La placa del hook está en el cuadro 1**, no después de un silencio.
- **Zona segura en 1080x1920:** nada arriba de y=230 ni abajo de y=1440, y los 230 px de la derecha libres (ahí van la descripción, los botones y el audio).
- **Subtítulos quemados en el cuerpo.** La mayoría mira sin sonido la primera vez.
- **Precios en pantalla con el formato argentino**: $12.500, no 12500 ni $12,500.

## Reglas que hacen la diferencia

- **Una idea por reel.** Si el guion tiene dos, son dos reels. Decilo.
- **Números antes que adjetivos.** Si no hay número, se pide; no se escribe alrededor del hueco.
- **Sin intro.** Sin "hola", sin "en este video", sin logo animado. El video empieza en la frase del segundo seis.
- **El plano cambia en cada bloque.** Un plano quieto de 8 segundos es donde la gente se va.
- **Un solo pedido al final**, y siempre el mismo camino: el WhatsApp que atiende, con el mensaje precargado de este video (o la palabra clave para comentar, si está configurada). Si el mensaje precargado es nuevo, avisá a Joaco para que lo sume al filtro de Claudio.
- **Nada inventado.** Ni cifras, ni clientes, ni resultados. `{{dato}}` y aviso.
- **Seguridad:** guantes en cámara con lavandina, cloro o ácidos; ninguna mezcla; diluciones solo de la etiqueta.
- **Audio en tendencia:** solo si el reel funciona igual sin la voz de Joaco. Si la idea necesita su voz, va su voz.

## Notas de grabación (incluilas siempre)

3 a 5 puntos concretos: qué se ve en cada bloque, plano detalle de la mano y el producto, misma luz para antes y después, dónde va el cartel de precio, celular vertical a la altura de los ojos, sonido del local controlado.

## Formato de entrega

```
REEL · {segmento} · {formato}

HOOKS (puntuados)
  {puntaje} {FUERTE/ZAFA/FLOJO}  #{id} {fórmula}   "{línea hablada}"
                                                  pantalla: {LÍNEA EN PANTALLA}
  ...
Grabamos el #{id}: {por qué, en una línea}.

GUION ({segundos} s, {palabras} palabras)
{el guion, un bloque por línea}

EN PANTALLA
  0:00  {placa}
  ...

PEDIDO: {acción} → WhatsApp con "{mensaje precargado}"
PRECIO: {precio} (Odoo, lista {lista}, consultado hoy · stock {n})   ← si aplica

NOTAS DE GRABACIÓN
  - ...

LISTO PARA GRABAR
hook:        #{id} {fórmula}, {puntaje} {veredicto}
largo:       {s} s en {n} bloques a {ppm} ppm, sin avisos
humanizador: {n} marcas sacadas, {puntaje} {PASA}
caption:     seguí con cristal-caption

¿Lo anoto en el tablero como listo para grabar?
```

## Ejemplo

```
/cristal-reel la gente cree que si la pileta está verde le falta cloro
```

```
HOOKS (puntuados)
  87  FUERTE  #28 El mito                 "Más cloro no te arregla la pileta verde."
                                         pantalla: MÁS CLORO NO
  80  FUERTE  #16 La pregunta textual     "¿Cuánto cloro le pongo si está verde? Nos lo preguntan todos los días."
                                         pantalla: ¿CUÁNTO CLORO LE PONGO?
  79  FUERTE  #10 Si te pasa esto, mirá  "Si tu pileta amaneció verde, no la vacíes. Mirá esto."
                                         pantalla: ¿PILETA VERDE?
Grabamos el #28: es el más corto, contradice lo que cree el que mira y abre con la mano
echando cloro al agua verde, que es movimiento en el cuadro 1. El #16 queda para un
segundo reel: la pregunta textual sirve para que lo encuentren en el buscador.
```
