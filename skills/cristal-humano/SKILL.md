---
name: cristal-humano
description: Le saca la huella de IA a cualquier texto de Química Cristal y lo deja en rioplatense - rayas, muletillas de IA y de folleto, caracteres invisibles, tuteo a voseo, regionalismos ajenos (piscina, lejía, coger) - y lo puntúa con un panel de cinco chequeos. Usala antes de mostrar cualquier guion, caption, historia, comentario, respuesta o mensaje de Cristal, y cuando pidan "humanizá esto", "suena a IA", "pasalo a voseo", "sacale lo de ChatGPT".
---

# cristal-humano

Dos herramientas viven en esta carpeta y funcionan. Usalas: esto no se hace a ojo.

```bash
python3 <carpeta>/humanize.py borrador.txt -o limpio.txt --report   # limpia y muestra qué cambió
python3 <carpeta>/detect.py borrador.txt limpio.txt                 # puntúa antes y después
python3 <carpeta>/detect.py limpio.txt                              # puntúa uno solo
```

`<carpeta>` es la "Base directory" de esta skill. Los archivos de trabajo van en tu carpeta de trabajo.

Las dos leen `slop.json`: palabras y frases de IA y de folleto con su reemplazo llano, regionalismos que no son de Río Cuarto, formas de tuteo con su voseo, caracteres invisibles, tipografía y 22 marcas de estructura. Se puede editar: si Joaco usa a propósito una palabra que el léxico cambia, se saca de ahí en la próxima versión del paquete.

## Por qué importa más en Instagram que en un texto largo

Los captions son cortos y los guiones se dicen en voz alta. Una frase escrita "de agencia" pesa más en 300 caracteres que en una página, y un guion que nadie diría así se nota en la primera toma. La señal no es un detector marcando el posteo: es una persona de Río Cuarto pasando de largo algo que suena a folleto o a traducción.

## Qué se arregla solo

1. **Caracteres invisibles**: espacios de ancho cero, unidores, guiones blandos, BOM, espacios duros. Un teclado de celular no los produce y sobreviven al copiar y pegar.
2. **Tipografía**: raya (—) a coma, comillas curvas y angulares a rectas, puntos suspensivos de un carácter a tres puntos, viñeta a guion. Los signos de apertura ¿ ¡ no se tocan: son castellano.
3. **Léxico**: "en el mundo actual", "soluciones integrales", "calidad premium", "brindamos", "al siguiente nivel", "no te lo pierdas", "tu hogar"...
4. **Regionalismos**: piscina → pileta, lejía → lavandina, trapeador → trapo de piso, coger → agarrar, aquí → acá, móvil → celular.
5. **Tuteo a voseo**: puedes → podés, tienes → tenés, escríbenos → escribinos, para ti → para vos, y los imperativos al principio de oración ("Descubre nuestra línea" → "Conocé nuestra línea").

## Qué NO se arregla solo

Las marcas de estructura se **reportan**, no se reescriben, porque cambiar la forma de una oración necesita criterio:

- "No es solo X, es Y" / "no solo X sino también Y" / "no se trata de X, se trata de Y"
- Tríadas ("rápido, fácil y económico.")
- Preguntas de una línea para armar suspenso ("¿El resultado?")
- Preámbulos ("en este video les voy a mostrar") y "pará de scrollear"
- Viñetas con emoji, emojis cohete/fuego/brillitos, tres palabras en mayúscula seguidas, exclamación en cada frase
- Más de cinco hashtags, "precio por privado", garantías vacías
- Tuteo ambiguo que el script no se anima a cambiar ("Lleva tu..."), pretérito en tuteo ("has visto"), vosotros

Esa lista es tu trabajo. Reescribí cada línea marcada a mano, manteniendo lo que quiere decir, y volvé a correr `detect.py`. Es lo que lleva el puntaje de REVISAR a PASA, y el detector **no deja pasar** un texto con dos o más marcas de estructura aunque el resto dé bien.

## Los cinco chequeos

`detect.py` da un puntaje humano de 0 a 100 por chequeo:

| chequeo | qué mide | cómo se ve la máquina |
|---|---|---|
| RITMO | variación del largo de las oraciones | todas las oraciones del mismo largo |
| CONCRETO | números, nombres, productos cada 100 palabras | sustantivos abstractos, sin cifras |
| RELLENO | términos del léxico cada 100 palabras | vocabulario de folleto |
| HUELLA | invisibles, rayas, comillas curvas | tipografía perfecta |
| VOZ | voseo y habla de acá, personas, marcas de estructura, tuteo | sin voseo, sin nadie que hable, revelaciones armadas |

El veredicto pesa el promedio al 60 % y el **peor chequeo** al 40 %, porque alcanza con una señal. PASA pide 70 o más, ningún chequeo abajo de 55 y menos de dos marcas de estructura.

## Decilo con honestidad

Son cinco heurísticas locales inspiradas en lo que miran los detectores públicos. No son GPTZero, Originality ni nada parecido, no los llaman y no prometen su veredicto. Arreglar lo que miden suele mover esos números porque miden lo mismo de fondo; esa es toda la promesa. Nunca le digas a Joaco que un texto es "indetectable".

Para textos de menos de 25 palabras (un comentario, una placa) los chequeos de concreto y voz dan "muy corto para juzgar": ahí vale el reporte de `humanize.py` y tu lectura.

## Orden de trabajo

1. `humanize.py borrador.txt -o limpio.txt --report`
2. Leé las marcas de estructura. Reescribí esas líneas vos.
3. Revisá que los reemplazos automáticos tengan sentido en contexto (un reemplazo que deja una frase rara se corrige a mano).
4. `detect.py borrador.txt limpio.txt` para mostrar el antes y el después.
5. Si no PASA, arreglá el chequeo más flojo que nombra la salida y otra vuelta. Dos vueltas es normal. Cinco quiere decir que el borrador se escribió con fórmula: lo que hace falta es otro borrador, no más pasadas.
6. Mostrá el texto limpio y el puntaje. Nunca el puntaje solo.
