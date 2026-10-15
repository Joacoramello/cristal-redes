---
name: cristal-perfil
description: Puntúa sobre 100 el perfil de Instagram de Química Cristal con una rúbrica de 12 ítems para comercio local (nombre, bio, botón de WhatsApp, fijados, destacadas, grilla, actividad) y reescribe lo que pierde puntos, en orden. Usala para "revisá el perfil de Cristal", "arreglá la bio", "puntuá el Instagram", "por qué no nos escriben desde Instagram".
---

# cristal-perfil

Casi todos optimizan lo que no es. El perfil no es una vidriera que se recorre: es una **pantalla de decisión** a la que se llega desde un reel o un anuncio, y tiene unos tres segundos para contestar: ¿esto es para mí, dónde está, cómo compro y está abierto?

## Antes de empezar

Cargá `cristal-marca` (datos de `config/marca`: @, dirección, número de WhatsApp que atiende).

## Qué hace falta

Pedile a Joaco una captura de la parte de arriba del perfil más las dos primeras filas de la grilla, y que te diga: a dónde va el link, qué abre el botón de WhatsApp, qué destacadas hay y qué está fijado. Si en este chat hay navegador conectado a su Chrome y él lo prefiere, podés **mirar** el perfil público con él presente; nunca iniciar sesión por él ni pedirle la contraseña.

Leé las mediciones anteriores en la colección `perfil` del tablero.

## Puntuar

Leé `rubrica.json` de esta carpeta: doce ítems, 100 puntos, cada uno con cómo se ve el puntaje completo y cómo suele fallar. Puntuá todos, mostrá la tabla y el total. Sé honesto: los perfiles de comercio suelen arrancar entre 30 y 50, y un puntaje generoso no sirve para nada.

```
PERFIL  41/100

  campo nombre         4/12   "Química Cristal", sin rubro ni ciudad
  bio línea 1          5/12   slogan, no dice qué vende ni dónde
  botones y categoría  6/10   WhatsApp abre el número viejo
  fijados              0/10   nada fijado
  destacadas           3/8    "Varios", "Navidad", promo con precio viejo
  ...
```

## Después, reescribir en este orden

Por puntos perdidos, de más a menos. No todo junto: Joaco tiene que ir y cambiar cada cosa.

**1. Campo nombre (30 caracteres).** La línea en negrita, no el @. Es lo que matchea el buscador de Instagram. Formato: `Química Cristal | {rubro} {ciudad}`. Tres opciones, contadas en caracteres.

**2. Bio, primera línea.** Qué vende, a quién y dónde. No un slogan. El resto de los 150 caracteres: una prueba (20 años, fabricación propia) y una condición que hace comprar (envío gratis en Río Cuarto desde el monto vigente, confirmado). Tres opciones.

**3. Los tres fijados.** Tres lugares, tres trabajos: la promo vigente con precio, cómo comprar (un carrusel de `cristal-carrusel`), y quiénes somos (Joaco en el local o la fábrica). Si alguno no existe, se dice y se agrega al plan. Es el arreglo de más impacto del perfil y son cuatro toques.

**4. Botones.** WhatsApp al número que atiende (Claudio), dirección cargada, categoría correcta, teléfono. Pedile que pruebe cada botón desde otro celular.

**5. Destacadas.** De cuatro a seis, con nombre de pregunta de comprador: Promos, Envíos, Piletas, Mayoristas, Camión, Cómo llegar. Borrar el resto. Precios viejos adentro de una destacada: fuera.

**6. El link.** Una puerta que coincida con la bio: el wa.me del número que atiende con mensaje precargado (ej. "Hola! Te escribo desde Instagram"), o la tienda. Un árbol de links con ocho opciones convierte peor que una puerta.

**7. Portadas de la grilla.** Las primeras nueve en miniatura. Portadas de reels elegidas, con cuatro palabras de texto.

## Entrega

Tabla de puntaje, después las reescrituras como bloques listos para copiar en el orden de arriba, cada una pasada por `cristal-humano` (y con el conteo de caracteres al lado del nombre y la bio). Al final, el puntaje estimado si aplica todo, contado honesto: si llega a 78 y no a 95, decí 78 y qué falta, que suele ser publicar seguido, historias casi todos los días y un fijado que todavía no existe. Nada de eso es una reescritura.

Guardá la medición en la colección `perfil` del tablero (`doc_id` la fecha, `puntaje`, `items` con los puntos de cada uno, `notas`) después de mostrarla. Nada se cambia en Instagram desde acá: Joaco edita cada campo.
