---
name: cristal-carrusel
description: Carruseles de Instagram para Química Cristal - la portada que se gana el deslizar, el texto placa por placa y las imágenes 1080x1350 listas para subir, en la paleta de la marca. Usala para "carrusel de Cristal", "placas", "posteo de varias fotos", "pasá esto a carrusel", o una idea de pasos, tabla o lista de Cristal que como imagen sola se pierde.
---

# cristal-carrusel

El carrusel es el formato de la grilla que más tiempo retiene, porque deslizar es una interacción y pasar no. Además tiene segunda oportunidad: Instagram puede volver a mostrarlo arrancando desde una placa posterior a quien no interactuó la primera vez, así que la placa 2 también tiene que valer sola.

Premia una idea partida en pasos. Castiga un caption cortado en pedazos.

Una herramienta vive en esta carpeta:

```bash
python3 <carpeta>/render_carrusel.py carrusel.json --out placas/ --hoja
```

Arma las placas en PNG de 1080x1350 con Pillow (sin navegador) y una hoja de contactos para revisar todas juntas. Mínimo de letra 32 px, márgenes de 120 px, numeración 3/8 y el @ en cada placa. Si un texto no entra, achica la letra y avisa en vez de cortarlo.

## Antes de escribir

Cargá `cristal-marca`. De `config/marca` salen el `handle` y la `paleta`; si no están, la paleta provisoria de `marca.md` y el @ se pide (sin @ las placas salen sin firma y el script avisa). Si hay precios, Odoo con el procedimiento de `negocio.md`.

## Cuándo carrusel y cuándo reel

Carrusel cuando la idea tiene **secuencia y se relee**: pasos, una tabla para guardar (cloro por litros de pileta, diluciones de la etiqueta), un antes y después en fotos, una lista que se captura. Reel cuando la idea tiene movimiento, cara o un resultado que hay que ver pasar (la grasa saliendo, la pileta aclarando).

Si la idea es una sola afirmación, no es ninguno de los dos: va a `cristal-reel` y decilo.

## Ideas que en Cristal funcionan como carrusel

- La tabla: dosis de cloro por litros de pileta, con el producto que vende Cristal y lo que dice su etiqueta.
- La cuenta: precio del bidón, dilución, litros que hace, precio por litro contra la alternativa del súper.
- Los 5 errores al limpiar {campana / pileta / pisos / ropa blanca}.
- Kit para {bar / colegio / consorcio / almacén que arranca}: qué lleva y cuánto rinde.
- Cómo comprar: WhatsApp, zona de envío, mínimo para envío gratis, horario, días del camión. (Es el carrusel fijado de "cómo comprar").
- Quiénes somos: el local, la fábrica, 20 años, Joaco. (El fijado de presentación).

## Estructura

De 6 a 10 placas. El tope es 20 y 20 es casi siempre un libro que nadie termina. Menos de 5 y el deslizar no arranca.

```
1          PORTADA   el hook. 6 palabras o menos, legible en la miniatura de la grilla.
                     Una línea de promesa abajo.
2          LO QUE ESTÁ EN JUEGO   por qué importa, en una oración. También es una segunda
                     portada: no puede ser preparación.
3 a N      UNA IDEA POR PLACA. Título de 3 a 7 palabras, como mucho 25 palabras abajo.
                     Si una placa necesita un párrafo, son dos placas.
N+1        RESUMEN   todo en una lista. Es la placa que se captura y se manda.
ÚLTIMA     PEDIDO    una acción: guardalo, mandáselo a alguien, o escribinos por WhatsApp.
```

## Reglas del texto

- **La portada es el 80 % del resultado.** Seis palabras, grandes. Pasala por `hookscore.py` de cristal-reel (`<carpeta>/../cristal-reel/hookscore.py`) si querés un segundo control: la portada es un hook.
- **Numeradas** (el script lo hace). Cuando se ve el final, se termina más.
- **Ninguna placa es un párrafo.** Más de 25 palabras: partila (el script avisa).
- **La placa de resumen** se lee sola, sin contexto. Los envíos son la señal más fuerte que se puede ganar.
- **Precios** con el formato argentino y la fuente (Odoo, hoy). Si el carrusel puede vivir meses fijado, mejor sin precio en la imagen: el precio va en el caption, que se edita.
- **Seguridad**: dosis y diluciones solo de la etiqueta; ninguna mezcla.
- **Texto alternativo** al menos en la portada.

## Armar las imágenes

1. Escribí el texto placa por placa y mostráselo a Joaco como lista numerada que se lee en diez segundos. **Las imágenes se arman recién con su OK al texto.**
2. Pasá el texto por `cristal-humano`.
3. Armá `carrusel.json` en tu carpeta de trabajo:

```json
{
  "marca": {"oscuro": "#0E3B5C", "claro": "#F3F8FB", "acento": "#16A6D9",
            "texto_oscuro": "#0B1F2E", "texto_claro": "#FFFFFF", "handle": "@..."},
  "slides": [
    {"tipo": "portada", "titulo": "LA LAVANDINA SE VENCE", "bajada": "Y casi nadie lo sabe."},
    {"tipo": "idea", "titulo": "El sol le saca el cloro", "cuerpo": "Al sol pierde fuerza en semanas."},
    {"tipo": "lista", "titulo": "Guardala así", "items": ["A la sombra", "Bien cerrada"]},
    {"tipo": "resumen", "titulo": "Todo junto", "items": ["...", "..."]},
    {"tipo": "cta", "titulo": "Guardalo", "cuerpo": "Y mandáselo al que hace las compras."}
  ]
}
```

   Tipos: `portada` (fondo oscuro, título grande), `idea` (título + cuerpo), `lista` y `resumen` (título + ítems numerados), `cta` (fondo oscuro). La `marca` sale de `config/marca`.
4. Corré `render_carrusel.py` con `--hoja`. Mirá la hoja de contactos (con Read) y arreglá lo que avise el script. Una sola vuelta de revisión.
5. Mandá las placas con SendUserFile (todas las PNG, en orden), más el caption.

Si Joaco tiene un diseño propio o fotos reales del producto, el script no las reemplaza: en ese caso entregá el texto y que lo arme él, o pedí las fotos y armá placas de foto + título.

## Entrega

```
CARRUSEL · {segmento} · 8 placas

1  PORTADA   LA LAVANDINA SE VENCE
             Y casi nadie lo sabe.
2  EN JUEGO  Guardada al sol, en pocas semanas limpia menos.
3            ...
7  RESUMEN   Las 4 reglas, juntas.
8  PEDIDO    Guardalo y mandáselo al que hace las compras.

Caption: trabajo B (cristal-caption), hook en la línea 1, un pedido, 3 hashtags.
Texto alternativo de la portada: ...
```

Después del OK y del armado, anotá la publicación en el tablero con `formato: "carrusel"` y `estado: "listo"`. Nada se sube: lo sube Joaco.
