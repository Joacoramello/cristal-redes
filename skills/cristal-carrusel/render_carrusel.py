#!/usr/bin/env python3
"""
render_carrusel.py - arma las placas de un carrusel de Química Cristal en
1080x1350 (4:5) a partir de un JSON, sin navegador: solo Pillow.

Entrada (carrusel.json):
{
  "marca": {                      # opcional: si falta, usa la paleta de marca.md
    "oscuro": "#EF7D1A", "claro": "#FFFFFF", "acento": "#EF7D1A", "acento_oscuro": "#FFFFFF",
    "texto_oscuro": "#1D1D1F", "texto_claro": "#FFFFFF", "handle": "@quimicacristal"
  },
  "slides": [
    {"tipo": "portada", "titulo": "LA LAVANDINA SE VENCE", "bajada": "Y nadie te lo dice."},
    {"tipo": "idea", "titulo": "El sol la mata", "cuerpo": "Guardada al sol pierde cloro en semanas."},
    {"tipo": "lista", "titulo": "Guardala así", "items": ["A la sombra", "Bien cerrada", "Lejos de la estufa"]},
    {"tipo": "resumen", "titulo": "Todo junto", "items": ["...", "..."]},
    {"tipo": "cta", "titulo": "¿Te sirvió?", "cuerpo": "Guardalo para la próxima compra."}
  ]
}

Reglas que aplica solo: tipografía mínima de 32 px, texto adentro de un margen
de 120 px (así el recorte de la grilla no come nada), numeración "3/8" en cada
placa, el @ de la cuenta abajo en cada una (las capturas viajan sin vos), y un
solo color de acento. Si un título no entra, achica la letra hasta el mínimo y
avisa en vez de cortar.

Uso
  python3 render_carrusel.py carrusel.json --out placas/
  python3 render_carrusel.py carrusel.json --out placas/ --hoja     # + hoja de contactos
"""

import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
MARGEN = 120
MIN_PX = 32

PALETA = {"oscuro": "#EF7D1A", "claro": "#FFFFFF", "acento": "#EF7D1A", "acento_oscuro": "#FFFFFF",
          "texto_oscuro": "#1D1D1F", "texto_claro": "#FFFFFF", "handle": "@quimicacristal"}

FUENTES = {
    "black": ["/usr/share/fonts/opentype/inter/Inter-Black.otf",
              "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "bold": ["/usr/share/fonts/opentype/inter/Inter-Bold.otf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "regular": ["/usr/share/fonts/opentype/inter/Inter-Medium.otf",
                "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
}
AVISOS = []


def fuente(peso, px):
    for path in FUENTES[peso]:
        if os.path.exists(path):
            return ImageFont.truetype(path, px)
    return ImageFont.load_default()


def envolver(draw, texto, f, ancho):
    lineas = []
    for parrafo in texto.split("\n"):
        actual = ""
        for palabra in parrafo.split():
            prueba = (actual + " " + palabra).strip()
            if draw.textlength(prueba, font=f) <= ancho:
                actual = prueba
            else:
                if actual:
                    lineas.append(actual)
                actual = palabra
        lineas.append(actual)
    return lineas


def ajustar(draw, texto, peso, px_max, ancho, max_lineas, n_slide):
    """Achica la letra hasta que entre en max_lineas. Nunca baja de MIN_PX."""
    px = px_max
    while px >= MIN_PX:
        f = fuente(peso, px)
        lineas = envolver(draw, texto, f, ancho)
        if len(lineas) <= max_lineas and all(draw.textlength(l, font=f) <= ancho for l in lineas):
            return f, lineas, px
        px -= 4
    f = fuente(peso, MIN_PX)
    lineas = envolver(draw, texto, f, ancho)
    AVISOS.append(f"placa {n_slide}: el texto no entra ni a {MIN_PX}px. Partilo en dos placas.")
    return f, lineas, MIN_PX


def bloque(draw, lineas, f, x, y, color, interlinea=1.12):
    alto = f.size * interlinea
    for l in lineas:
        draw.text((x, y), l, font=f, fill=color)
        y += alto
    return y


def centrar_contenido(img, fondo):
    """Baja el bloque de texto para que quede centrado entre la barra y el pie."""
    zona = (0, MARGEN + 40, W, H - MARGEN - 10)
    recorte = img.crop(zona)
    vacio = Image.new("RGB", recorte.size, fondo)
    from PIL import ImageChops
    caja = ImageChops.difference(recorte, vacio).getbbox()
    if not caja:
        return
    alto_util = zona[3] - zona[1]
    contenido = recorte.crop((0, caja[1], W, caja[3]))
    nuevo_y = max(0, int((alto_util - contenido.height) / 2 - 40))
    if nuevo_y <= caja[1]:
        return
    img.paste(vacio, (0, zona[1]))
    img.paste(contenido, (0, zona[1] + nuevo_y))


def placa(slide, i, total, m):
    tipo = slide.get("tipo", "idea")
    oscura = tipo in ("portada", "cta")
    fondo = m["oscuro"] if oscura else m["claro"]
    tinta = m["texto_claro"] if oscura else m["texto_oscuro"]
    img = Image.new("RGB", (W, H), fondo)
    d = ImageDraw.Draw(img)
    ancho = W - 2 * MARGEN

    # en placas de fondo oscuro (o naranja) el acento puede ser otro color
    ac = m.get("acento_oscuro", m["acento"]) if oscura else m["acento"]
    # barra de acento arriba
    d.rectangle([MARGEN, MARGEN, MARGEN + 96, MARGEN + 14], fill=ac)

    if tipo == "portada":
        f, lin, _ = ajustar(d, slide.get("titulo", "").upper(), "black", 132, ancho, 4, i)
        alto = len(lin) * f.size * 1.05
        y = (H - alto) / 2 - 60
        y = bloque(d, lin, f, MARGEN, y, tinta, 1.05)
        if slide.get("bajada"):
            fb, lb, _ = ajustar(d, slide["bajada"], "regular", 48, ancho, 3, i)
            bloque(d, lb, fb, MARGEN, y + 40, ac, 1.2)
    elif tipo in ("lista", "resumen"):
        f, lin, _ = ajustar(d, slide.get("titulo", ""), "black", 84, ancho, 2, i)
        y = bloque(d, lin, f, MARGEN, MARGEN + 70, tinta, 1.08) + 40
        items = slide.get("items", [])
        px = 46 if len(items) <= 5 else 40
        for k, item in enumerate(items, 1):
            fi, li, _ = ajustar(d, item, "regular", px, ancho - 90, 3, i)
            d.ellipse([MARGEN, y + 6, MARGEN + 52, y + 58], fill=m["acento"])
            fn = fuente("bold", 30)
            num = str(k)
            d.text((MARGEN + 26 - d.textlength(num, font=fn) / 2, y + 13), num, font=fn, fill=m["texto_claro"])
            y = bloque(d, li, fi, MARGEN + 90, y, tinta, 1.2) + 26
        if y > H - MARGEN - 60:
            AVISOS.append(f"placa {i}: la lista se pasa del margen de abajo. Sacá ítems o partila.")
    else:  # idea, gancho, cta
        f, lin, _ = ajustar(d, slide.get("titulo", ""), "black", 96, ancho, 3, i)
        y = bloque(d, lin, f, MARGEN, MARGEN + 90, tinta, 1.06) + 50
        if slide.get("cuerpo"):
            if len(slide["cuerpo"].split()) > 25:
                AVISOS.append(f"placa {i}: más de 25 palabras en el cuerpo. Partila en dos.")
            fc, lc, _ = ajustar(d, slide["cuerpo"], "regular", 50, ancho, 7, i)
            bloque(d, lc, fc, MARGEN, y, tinta if not oscura else ac, 1.28)

    if tipo != "portada":
        centrar_contenido(img, fondo)

    # pie: numeración y @
    fp = fuente("bold", 32)
    pie_y = H - MARGEN + 30
    d = ImageDraw.Draw(img)
    d.text((MARGEN, pie_y), m.get("handle", ""), font=fp, fill=ac)
    num = f"{i}/{total}"
    d.text((W - MARGEN - d.textlength(num, font=fp), pie_y), num, font=fp, fill=tinta)
    return img


def hoja_contactos(imgs, ruta):
    cols = min(len(imgs), 5)
    filas = (len(imgs) + cols - 1) // cols
    tw, th = 216, 270
    hoja = Image.new("RGB", (cols * (tw + 12) + 12, filas * (th + 12) + 12), "#DDDDDD")
    for k, im in enumerate(imgs):
        r, c = divmod(k, cols)
        hoja.paste(im.resize((tw, th)), (12 + c * (tw + 12), 12 + r * (th + 12)))
    hoja.save(ruta)


def main():
    ap = argparse.ArgumentParser(description="Arma las placas 1080x1350 de un carrusel.")
    ap.add_argument("spec", help="carrusel.json")
    ap.add_argument("--out", default="placas", help="carpeta de salida")
    ap.add_argument("--hoja", action="store_true", help="armar también una hoja de contactos")
    args = ap.parse_args()

    spec = json.load(open(args.spec, encoding="utf-8"))
    m = dict(PALETA)
    m.update(spec.get("marca") or {})
    slides = spec["slides"]
    if not m.get("handle") or "COMPLETAR" in m.get("handle", "").upper() or "[" in m.get("handle", ""):
        AVISOS.append("falta el @ real de la cuenta en 'marca.handle': las placas salen sin firma.")
        m["handle"] = ""
    if not 6 <= len(slides) <= 10:
        AVISOS.append(f"{len(slides)} placas. Lo que funciona es entre 6 y 10.")
    os.makedirs(args.out, exist_ok=True)
    imgs = []
    for i, s in enumerate(slides, 1):
        im = placa(s, i, len(slides), m)
        ruta = os.path.join(args.out, f"{i:02d}.png")
        im.save(ruta)
        imgs.append(im)
        print(f"  {ruta}")
    if args.hoja:
        ruta = os.path.join(args.out, "hoja_contactos.png")
        hoja_contactos(imgs, ruta)
        print(f"  {ruta}")
    for a in AVISOS:
        print(f"AVISO  {a}", file=sys.stderr)
    sys.exit(1 if any("no entra" in a for a in AVISOS) else 0)


if __name__ == "__main__":
    main()
