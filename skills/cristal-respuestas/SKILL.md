---
name: cristal-respuestas
description: Responde comentarios y mensajes directos que llegan a la cuenta de Química Cristal - los ordena (precio o pedido, palabra clave, mayorista, reclamo, pregunta, apoyo, ruido), responde con precios de Odoo y deriva a WhatsApp. Usala para "respondé estos comentarios", "me preguntaron el precio en el reel", "qué le contesto a este mensaje", "nos dejaron un comentario negativo". Si el mensaje es un pedido para cargar en Odoo, eso es asistente-pedidos-cristal.
---

# cristal-respuestas

Los comentarios del posteo propio son donde se decide el alcance y, para un comercio, donde están los compradores. Cada respuesta es otra interacción en el posteo, las de la primera hora hacen casi todo el trabajo, y un "¿precio?" sin responder es una venta que se fue al súper.

Pero no todos valen lo mismo, así que esta skill ordena antes de escribir.

## Antes de empezar

Cargá `cristal-marca`. Si hay preguntas de precio o stock, consultá Odoo **una vez** para todas (procedimiento en `negocio.md`): lista L.C 1 para consumidor final, Lista Mayorista si es revendedor. Ubicá la publicación en el tablero para saber qué promo, mensaje precargado y palabra clave tenía.

## Entrada

Joaco pega los comentarios o mensajes (con el @ si puede) o manda capturas. No se lee el hilo con un navegador para responder solo, y nada se publica desde acá.

## Ordenar primero

Cada comentario o mensaje a un grupo, y decí los conteos:

| grupo | qué es | qué recibe |
|---|---|---|
| **PRECIO / PEDIDO** | "¿precio?", "¿hacen envío a Holmberg?", "¿tienen el de 5 L?", "quiero uno" | respuesta pública con el dato (precio de Odoo, zona, stock) y la puerta a WhatsApp. **Primero de todo** |
| **PALABRA CLAVE** | la palabra que pidió el posteo | lo prometido, enseguida y sin vueltas |
| **MAYORISTA** | revendedor, almacén, emprendedor, "¿venden por mayor?" | respuesta corta y derivación al WhatsApp mayorista con mensaje precargado |
| **RECLAMO** | algo salió mal: producto, entrega, atención | respuesta pública breve, y lo resuelve Joaco por privado. Se le avisa **ya** |
| **PREGUNTA** | duda de uso que tienen muchos ("¿cuánto cloro le pongo?") | respuesta útil en público; si tiene demanda, se responde con un reel |
| **SUSTANCIA** | aporta, discute, cuenta su experiencia | la respuesta más larga del hilo |
| **APOYO** | "excelente", emojis, etiquetas | me gusta y de 3 a 8 palabras como mucho |
| **RUIDO** | spam, competencia, mala fe, cebos | nada, u ocultar si es ofensivo |

Escribí en ese orden y frená cuando se termine el valor.

## Cómo responder

- **Contestá lo que preguntaron, en público.** Si preguntan el precio, el precio. "Precio por privado" está prohibido: espanta, y el que lee el hilo después también quería saberlo. Si el precio depende de algo (cantidad, segmento, zona), se dice en una línea y se manda a WhatsApp.
- **La puerta a WhatsApp**: el botón del perfil o el link de la bio, con el mensaje precargado del posteo. "Te esperamos por WhatsApp (botón del perfil) con 'Quiero la promo de cloro' y te lo coordinamos." Plazos y envío, solo los de `negocio.md` (24 h hábiles; gratis solo desde el monto vigente). En Instagram los números escritos no se tocan; una vez, al final, sí puede ir.
- **El nombre una sola vez**, al principio, sin signo de exclamación.
- **Mismo largo que el comentario.** A cuatro palabras no se le contesta con cuatro renglones.
- **Cordial y prolijo**, nunca canchero ni vulgar: es la cara del negocio.
- **Nada de descuentos ni condiciones que no estén vigentes.** Si alguien negocia, a WhatsApp, donde decide Joaco.
- **A un reclamo:** reconocé lo concreto en una línea, en sus palabras, decí que lo resuelven por privado y avisale a Joaco con el detalle. No se discute en público, no se borra, no se responde dos veces en el mismo hilo.
- **A un troll o competidor:** nada. Una respuesta es alcance, y eso es lo que buscan. Si es ofensivo, ocultarlo: los controles de comentarios existen y usarlos no es perder.
- **A un mayorista:** reconocé el rubro ("Qué bueno que tengas almacén en {pueblo}."), una línea de qué hay (granel, mínimo, el camión) y al WhatsApp mayorista.

## La jugada que casi nadie hace

Si una pregunta en los comentarios es la que tienen otros treinta, **respondela con un reel**. Instagram pega el comentario al video nuevo como sticker, el que preguntó recibe un aviso, y una pregunta con demanda real se convierte en un posteo con el hook ya escrito. Marcá cada PREGUNTA que califique y pasásela a `cristal-reel` como fórmula #16.

## Palabra clave

Si el posteo pidió una palabra, esos comentarios son el punto del posteo: cada uno es alguien que levantó la mano. Se responde a cada uno y se manda lo prometido, **en el primer mensaje, sin condiciones** ("antes de mandártelo, ¿a qué te dedicás?" es un engaño y se recuerda). Si Joaco tiene configuradas respuestas automáticas con las herramientas de Instagram o un socio aprobado, que corran; si no, a mano está bien a este volumen. **Nunca** mandar mensajes a quien no comentó.

## Mensajes directos

El mismo orden. La diferencia: en privado se puede ir más al grano, pero el cierre es igual, **a WhatsApp**, porque ahí está el catálogo, los precios y quien carga el pedido (Claudio para mayorista y promos; si es un pedido de cliente institucional, Joaco). Plantilla:

```
{Nombre}, {respuesta concreta a lo que preguntó, con precio si aplica}.
Para pedirlo escribinos al WhatsApp {número de config/marca} con "{mensaje precargado}" y te lo coordinamos.
```

Si piden algo que no hay en stock, decilo y ofrecé el reemplazo (si es solo cambio de marca del mismo producto, se ofrece directo; si es otra cosa, se consulta a Joaco).

## Entrega

Un bloque, por grupo, cada respuesta lista para copiar y pasada por `cristal-humano`:

```
RESPUESTAS · reel "pileta verde" · 46 comentarios
9 PRECIO/PEDIDO · 21 PALABRA CLAVE · 2 MAYORISTA · 1 RECLAMO · 3 PREGUNTA · 8 APOYO · 2 RUIDO

PRECIO / PEDIDO   (precios de Odoo, L.C 1, hoy)
@usuario: "precio??"
> El combo de 6 kg está {{precio de Odoo}}. Escribinos por WhatsApp (botón del perfil) con
> "Quiero la promo de cloro" y te lo llevamos en 24 h hábiles. {{envío según el monto}}

RECLAMO   → avisarle a Joaco ahora: @usuario dice que el pedido del jueves llegó sin el alguicida.
@usuario: "..."
> Tenés razón, te faltó el alguicida. Te escribimos por privado para solucionarlo.

PREGUNTA → REEL
@usuario: "¿y si tengo pileta de lona?"  12 me gusta. Es un reel, no una respuesta. Fórmula #16.

RUIDO (2): sin responder. Uno ofensivo: ocultalo.
```

Nada se publica hasta que Joaco diga que sí: él pega las respuestas. Si hubo PRECIO/PEDIDO o PALABRA CLAVE en cantidad, sumalo como nota en la publicación del tablero (sirve para la auditoría).
