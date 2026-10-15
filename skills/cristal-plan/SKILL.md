---
name: cristal-plan
description: Arma la semana de redes de Química Cristal - qué se publica cada día, en qué formato, para qué segmento, con qué hook, las historias, la ronda de interacción con cuentas locales y la temporada (pileta, camión, gastronomía), y la guarda en el tablero. Usala para "armá la semana de Cristal", "qué publicamos esta semana", "calendario de contenido", "no tengo de qué publicar en el feed".
---

# cristal-plan

La sala de control. Todo lo demás del paquete ejecuta; esto decide qué se ejecuta. Una vez por semana, siempre el mismo día.

## Qué leer

1. Cargá `cristal-marca` (voz, segmentos, temporadas, `config/marca`).
2. Del tablero: `publicaciones` de las últimas 4 semanas (qué se hizo, qué funcionó por múltiplo y por conversaciones de WhatsApp, qué temas no repetir), `referentes` (qué fórmulas están funcionando en el rubro, mandan sobre cualquier regla de acá) y el plan de la semana anterior (qué quedó sin hacer).
3. Si hay una auditoría reciente (`cristal-auditoria`), sus conclusiones mandan.
4. Odoo: qué combos o promos hay activos (categoría "Combos y Kit"), con stock. No se planifica una promo sin stock.

## Qué preguntarle a Joaco (en una sola tanda, solo lo que no sepas)

1. ¿Qué pasó esta semana? Un cliente, una pregunta repetida en el mostrador, un pedido grande, un problema, algo que se fabricó, el camión. De acá salen los posteos.
2. ¿Hay promo, lanzamiento o salida del camión esta semana o la que viene?
3. ¿Cuánto puede grabar? (Ej. "una hora el martes en el local".) El plan tiene que caber en eso.

## Qué se publica

Arrancá con lo que se puede sostener: **tres posteos por semana bien hechos le ganan a cinco a medias**. Si las últimas semanas no se cumplió el plan, bajá la cantidad y decilo.

Al menos dos de los tres, reels: es el único formato que llega seguido a gente que no te sigue. El carrusel va hondo con los que ya te siguen. Las historias son diarias y se planean aparte.

Con tres posteos: **dos fijos y uno que rota.** Nunca dos del mismo tipo seguidos. Estos tipos son los mismos valores de `pilar` del tablero:

| tipo (pilar) | lugar | trabajo | formato |
|---|---|---|---|
| **demostración** | fijo, todas las semanas | el producto haciendo algo visible: antes y después, demo en frío | reel |
| **enseñar** | fijo, todas las semanas | algo que el que mira puede hacer hoy: la tabla, la dilución, el mito | reel o carrusel |
| **oferta** | rota (en temporada de pileta, fijo y pasa a 4 posteos) | la promo con precio, dicha sin vueltas. Formato "precio en pantalla" | reel o historias |
| **detrás de escena** | rota | la fábrica, el camión, el depósito: lo que un súper no puede mostrar | reel |
| **mayorista** | rota (fijo la semana que sale el camión a un pueblo nuevo) | "si tenés almacén...", rendimiento para revender, preventa | reel |
| **prueba** | cuando haya algo real | un cliente con permiso, un número de Odoo | reel o carrusel |

El lugar que rota va pasando por oferta, detrás de escena y mayorista; mirá en el tablero cuál tocó la semana pasada.

Para cada lugar: el tema, **el ángulo concreto que salió de lo que pasó esta semana**, el formato, el segmento y el número de fórmula de `hooks.json` de cristal-reel (carpeta hermana: `<carpeta>/../cristal-reel/hooks.json`; si no está, cargá `cristal-reel` con la herramienta Skill y usá su "Base directory"). No un tema: un ángulo. "Pileta" no es un plan. "La señora que trajo una muestra de agua verde y era el pH" es un reel.

## Cuándo publicar

Consumidor final: a la tardecita (19 a 21 h). Mayorista, gastronómicos e institucional: temprano (7 a 9 h) o al mediodía.

Pero decilo claro: **la hora importa mucho menos que los dos primeros segundos.** Instagram sigue mostrando un reel durante días si funciona, y entierra uno bien puesto que no. Si Joaco está optimizando horarios antes de que los hooks funcionen, está puliendo lo que no es: decíselo.

## Historias

Todos los días, de 3 a 5 placas (máximo 7; ver `cristal-historias`). En el plan: qué historia tiene sticker y qué día, y las de preventa si sale el camión.

## La ronda de interacción (no es opcional)

20 minutos por día, antes de publicar. Una lista de 10 cuentas, que maneja `cristal-alcance`:

- **5 de alcance local**: cuentas de Río Cuarto con la audiencia que Cristal quiere (medios locales, gastronómicos conocidos, clubes, inmobiliarias, consorcios). Un comentario bueno ahí lo ve más gente que muchos posteos propios.
- **3 pares**: comercios de la ciudad de tamaño parecido, no competidores directos (ferreterías, viveros, bazares). Son los que devuelven.
- **2 compradores**: un bar, un colegio, un almacén de la zona que podría comprar. Se comenta durante semanas antes de cualquier mensaje, y nunca se vende en un comentario.

Si Joaco no tiene la lista, proponé categorías y pedile los @; no inventes cuentas.

## Entrega

```
SEMANA DEL 20 DE OCTUBRE  ·  3 posteos + historias diarias  ·  grabación: martes 1 h en el local

LUN  solo historias + ronda (20 min)
MAR  19:30  REEL      demostración  CF          #13 Antes y después  - la campana del bar de la esquina (con permiso)
JUE  08:00  REEL      mayorista     ruta camión #14 Llamado al grupo - almacenes de {{pueblo de la ruta}}, cierre preventa martes
SÁB  19:00  CARRUSEL  enseñar       CF          tabla               - cloro por litros de pileta, con nuestro granulado

HISTORIAS  todos los días, 3-5 placas. Caja de preguntas el jueves ("¿qué le pasa a tu pileta?").
           Preventa del camión: lunes y martes.
RONDA      5 locales / 3 pares / 2 compradores (lista abajo)

Decime "escribí el martes" y lo armo.
```

Guardalo en la colección `planes` del tablero (`doc_id` = semana ISO, ej. `2026-W43`) después de que Joaco lo apruebe, y anotá cada posteo en `publicaciones` con `estado: "planificado"`. Si tiene Google Calendar conectado y lo pide, cargá el bloque de grabación y cada publicación como eventos en su calendario (con su OK antes de crearlos). Nada se programa ni se publica en Instagram desde acá: es un plan y lo ejecuta Joaco.
