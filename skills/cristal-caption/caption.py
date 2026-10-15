#!/usr/bin/env python3
"""
caption.py - revisa un caption de Instagram de Química Cristal y muestra
exactamente lo que se ve en el feed antes del "... más".

Portado y ampliado a partir del caption.py de instagram-agent-skill
(Jake Schincariol, MIT). Lo nuevo de esta versión: pedidos de acción en
rioplatense, chequeo de PRECIO VISIBLE (en Argentina "precio por privado"
espanta), mención de la ciudad para búsqueda local, y aviso de teléfonos y
links de WhatsApp en el cuerpo, que en un caption no se pueden tocar.

Instagram muestra unos 125 caracteres en el feed y esconde el resto detrás de
un toque. Casi todos los captions que fallan, fallan ahí. El corte en 125 es
aproximado: cambia con el celular y los saltos de línea, por eso conviene
margen y no un caption calculado para terminar justo ahí.

Uso
  python3 caption.py caption.txt
  python3 caption.py caption.txt --keywords "cloro para pileta,limpieza de piletas"
  python3 caption.py caption.txt --local "Río Cuarto"
  python3 caption.py caption.txt --oferta          # es un post de promo: exige precio
  python3 caption.py caption.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

LIMIT = 2200
TRUNCATE = 125
HASHTAG_LIMIT = 5        # Tope de Instagram por post o reel desde el 18-dic-2025 (antes 30).

HASHTAG_RE = re.compile(r"(?:^|\s)(#[\wÁÉÍÓÚÜÑáéíóúüñ]+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[A-Za-z0-9_.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\bwa\.me/\S*|\b[a-z0-9-]+\.(?:com|com\.ar|ar|net|org|io|app)(?:/\S*)?\b",
                     re.IGNORECASE)
PHONE_RE = re.compile(r"(?:\+?54\s?9?\s?)?\(?0?3\d{2,3}\)?[\s-]?(?:15[\s-]?)?\d{3}[\s-]?\d{4}\b|\b\d{10}\b")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
PRICE_RE = re.compile(r"\$\s?\d{1,3}(?:\.\d{3})+(?:,\d+)?|\$\s?\d+(?:,\d+)?")
CONCRETE_RE = re.compile(r"\$\s?\d|\b\d[\d.,]*\b|(?<![.!?¿¡]\s)(?<!^)\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}\b", re.MULTILINE)
OFERTA_RE = re.compile(r"(?i)\b(?:promo|promoción|oferta|descuento|combo|liquidación|2x1|3x2|10\s?\+\s?1|llevá \d+)\b")
PRIVADO_RE = re.compile(r"(?i)\bprecios? (?:por|al|en) (?:privado|dm|md|inbox|interno)\b|\bconsult(?:á|a|ar) (?:el )?precio\b")
TUTEO_RE = re.compile(r"\b(?:tú|puedes|tienes|quieres|sabes|eres|necesitas|escríbenos|síguenos|"
                      r"llámanos|contáctanos|pídelo|descubre|aprovecha)\b", re.IGNORECASE)

ASKS = [
    (re.compile(r"(?i)\bcoment(?:á|a|en)\s+(?:la palabra\s+)?[\"“']?[A-ZÁÉÍÓÚÑ0-9]{3,}\b"), "comentar una palabra clave"),
    (re.compile(r"(?i)\b(?:escribinos|escribime|mandanos|mandame|hablanos)\b|\bpedilo\b|\bhacé tu pedido\b"), "escribir / pedir"),
    (re.compile(r"(?i)\bguard(?:á|alo|ala|ate)\b"), "guardar"),
    (re.compile(r"(?i)\bcompart(?:í|ilo|ila)\b|\bmandáselo\b|\bpasáselo\b"), "compartir / mandárselo a alguien"),
    (re.compile(r"(?i)\bsegu(?:inos|ime)\b"), "seguir"),
    (re.compile(r"(?i)\blink (?:en|de) (?:la |mi |nuestra )?bio\b"), "link de la bio"),
    (re.compile(r"(?i)\bdesliz(?:á|a)\b|\bpasá (?:las fotos|a la derecha)\b"), "deslizar"),
    (re.compile(r"(?i)\bcontanos\b|\bcontame\b|\b¿(?:cuál|qué|cuánto|cuántos)\b"), "responder una pregunta"),
    (re.compile(r"(?i)\bvení(?:te)? al local\b|\bpasá por el local\b|\bte esperamos en\b"), "venir al local"),
]

FILLER_TAGS = {"#viral", "#parati", "#fyp", "#foryou", "#foryoupage", "#explore", "#explorepage",
               "#explorar", "#reels", "#reelsinstagram", "#instagood", "#tendencia", "#trending",
               "#follow", "#like4like", "#instadaily", "#argentina", "#love", "#viralreels"}


def visible_window(text, cut):
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  LO QUE MUESTRA EL FEED", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... más" if truncated else "(entra entero)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None, local=None, oferta=False):
    stripped = text.strip()
    chars = len(stripped)
    lines = stripped.split("\n")
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    phones = PHONE_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(stripped)]
    if "escribir / pedir" in asks and "link de la bio" in asks:
        asks.remove("link de la bio")      # "pedilo desde el link de la bio" es un solo pedido
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]
    es_oferta = oferta or bool(OFERTA_RE.search(stripped))
    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LARGO", "FALLA" if chars > LIMIT else "OK",
        f"{chars} / {LIMIT} caracteres" + (f", {chars - LIMIT} de más" if chars > LIMIT else ""))

    if not first_line:
        add("PRIMERA LÍNEA", "FALLA", "el caption arranca con una línea vacía")
    elif first_line.startswith(("#", "@")):
        add("PRIMERA LÍNEA", "FALLA", "arranca con hashtag o mención, el único lugar que vale una oración")
    elif re.match(r"(?i)^\s*[¡¿]?\s*(?:hola|buenas|buen d[ií]a|qu[eé] tal)\b", first_line):
        add("PRIMERA LÍNEA", "FALLA", "arranca saludando. Nadie entra al feed para que lo saluden")
    elif len(first_line) > cut:
        add("PRIMERA LÍNEA", "OJO", f"{len(first_line)} caracteres, se corta en {cut} a mitad de idea. "
                                    "Sirve si el corte deja intriga; no si corta una subordinada")
    else:
        add("PRIMERA LÍNEA", "OK", f"{len(first_line)} caracteres, entra entera")

    add("GANCHO CONCRETO", "OK" if CONCRETE_RE.search(window) else "OJO",
        f"{len(CONCRETE_RE.findall(window))} número(s) o nombre(s) antes del corte"
        + ("" if CONCRETE_RE.search(window) else " - nada chequeable antes del toque"))

    if PRIVADO_RE.search(stripped):
        add("PRECIO VISIBLE", "FALLA", "dice 'precio por privado'. En Argentina espanta: poné el precio "
                                       "de Odoo, o explicá en una línea por qué varía")
    elif es_oferta:
        prices = PRICE_RE.findall(stripped)
        if not prices:
            add("PRECIO VISIBLE", "FALLA", "es una promo y no tiene precio. Una oferta sin precio es un aviso de intriga")
        elif not PRICE_RE.search(window):
            add("PRECIO VISIBLE", "OJO", f"el precio ({prices[0]}) quedó abajo del corte. En una promo va arriba")
        else:
            add("PRECIO VISIBLE", "OK", f"precio a la vista antes del corte: {PRICE_RE.search(window).group(0)}")

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGS", "FALLA", f"{len(tags)} hashtags, más del tope de {HASHTAG_LIMIT} de Instagram. "
                                 "Los que pasan el quinto no cuentan y el bloque se ve viejo")
    elif filler:
        add("HASHTAGS", "OJO", f"{len(tags)} hashtags, {len(filler)} genéricos ({', '.join(filler[:3])}). No describen nada")
    else:
        add("HASHTAGS", "OK", f"{len(tags)} hashtag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if tags and any(re.search(r"(?:^|\s)" + re.escape(t) + r"(?!\w)", window) for t in tags):
        add("UBICACIÓN TAGS", "OJO", "hay un hashtag adentro de lo visible, gastando lugar del feed en una etiqueta")

    if links:
        add("LINKS", "OJO", f"{len(links)} link(s) en el caption ({links[0]}). En el caption no se pueden "
                            "tocar: van en la bio, en el botón de WhatsApp o por mensaje")
    if phones:
        add("TELÉFONO", "OJO", f"teléfono en el cuerpo ({phones[0]}). Tampoco se puede tocar. Sirve para el que "
                               "lo copia; el camino corto es el botón de WhatsApp del perfil")

    if len(asks) == 1:
        add("UN PEDIDO", "OK", f"un solo pedido: {asks[0]}")
    elif not asks:
        add("UN PEDIDO", "OJO", "no pide ninguna acción. Decidí para qué es este post")
    else:
        add("UN PEDIDO", "OJO", f"{len(asks)} pedidos ({', '.join(asks)}). Dos pedidos es igual a ninguno")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJIS", "OJO" if density > 4 else "OK",
        f"{len(emoji)} emoji, {density:.1f} cada 100 caracteres" + (" - se lee como adorno" if density > 4 else ""))

    tuteo = TUTEO_RE.findall(stripped)
    if tuteo:
        add("VOSEO", "FALLA", f"tuteo ({', '.join(sorted(set(t.lower() for t in tuteo))[:3])}). "
                              "En una cuenta de Río Cuarto suena a traducción: pasá el texto por cristal-humano")

    if local:
        low = stripped.lower()
        found = local.lower() in low or local.lower().replace("í", "i") in low
        add("BÚSQUEDA LOCAL", "OK" if found else "OJO",
            f"menciona {local}" if found else f"no menciona {local}. El buscador de Instagram lee el texto: "
                                              "nombrá la ciudad en una oración normal")

    if keywords:
        low = stripped.lower()
        found = [k for k in keywords if k.lower() in low]
        missing = [k for k in keywords if k.lower() not in low]
        in_window = [k for k in found if k.lower() in window.lower()]
        status = "OK" if not missing else ("OJO" if found else "FALLA")
        add("TÉRMINOS", status, f"{len(found)}/{len(keywords)} presentes"
            + (f", {len(in_window)} antes del corte" if found else "")
            + (f". Faltan: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "FALLA")
    warns = sum(1 for c in checks if c["status"] == "OJO")
    verdict = "ARREGLAR" if fails else ("REVISAR" if warns else "LISTO")
    return {"characters": chars, "limit": LIMIT, "truncate_at": cut, "visible": window,
            "truncated": truncated, "first_line_chars": len(first_line), "hashtags": tags,
            "links": links, "phones": phones, "emoji": len(emoji), "asks": asks,
            "es_oferta": es_oferta, "checks": checks, "verdict": verdict}


def render(a, out=sys.stdout):
    head = (f"REVISIÓN DE CAPTION  ·  {a['characters']} / {a['limit']} car.  ·  "
            f"{len(a['hashtags'])} hashtags  ·  {len(a['asks'])} pedido(s)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<6} {c['check']:<16} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VEREDICTO  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisa un caption de Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="archivo del caption, o - para stdin")
    ap.add_argument("--truncate", type=int, default=TRUNCATE, help=f"caracteres antes del '... más' (default {TRUNCATE})")
    ap.add_argument("--keywords", default="", help="términos de búsqueda separados por coma")
    ap.add_argument("--local", default="", help="ciudad o localidad que tiene que aparecer (ej. 'Río Cuarto')")
    ap.add_argument("--oferta", action="store_true", help="es un post de promo: exige precio visible")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","), local=args.local or None,
                oferta=args.oferta)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "LISTO" else 1)


if __name__ == "__main__":
    main()
