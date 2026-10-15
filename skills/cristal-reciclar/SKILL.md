---
name: cristal-reciclar
description: Convierte un material largo de Química Cristal en una semana de reels, carruseles e historias - un video grabado, un anuncio viejo, una charla de mostrador, una visita a un cliente, un audio de WhatsApp, un catálogo o una ficha técnica. Usala para "reciclá esto", "sacale posteos a este video", "tengo este audio, hacé contenido", "pasá el catálogo a redes", "cortá este video en reels".
---

# cristal-reciclar

Un buen material largo tiene adentro de cuatro a seis posteos. Casi todos sacan uno y tiran el resto.

## De dónde sale material en Cristal (sin grabar nada nuevo)

- **Anuncios viejos que funcionaron**: los videos de Joaco en el local. (Los del empleado que ya no está, AD18 y AD20, **no** se usan.)
- **Un audio o una charla**: Joaco explicándole algo a un cliente, a un empleado nuevo o a Claude. Pedile que grabe 10 minutos contando cómo se prepara una pileta para la temporada y salen cinco posteos.
- **Preguntas reales** que llegaron por WhatsApp o al mostrador (sin datos del cliente).
- **Fichas técnicas y catálogos**: diluciones, rendimientos, usos. Son tablas y carruseles listos.
- **Una visita** de Alejandra o una entrega grande (con permiso del cliente para mostrar algo).
- **Un día de fabricación** grabado de corrido en el celular.

## Entrada

Una transcripción, un audio, un video, un PDF o el texto. Si es un video o audio propio, pedí el archivo además: un reel con la imagen real le gana a uno con las mismas palabras regrabadas. Si es un archivo de video, podés sacar la transcripción y los fotogramas con las herramientas del entorno (ffmpeg si está) para ubicar los momentos. Leé todo antes de sacar nada.

Cargá `cristal-marca` y mirá en el tablero qué se publicó las últimas semanas para no repetir.

## Extraer, no resumir

El resumen de un video no es un reel. Nadie quiere el resumen. Recorré el material y sacá lo que se sostiene solo:

| qué | qué es |
|---|---|
| **Afirmaciones** | cada frase que arrancaría una discusión ("más cloro no arregla la pileta verde") |
| **Números** | precios, litros, diluciones, tiempos, años |
| **Historias** | cada momento con una persona, una escena y un costo |
| **Mecanismos** | cada "lo que pasa en realidad es..." |
| **Errores** | cada cosa que salió mal y se admitió |
| **Frases** | cada oración citable tal como está |
| **Preguntas** | cada pregunta de un cliente, textual |

Listá lo que encontraste, con cantidades, antes de escribir nada. Si salen menos de cuatro cosas, el material es flaco y cuatro posteos sacados de ahí van a ser flacos también: decilo.

Revisá cada número y cada dosis contra Odoo o la etiqueta antes de usarlo: lo que alguien dijo de memoria en un audio puede estar mal.

## Formato por extracto

No todo es un reel.

- **Afirmación, error, historia** → reel. Necesitan voz y cara.
- **Mecanismo, lista, tabla, dilución** → carrusel. Se releen.
- **Frase citable, pregunta textual** → placa de historia, no posteo.

## Armar la semana

Cada extracto es un posteo y cada posteo se sostiene solo: el que mira nunca vio el original y nunca lo va a ver. Nunca "como dije en el video anterior".

A cada uno, una fórmula de `hooks.json` de cristal-reel (carpeta hermana: `<carpeta>/../cristal-reel/hooks.json`; si no está, cargá `cristal-reel` y usá su "Base directory"), y que varíen. Cinco posteos de un mismo material con la misma forma de hook se leen como fábrica de contenido, porque lo son.

Si el material es video propio, **usá la imagen real**: el momento en que Joaco lo dijo, con la reacción verdadera, le gana a regrabarlo. Cortá en la frase, no en la respiración.

Orden: la afirmación más fuerte primero, la historia a mitad de semana, el mecanismo al final, cuando los que vieron los anteriores lo están esperando.

## Entrega

```
MATERIAL: audio de Joaco sobre preparar la pileta (11 min, ~1.600 palabras)

ENCONTRÉ  4 afirmaciones, 7 números, 2 historias, 3 mecanismos, 1 error, 5 frases, 3 preguntas

SEMANA
MAR  REEL      #28 El mito             "Más cloro no te arregla la pileta verde"
                                       usar 3:40 del audio sobre imagen de la pileta
JUE  CARRUSEL  tabla                   "Cloro por litros de pileta" (dosis de la etiqueta del granulado)
SÁB  REEL      #21 A mitad de frase    "...y era el pH, no el cloro" (la historia de la clienta, sin nombre)
HISTORIA       pregunta textual        "¿Cuánto tarda en aclarar?" como caja de preguntas el viernes

Decime "escribí el martes" y lo armo.
```

Después escribí de a uno cuando lo pida, cada uno con `cristal-reel` o `cristal-carrusel` y `cristal-humano`. No entregues cuatro guiones terminados juntos: van a sonar iguales y no se va a grabar ninguno. Si Joaco aprueba la semana, anotá los posteos en el tablero como `planificado`.
