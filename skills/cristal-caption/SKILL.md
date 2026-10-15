---
name: cristal-caption
description: Captions de Instagram y Facebook para Química Cristal - la línea que sobrevive al corte del "más", un solo pedido, precio visible en promos, la ciudad para búsqueda local y hasta 5 hashtags, revisado por script. Usala para "caption de Cristal", "qué pongo en la descripción", "texto del posteo", o un reel/carrusel/foto de Cristal que necesita texto, o dudas de hashtags.
---

# cristal-caption

Una herramienta vive en esta carpeta y funciona:

```bash
python3 <carpeta>/caption.py caption.txt --local "Río Cuarto"
python3 <carpeta>/caption.py caption.txt --local "Río Cuarto" --keywords "cloro para pileta,pileta verde"
python3 <carpeta>/caption.py caption.txt --oferta          # post de promo: exige precio visible
```

Imprime el caption como lo muestra el feed: los primeros 125 caracteres en una caja y el resto detrás del toque. Leé esa caja antes que cualquier otra cosa que escribiste.

## Antes de escribir

Cargá `cristal-marca` (voz, segmentos, `config/marca`). Si el posteo tiene precio, consultá Odoo con el procedimiento de `negocio.md`: el precio del caption tiene que ser el mismo que el del video o la placa, de la lista del segmento, consultado hoy.

## Primero: qué trabajo hace este caption

Es la decisión que más captions arruina cuando se saltea.

**Trabajo A: el video ya enganchó.** Un reel trae su hook hablado y en pantalla en los dos primeros segundos. El caption no es un segundo hook, y competir con el video es perder los dos. Su trabajo: el pedido, el contexto que hace que el pedido tenga sentido, y las palabras que la gente busca.

**Trabajo B: el caption es el contenido.** Una foto, una placa, la portada de un carrusel. Acá la primera línea es el hook y funciona igual que el de un reel: concreta, corta, y cortada en una intriga, no a mitad de una subordinada.

Decí cuál estás escribiendo y por qué.

**Promo (cualquier formato):** el precio y lo que incluye van en la primera línea, siempre. "Combo cloro 6 kg a {{precio de Odoo}}. Envío gratis en Río Cuarto." (Lo del envío gratis, solo si ese precio llega al monto mínimo de `negocio.md`; si no, la condición real.) Corré el linter con `--oferta`.

## La forma

```
Línea 1    ~125 caracteres visibles. Trabajo A: el pedido, claro. Trabajo B: el hook.
           Promo: producto + precio. Nunca un saludo, un hashtag ni un emoji de entrada.
Cuerpo     párrafos cortos, una línea en blanco entre cada uno. De dos a seis.
           Acá van las palabras de búsqueda y la ciudad.
El pedido  uno solo: escribinos por WhatsApp (botón o link de la bio) con el mensaje
           precargado, comentá la palabra clave, o guardalo.
Hashtags   hasta cinco, en su línea al final, o ninguno.
```

El límite es 2.200 caracteres y casi nada necesita eso. Un caption que se gana el toque y entrega 600 caracteres le gana a uno de 1.800.

## Hashtags, sin vueltas

Instagram limitó los hashtags a **cinco por posteo** el 18 de diciembre de 2025 (antes eran 30), y ya había dicho que no son una palanca de alcance sino una etiqueta. Entonces: de cero a cinco, específicos, como etiqueta del tema. Uno local (#riocuarto) y tres o cuatro del tema (#piletas #limpiezadepiletas #productosdelimpieza). `#viral`, `#parati`, `#fyp`, `#argentina` no describen nada: afuera.

## La búsqueda importa más que los hashtags

El buscador de Instagram lee el texto. La frase por la que Cristal quiere ser encontrado va escrita como la escribiría una persona, en una oración normal: "cloro para pileta en Río Cuarto" en la línea tres, no `#cloroparapileta` en un bloque. **La ciudad va siempre** en contenido para consumidor final o mayorista local: es lo que hace que lo encuentre alguien de Río Cuarto y no de Rosario. Para ruta camión, el nombre del pueblo.

Pedile a Joaco dos o tres términos (o proponelos según el tema) y pasalos al linter con `--keywords`.

## Reglas

- **Nada de links ni teléfonos en el cuerpo.** No se pueden tocar. El camino es el botón de WhatsApp del perfil o el link de la bio. Si Joaco quiere el número igual (hay clientes grandes que lo copian), que vaya al final, y el linter lo va a marcar: decidilo en voz alta.
- **Precio a la vista.** "Precio por privado" está prohibido: en Argentina espanta. Si el precio varía (por cantidad, por segmento), se dice en una línea y se manda a WhatsApp.
- **Un solo pedido.** Dos pedidos es igual a ninguno. El linter los cuenta.
- **La palabra clave se puede tipear:** una palabra, sin espacios ni emojis, y se dice también en el video. "Comentá PILETA" sirve; "comentá 'quiero la tabla'" no.
- **Emoji como puntuación, no como adorno.** Uno, a veces ninguno.
- **Texto alternativo** en carruseles y fotos: una frase que describa la imagen. Lo leen los lectores de pantalla y el buscador.
- **Facebook:** el mismo caption sirve; ahí los links sí se pueden tocar, así que se puede agregar el wa.me al final en la versión de Facebook.

## El proceso

1. Decidí trabajo A, B o promo, y decilo.
2. Escribilo.
3. Pasalo por `cristal-humano`. Los captions son cortos y una muletilla pesa más acá que en cualquier otro lado.
4. Corré `caption.py` con `--local` (siempre), `--keywords` y `--oferta` si es promo. Arreglá cada FALLA. Cada OJO se decide en voz alta, no en silencio.
5. Entregá el bloque listo para copiar y después el resumen:

```
CAPTION LISTO
trabajo:     A, el reel trae el hook
visible:     112 de 125 caracteres antes del corte
pedido:      uno, WhatsApp con "Hola! Vi el video de la pileta verde"
precio:      {{precio}} en la línea 1 (Odoo, L.C 1, hoy)      ← si aplica
hashtags:    3
búsqueda:    "Río Cuarto" en la línea 1, "cloro para pileta" en la línea 3
revisión:    LISTO
```

Si la publicación está en el tablero, actualizá su `cta` y `mensaje_whatsapp` con lo que quedó (leé el documento y escribí con `if_version`). Nada se publica: Joaco lo pega.
