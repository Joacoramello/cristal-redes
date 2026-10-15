---
name: cristal-marca
description: Base de las redes de Química Cristal (Cristal, Crilim) - voz, segmentos, precios desde Odoo, reglas y tablero. Toda skill cristal-* la carga primero. Usala también para "qué publico hoy", "por dónde arranco con las redes de Cristal", "completá/actualizá los datos o la voz de la marca", "cómo funcionan las skills de redes".
---

# cristal-marca

El centro del paquete de redes de Química Cristal. No escribe contenido: le da a las otras skills la voz, el negocio y la memoria, y orienta a Joaco cuando no sabe por dónde empezar.

## Qué cargar siempre (todas las skills cristal-* hacen esto primero)

1. Leé `referencias/marca.md` (voz, quién es la cara, qué no se dice) y `referencias/negocio.md` (segmentos, precios desde Odoo, temporadas, seguridad). Están en la carpeta de esta skill: la que figura como "Base directory" cuando la cargás.
2. Leé `config/marca` del tablero (ver `referencias/tablero.md`). Lo que diga ahí le gana a `marca.md`. Si no existe o faltan campos, seguí y pedí solo lo que el trabajo de hoy necesita.
3. Si el trabajo es de una publicación concreta, leé las últimas `publicaciones` del tablero para no repetir tema ni fórmula de las últimas dos semanas.

## El paquete

| Skill | Para qué |
|---|---|
| `cristal-plan` | La semana: qué se publica, en qué formato, para qué segmento, con qué hook, y la ronda de interacción |
| `cristal-reel` | Una idea a reel: tres hooks puntuados, guion, texto en pantalla, hoja de tiempos |
| `cristal-carrusel` | Carruseles: portada, placas, y las imágenes 1080x1350 listas para subir |
| `cristal-historias` | Las historias del día y el embudo a WhatsApp |
| `cristal-caption` | El caption: lo que se ve antes del "más", un pedido, precio visible, revisión automática |
| `cristal-humano` | Le saca la huella de IA a cualquier texto y lo pasa a voseo rioplatense |
| `cristal-respuestas` | Comentarios y mensajes en la cuenta propia: priorizar, responder, derivar a WhatsApp |
| `cristal-alcance` | Comentar en cuentas locales, propuestas de colaboración, seguimientos |
| `cristal-reciclar` | Un video largo, una visita, un anuncio o una charla de mostrador convertidos en una semana de posteos |
| `cristal-referentes` | Investigar qué funciona en cuentas del rubro, rankeado por cuánto le ganó cada reel a su cuenta |
| `cristal-auditoria` | Qué funcionó de lo publicado, qué se deja de hacer, y qué orgánico pasa a pauta |
| `cristal-perfil` | Puntaje del perfil sobre 100 y la reescritura de lo que pierde puntos |

El ciclo: **perfil** una vez al arrancar y cada tres meses → **referentes** una vez por mes → **plan** cada semana (mismo día) → **reel / carrusel / historias** → **caption** → **humano** antes de mostrar cualquier texto → Joaco publica → **respuestas** en la primera hora → métricas a los 7 días → **auditoría** una vez por mes, que alimenta el plan y la pauta.

## "¿Qué publico hoy?" o "¿por dónde arranco?"

Leé el tablero y respondé según lo que haya, en este orden:

1. Sin puntaje de perfil → arrancá por `cristal-perfil`. Un reel que trae gente a un perfil que no convierte se desperdicia.
2. Faltan datos clave en `config/marca` (el @, el número de WhatsApp que atiende, la dirección) → completalos antes de escribir nada que los use (ver abajo).
3. Hay plan de esta semana → decí qué toca hoy y ofrecé escribirlo con la skill que corresponde.
4. No hay plan → `cristal-plan`.
5. Hay posteos de hace 7 días o más sin métricas → pedí las capturas de Insights para cargarlas.

Respuesta corta: qué toca, por qué, y la oferta de escribirlo. No un menú de opciones.

## Completar o actualizar los datos de la marca

Cuando Joaco pida "completá los datos de Cristal", "actualizá la voz", o falte algo que el trabajo necesita:

1. Leé `config/marca` (si existe, guardá su `version`).
2. Preguntá **solo lo que falta**, de a una o dos cosas por vez, con AskUserQuestion si está disponible. Prioridad: @ de Instagram, número de WhatsApp de Claudio, dirección y horario, palabra clave y qué manda, link de la bio, logo y colores.
3. **Voz**: pedile tres videos o transcripciones de él hablando a cámara (los anuncios que funcionaron sirven). Leelos y anotá en `voz_notas`, en sus palabras: cómo arranca las frases, muletillas reales, palabras que usa, cómo pide la acción, ritmo. Guardá las transcripciones en `voz_muestras`. No describas la voz con adjetivos ("cercano, dinámico"): escribí ejemplos de lo que dice.
4. Mostrale el documento completo y escribilo en `config/marca` con ArtifactData solo después de su sí (`set` con `if_version` si ya existía).
5. Si el cambio es estructural (una regla nueva, un segmento nuevo), además de guardarlo en el tablero decile que conviene actualizar `marca.md` o `negocio.md` en la próxima versión del paquete.

## Reglas que valen para todo el paquete

- **Nada se publica solo.** Las skills escriben; Joaco publica, comenta y manda los mensajes. No se usa navegador para postear, comentar, seguir ni mandar mensajes, y no se automatiza interacción en Instagram: viola sus términos y restringe la cuenta (ya hay dos números de WhatsApp restringidos por mensajes masivos; no repetir la historia en Instagram).
- **No se inventa nada.** Ni precios, ni clientes, ni resultados, ni testimonios, ni diluciones. Si falta un dato, `{{dato}}` y un aviso.
- **Precios desde Odoo, el día.** Procedimiento en `negocio.md`.
- **Seguridad química primero.** Ninguna mezcla, ninguna promesa sanitaria fuera de la etiqueta.
- **Todo texto pasa por `cristal-humano`** antes de mostrarse: guion, caption, historia, comentario, respuesta, mensaje.
- **Anotar en el tablero** lo que Joaco aprueba, para que el próximo chat sepa qué se hizo.
- Joaco quiere un asesor franco: si un pedido no va a vender, si la idea es floja o si está puliendo lo que no importa (horario de posteo antes que el hook), decíselo con el motivo y la alternativa.
