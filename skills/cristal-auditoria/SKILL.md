---
name: cristal-auditoria
description: Post mortem de lo que publicó Química Cristal - qué funcionó por múltiplo, retención y conversaciones de WhatsApp (no por vistas), qué dejar de hacer, qué orgánico pasa a anuncio en Meta; carga al tablero las métricas de capturas de Insights. Usala para "cómo nos fue con lo que publicamos", "auditá nuestras redes", "leé nuestras estadísticas", "por qué no anduvo nuestro reel", "te paso las métricas", o capturas de Insights de Cristal.
---

# cristal-auditoria

La única fuente honesta de qué funciona para Cristal es Cristal. Toda regla de cualquier guía, incluidas las de este paquete, es una suposición. Los últimos 30 posteos propios son la evidencia, y la venta en Odoo es la verdad.

Una herramienta vive en esta carpeta:

```bash
python3 <carpeta>/auditoria.py carpeta_publicaciones/ --desde 2026-09-01
```

## Dos trabajos distintos

**A. Cargar métricas** (cada semana, a los 7 días de cada posteo). Joaco manda capturas de Insights de un posteo o pega los números. Vos:

1. Leés las capturas y extraés: vistas (reproducciones), cuentas alcanzadas, % de no seguidores, % que pasó los 3 s (si está el gráfico de retención, leelo), tiempo promedio de reproducción, guardados, compartidos, comentarios, seguidores ganados. Guardalos como números sin separadores (6100, no "6.100").
2. Preguntás lo que Instagram no da: **cuántas conversaciones de WhatsApp llegaron con el mensaje precargado de ese posteo** (lo sabe Joaco o lo cuenta Claudio) y si hubo **pedidos**. Para ventas podés buscar en Odoo pedidos de los días siguientes que mencionen el origen. Sin marca de origen la venta es estimada: va en `ventas_estimadas`, nunca en `ventas`, y no cuenta para mandar algo a pauta.
3. Encontrás la publicación en el tablero (por fecha y hook) y escribís `metricas` con `update` + `if_version`, más `estado: "publicado"` y la `url` si la pasó. Si el posteo no estaba anotado, lo creás con lo que se sepa (con su OK).
4. Una línea de lectura: "6,1x la mediana, 62 % pasó los 3 s, 4 conversaciones. El hook funcionó; anotado." Sin informe largo.

Si en el chat hay navegador conectado a su Chrome y Joaco está presente, podés **leer** el panel de estadísticas de la cuenta profesional en su sesión, sin iniciar sesión por él. Leer, no tocar nada.

**B. Auditar** (una vez por mes, o cuando lo pida). Es lo de abajo.

## Qué medir de verdad

Las vistas solas son el número menos útil de la pantalla: dependen sobre todo de cuántos ya te siguen. Esto se calcula, y se muestra la cuenta:

| métrica | cómo | qué dice |
|---|---|---|
| **Múltiplo** | vistas / mediana de vistas de la cuenta | si fue un hit o un día normal |
| **No seguidores** | % del alcance que no seguía la cuenta | si viajó |
| **Retención 3 s** | % que pasó los 3 segundos | la nota del hook |
| **Tiempo promedio** | segundos vistos en promedio, contra el largo del reel | si el medio funcionó |
| **Envíos / alcance** | compartidos cada 1.000 alcanzados | la señal más fuerte: alguien puso su nombre |
| **Seguidores / alcance** | seguidores ganados cada 1.000 | si el perfil convirtió la atención |
| **Conversaciones** | WhatsApp con el mensaje precargado | si el posteo hace vender. **La que más importa** |
| **Ventas** | pedidos atribuibles en Odoo | la verdad |

Se ordena por múltiplo y por conversaciones, no por vistas. Un reel de 900 vistas con 6 conversaciones le ganó a uno de 9.000 con ninguna.

## El proceso

1. Bajá las publicaciones del tablero a archivos: ArtifactData `list` de `publicaciones` con `out_dir` apuntando a tu carpeta de trabajo (y `query.limit` alto).
2. Corré `auditoria.py` sobre esa carpeta, con `--desde` / `--hasta` si el período importa.
3. Mirá el tercio de arriba contra el de abajo y buscá qué los separa, dispuesto a concluir algo que a Joaco no le guste:
   - **Retención a los 3 s.** Si arriba y abajo difieren acá, es el hook y nada más, y todo lo demás distrae.
   - **Fórmula de hook.** ¿Qué números de `hooks.json` están arriba?
   - **Formato y pilar.** Reel, carrusel; demostración, la cuenta, mito, oferta, detrás de escena.
   - **Segmento.** ¿Qué segmento escribe por WhatsApp y cuál solo mira?
   - **Largo.** Menos de 15 s, 15-30, 30-60, más de 60.
   - **Si se respondieron comentarios en la primera hora.**
   - **Día y hora.** Última, y solo si lo demás no muestra nada. Casi nunca es la causa y es donde todos quieren que esté.
4. Cada conclusión, como afirmación con su evidencia y su nivel de confianza. Con 30 posteos se ve un patrón. Con 6 no, y decirlo vale más que inventar uno.

## La distinción que ahorra meses

**Un reel con vistas y sin seguidores ni mensajes no es un reel fallido, es un problema de perfil o de pedido.** Un reel sin vistas es un problema de hook. Separá las dos cosas antes de recomendar. Si los no seguidores son altos y los seguidores y conversaciones bajos, dejá de reescribir hooks: el problema está en `cristal-perfil` o en el pedido de acción (¿el mensaje de WhatsApp era claro? ¿el número atendía?).

## Del orgánico a la pauta

Este es el puente que hace que el orgánico pague. El script marca **candidatos a anuncio**: múltiplo de 3x o más y al menos una conversación. Para cada uno:

1. Decí por qué es candidato (múltiplo, retención, conversaciones).
2. Proponé la versión anuncio: el mismo hook y estructura, con precio en pantalla si es oferta, y el mensaje precargado único para Claudio.
3. Pasalo a `meta-ads-cristal` (cargala con la herramienta Skill), que decide presupuesto, estructura y economía unitaria. Esta skill no toca la pauta.

## Entrega

```
AUDITORÍA  ·  31 posteos  ·  12 sep - 12 oct  ·  mediana 1.400 vistas

ARRIBA (por múltiplo)
  6,1x  #28 El mito          62 % pasó 3 s   48 % no seg.   4 conversaciones
  4,3x  #13 Antes y después  58 %            51 %           6 conversaciones
  ...
ABAJO
  0,4x  #30 Precio en pantalla (sin Joaco)   31 %   9 %     0
  ...

LO QUE DICEN LOS DATOS
1. La retención a los 3 s es toda la historia: arriba 60 %, abajo 33 %. n=31.
2. Los videos con la mano trabajando en el primer cuadro: 4,0x contra 0,9x. n=7. La señal más fuerte.
3. Las placas de promo con foto de producto juntan vistas y ninguna conversación.
4. El día de la semana no muestra nada. Dejá de mirarlo.

DEJAR: placas de promo con foto de stock.
HACER MÁS: antes y después, con la mano en el cuadro 1.
A PAUTA: el reel del mito de la pileta (6,1x, 4 conversaciones) -> meta-ads-cristal.
```

(Los números de arriba muestran el formato, no son de Cristal: los reales salen del script.)

Después pasale las conclusiones a `cristal-plan` para que la semana siguiente se arme con evidencia propia, y a `cristal-referentes` para filtrar las fórmulas que a Cristal le funcionan. Si la auditoría deja una regla nueva (ej. "no más placas de stock"), anotala en `notas` del plan de la semana siguiente.
