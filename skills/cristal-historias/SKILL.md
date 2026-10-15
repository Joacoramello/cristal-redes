---
name: cristal-historias
description: Historias de Instagram del día para Química Cristal - la secuencia placa por placa, qué sticker va dónde y el embudo que lleva a WhatsApp, incluida la preventa del camión. Usala para "historias de Cristal", "qué subo a las historias", "encuesta para historias", "no tengo nada para subir a historias", o vender algo de Cristal sin hacer un posteo.
---

# cristal-historias

Las historias no son un feed más chico. El feed es por donde te encuentran los que no te conocen. Las historias son donde los que ya te siguen deciden si comprarte, y es el único lugar de Instagram donde un toque se convierte en conversación en un solo paso.

Fuera de los seguidores casi nadie las ve, así que el trabajo es otro: profundidad, no alcance. Para un comercio, además, la historia diaria es la prueba de que está abierto.

## Antes de escribir

Cargá `cristal-marca`. Mirá el plan de la semana en el tablero (qué historia toca hoy) y si hay precio, Odoo.

## La forma del día

De 3 a 7 placas. Pasadas siete, sube el salteo y las últimas se reproducen para nadie, que es justo donde la gente pone el pedido.

```
1      LA APERTURA   algo que pasa hoy, con una cara o una mano: el camión cargándose,
                     la fábrica, el mostrador, un pedido saliendo.
2-3    EL MEDIO      el contenido: el proceso, el resultado, el error, el producto en uso.
4      EL PEDIDO     un sticker. Encuesta, caja de preguntas, quiz o link.
5      EL CIERRE     la respuesta, el resultado, o lo que viene mañana.
```

El pedido va en la placa 4, no en la 7.

## Material del día a día que ya existe (no hay que inventar nada)

- El camión cargándose el día antes de la salida, con el nombre del pueblo.
- Pedidos armados saliendo para reparto (sin datos del cliente a la vista).
- La fábrica: un bidón llenándose, un lote nuevo.
- El mostrador: la pregunta que hicieron hoy, contestada en una placa.
- Llegó mercadería nueva: el producto en la mano.
- La promo del mes en la vidriera, con el precio.

## Los stickers y para qué sirve cada uno

| sticker | trabajo | cuándo |
|---|---|---|
| **Encuesta** | el toque más barato que existe | querés volumen de respuestas, no información |
| **Caja de preguntas** | juntar las palabras exactas que usa la gente | necesitás ideas de contenido u objeciones textuales |
| **Quiz** | enseñar dejando que se equivoquen | hay un mito en el rubro (más cloro, más lavandina, mezclas) |
| **Link** | la única superficie con link además de la bio | hay un lugar real a dónde ir: el WhatsApp con mensaje precargado |
| **Cuenta regresiva** | una fecha a la que suscribirse | cierre de preventa del camión, fin de una promo, arranque de temporada |
| **Deslizador** | termómetro de ánimo | nada importante; divertido, de poco valor |

La caja de preguntas es la más subestimada. Cada respuesta es un caption, un hook o un mensaje escrito con las palabras del cliente. Pasáselas a `cristal-reel` como fórmula #16 (la pregunta textual).

## Reglas

- **Cara o mano en la primera placa.** Texto sobre fondo de color se saltea, y la primera decide si se ven las demás.
- **Una idea por placa.** Nadie lee un párrafo en una historia.
- **Texto en el medio:** en 1080x1920, nada arriba de y=250 ni abajo de y=1600. Arriba va el perfil y abajo la barra de respuesta.
- **Hablale a una persona.** "Vos", singular.
- **No compartas el posteo del feed sin decir nada.** Es la placa más ignorada de la plataforma. Si señalás un posteo, decí qué pasó y por qué vale volver.
- **Vender en historias, no en el feed:** tres placas de contexto, una de oferta con precio, una de prueba. Esa secuencia vende más que un posteo de lo mismo y no te cuesta alcance.
- **Precio a la vista** en la placa de oferta, de Odoo y del día.
- **Historias destacadas:** lo que sirve para siempre (cómo comprar, envíos, zonas del camión, piletas) se guarda en su destacada. Indicá cuál.

## El embudo, hecho bien

La secuencia que funciona: una historia que nombra un problema, una encuesta o caja de preguntas para que digan "me pasa", y después una respuesta a cada uno que contestó. La conversación arranca porque hablaron primero. **Ellos se mueven primero, después vos respondés.**

Para Cristal la respuesta deriva a WhatsApp con el mensaje precargado (lo atiende Claudio), no a una charla larga por Instagram. Las respuestas automáticas por palabra clave existen para cuentas profesionales, con las herramientas de Instagram o socios aprobados. Mandar mensajes a gente que no interactuó, no: es lo que restringe cuentas (ya pasó con dos números de WhatsApp).

## Preventa del camión (cuando toca salida)

Tres días antes de la salida y el día anterior:

1. El camión o el depósito, con el nombre del pueblo en pantalla.
2. Qué lleva: la promo "a reventar" de esa salida, con precio mayorista de Odoo.
3. Condiciones: pedido mínimo y envío según `negocio.md` (confirmadas con Joaco).
4. Cuenta regresiva al cierre de la preventa + link al WhatsApp con "Hola! Quiero hacer un pedido para el camión de {Pueblo}".
5. El día de la salida: el camión saliendo. Prueba de que el camión existe y va.

## Entrega

```
HISTORIAS · {día} · 5 placas

1  [video, mano cargando bidones al camión]   "Mañana el camión va a {{pueblo}}."
2  [foto, la promo en el depósito]            "Lavandina 5 L x 4 a {{precio Odoo}}."
3  [video corto, Joaco]                       "Pedidos hasta hoy a las 18."
4  [cuenta regresiva + link WhatsApp]         "Cierra la preventa"
5  [foto del camión + caja de preguntas]      "¿De qué pueblo sos? Te avisamos cuándo pasa."

Después: cada respuesta a la caja de la placa 5 recibe un mensaje con la fecha del pueblo.
Destacada: "Camión".
```

Todo el texto pasa por `cristal-humano`. Nada se sube: Joaco lo sube. Las historias no se anotan una por una en el tablero; si una tuvo una respuesta fuera de lo normal (muchas respuestas, pedidos), anotala como publicación con `formato: "historia"`.
