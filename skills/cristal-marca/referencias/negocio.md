# El negocio detrás de las redes

Lo que las skills de redes necesitan saber para que un posteo venda y no solo junte vistas. Los datos que cambian (precios, stock, montos de envío) **no se copian de acá**: se consultan en Odoo o se le preguntan a Joaco el día que se escribe. Lo que está con fecha es la última versión conocida; si pasaron más de 30 días, se confirma antes de publicarlo.

## Para qué sirven las redes (orden de prioridad)

1. **Vender por WhatsApp** a consumidor final de Río Cuarto y alrededores, y a mayoristas.
2. **Encontrar el próximo anuncio.** Hasta oct-2026 Cristal no publicaba orgánico, solo pauta en Meta (unos $200-300 mil por mes). Un reel orgánico que le gana 3 veces o más a la mediana de la cuenta es un candidato a anuncio: se graba igual, con precio, y pasa a la skill `meta-ads-cristal`. El orgánico es el laboratorio barato de la pauta.
3. **Respaldar la venta en persona.** Alejandra visita gastronómicos, institucionales, consorcios y fábricas; el que la recibe busca la cuenta. El perfil tiene que confirmar que esto es serio y que existe hace 20 años.
4. **Preventa del camión** en los pueblos de la zona.

Seguidores y "me gusta" no son objetivo. Las métricas que importan están en `cristal-auditoria`.

## Segmentos

Nunca se mezclan dos segmentos en un mismo posteo: cada uno tiene su precio, su pedido mínimo y su mensaje de entrada.

| Segmento | Quién | Qué le duele | Qué contenido le sirve | Cierre |
|---|---|---|---|---|
| **Consumidor final (CF)** | Hogares de Río Cuarto, Las Higueras, Holmberg | Pileta verde, gastar de más en el súper, limpiar rápido, olor | Antes/después, la cuenta (precio por litro), mitos, tablas para guardar, promo con precio | WhatsApp (Claudio) o el local. Envío gratis desde el monto vigente |
| **Mayorista Río Cuarto** | Químicas, casas de limpieza, revendedores, emprendedores de limpieza | Margen, rotación, proveedor que cumpla | Detrás de escena de la fábrica, rendimiento, "cuánto ganás revendiendo X", llamado al grupo | WhatsApp mayorista (Claudio), lista Mayorista |
| **Ruta camión (zona ~100 km)** | Almacenes, revendedores e institucionales de los pueblos | Que el proveedor llegue, flete | Fecha de salida y cierre de preventa, promo "a reventar" de un producto de alta rotación, nombre del pueblo | Preventa (Joaco). El camión sale los **miércoles** (cambiado el 02/10/2026, confirmar). Pago anticipado o contra entrega |
| **Gastronómicos / institucional / consorcios** | Bares, restaurantes, hoteles, colegios, clubes, cooperativas, edificios | Grasa, inspecciones, consumo, que no falte | Demo en frío (campana, plancha, parrilla), "3 que todo bar necesita", dilución y costo por servicio | Visita de Alejandra + WhatsApp. La pauta para este segmento rinde mal ($2.762 por conversación en gastronómicos); el orgánico apoya la visita, no la reemplaza |

## Condiciones comerciales (confirmar antes de publicarlas)

- Envío a domicilio gratis en Río Cuarto desde **$49.000** (desde oct-2026), entrega en 24 h hábiles. **"Te lo llevamos gratis" se dice solo si el precio de Odoo del producto o combo llega al monto**; si no llega, se dice la condición ("envío gratis sumando $X más") o el costo del envío. Nunca "sale hoy" ni "llega hoy": la promesa es 24 h hábiles.
- Mayorista (datos de sep-2026): pedido mínimo $75.000, flete $9.000, envío gratis desde $99.000.
- Ruta camión: sin 20 % de descuento de primera compra; la herramienta es una promo de un producto de alta rotación por cantidad.
- Institucional: promo mensual por "rubro de entrada" (lo que el cliente todavía no compra), con unidades gratis o equipo sin cargo, no un descuento chico. Esa promo va por WhatsApp a cada cliente, no a redes.
- Precios: los decide Sergio. Descuentos de la promo mensual institucional: los autoriza Joaco. **Ninguna skill de redes inventa un descuento.**

## Precios y stock: siempre desde Odoo

Conector `odoo_producc`. Antes de escribir un precio en un guion, caption, placa o historia:

1. **Buscar el producto**: `search_records` en `product.product` por nombre o código (`default_code`), con `fields: ["display_name","lst_price","standard_price","qty_available","categ_id"]`. `lst_price` es el precio público de lista (consumidor final, **IVA incluido**). Los combos de temporada están en la categoría "Combos y Kit" (id 53).
2. **Ver si la lista tiene un precio propio**: `search_records` en `product.pricelist.item` con `[["pricelist_id","=",ID],["product_id","=",ID_PRODUCTO]]`. Si hay `fixed_price`, ese manda; si tiene `min_quantity` mayor a 1, es un precio por cantidad y así se comunica ("llevando 4 o más").
   - Listas: **L.C 1** (id 19, consumidor final), **Lista Mayorista** (id 6), **L.E 1** (id 32, empresas/institucional). L.C 2 y L.E 2 existen; no usarlas sin que Joaco lo pida.
   - Si la regla es una fórmula por categoría (recargo sobre costo), no calcular un precio para publicar: preguntarle a Joaco.
3. **Stock**: si `qty_available` no alcanza para dos semanas de venta esperada, no se promociona; se avisa a Joaco.
4. **Dejar escrito de dónde salió**: en la respuesta, "precio de Odoo, lista L.C 1, consultado hoy". Si no se pudo consultar, el borrador lleva `{{precio}}` y un aviso.

Ejemplo de por qué no se copia nada: el combo de cloro 6 kg se pautó a $39.990 en la temporada 2025-26 y en oct-2026 su precio de lista en Odoo es otro.

## Temporadas y fechas que mueven contenido

| Cuándo | Qué pasa | Contenido |
|---|---|---|
| Sep-oct | Preparación de piletas | "Abrila azul", qué hacer antes de llenar, tabla de cloro por litros |
| Nov-mar | Temporada de pileta (pico dic-ene) | Pileta verde, pH, combos de cloro con precio, mitos, recompra |
| Dic | Fiestas, gastronomía a full | Gastronómicos: grasa, campanas, limpieza profunda antes del cierre |
| Feb-mar | Vuelta a clases y a la oficina | Institucional: colegios, consorcios, kit de inicio de año |
| Abr-ago | Frío y humedad | Moho, hongos, ropa, pisos; el mostrador sostiene la caja sin la pileta |
| Hot Sale (may) / CyberMonday (nov) | Fechas de descuento online en Argentina | Solo si Joaco arma una promo real para la web |
| Cada semana | Salida del camión | Historia con el pueblo, la fecha y el cierre de preventa |

## Seguridad y lo que se puede afirmar

- **Nunca** mostrar ni describir mezclas de productos químicos entre sí, ni "recetas caseras" con lavandina, amoníaco, ácidos o vinagre. Se dice "no lo mezcles con nada" y alcanza.
- Diluciones, dosis y modos de uso: **solo** los de la etiqueta o la ficha técnica del producto. Si no está a mano, se pide; no se escribe de memoria.
- Dosis de pileta: con la tabla del producto que vende Cristal. Si el contenido da dosis generales, aclarar "para una pileta de X litros, con el producto Y; mirá la etiqueta del tuyo".
- "Desinfecta", "elimina bacterias", "mata el 99,9 %": solo si figura en el rótulo registrado del producto. Si no, "limpia".
- Guantes en cámara cuando se manipula lavandina, cloro o ácido. Es lo que se enseña también.

## Conexión con las otras skills de Cristal

- `meta-ads-cristal`: cuando un orgánico gana (múltiplo 3x o más y conversaciones en WhatsApp), se le pasa el posteo como candidato a anuncio. Esa skill decide presupuesto y estructura; las de redes no tocan la pauta.
- `asistente-pedidos-cristal`: los pedidos que lleguen por redes se cargan con esa skill, no desde las de redes.
- `reel-creator`: es la skill genérica de reels (marca personal de Joaco u otros temas). Para Química Cristal se usa `cristal-reel`.

## El tablero

Todo lo que se planifica, publica y mide queda en el tablero "Redes Cristal": https://claude.ai/artifact/6CsofcZcAPUMt3Nhu8YPw7. Cómo leerlo y escribirlo: `referencias/tablero.md`.
