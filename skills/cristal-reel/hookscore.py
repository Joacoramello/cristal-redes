#!/usr/bin/env python3
"""
hookscore.py - puntúa la primera línea de un reel en las cinco cosas que tienen
en común los hooks que frenan el dedo, y rankea varios contra sí.

Portado al español rioplatense y al rubro limpieza para Química Cristal, a
partir del hookscore.py de instagram-agent-skill (Jake Schincariol, MIT).

Qué es:  cinco heurísticas locales, calculadas con el texto solo. Miden cosas
que comparten los hooks que retienen: un largo que se dice en menos de tres
segundos, algo concreto, algo en juego, la carga al principio y no al final, y
alguien a quien se le habla.

Qué NO es:  un predictor de vistas. El original se validó en inglés: separa
bien un hook flojo de uno real (AUC 0,83) y casi nada un éxito de un fracaso
del mismo creador (AUC 0,56, una moneda es 0,50). Esta versión en español no
está validada contra datos reales todavía. Usala para lo que sirve: matar
saludos, preámbulos, hooks sin nada concreto, hooks en tuteo y hooks que
tardan cinco segundos en decirse. Cuál de dos hooks decentes funciona lo decide
tu cara, el corte, el audio y a quién se lo muestra Instagram. Confiá en el
gráfico de retención antes que en este script.

Cada chequeo da de 0 a 100. Más alto es mejor.

Uso
  python3 hookscore.py hooks.txt               # un hook por línea, rankeados
  python3 hookscore.py --hook "Nadie te dice que la lavandina se vence."
  python3 hookscore.py hooks.txt --json
"""

import argparse
import json
import re
import statistics
import sys

LETRAS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
WORD_RE = re.compile(rf"[{LETRAS}0-9$%'’-]+")
NUMBER_RE = re.compile(
    r"\$\s?\d[\d.]*(?:,\d+)?"                                   # plata: $39.990
    r"|\b\d[\d.]*(?:,\d+)?\s?"                                  # una cifra, con o
    r"(?:%|x\b|kg\b|kilos?\b|g\b|l\b|lts?\b|litros?\b|cc\b|ml\b|m2\b"  # sin unidad
    r"|hs\b|horas?\b|min\b|minutos?\b|segundos?\b|días?\b|semanas?\b|meses\b|mes\b|años?\b)?",
    re.IGNORECASE)
PROPER_RE = re.compile(r"(?<![.!?¿¡]\s)(?<!^)\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Los números dichos en voz alta son tan concretos como los escritos.
# "un/una/uno" y "primero" no están: son relleno mucho más seguido que cantidad.
NUMEROS_HABLADOS = {
    "cero", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
    "diez", "once", "doce", "quince", "veinte", "treinta", "cuarenta",
    "cincuenta", "sesenta", "setenta", "ochenta", "noventa", "cien", "ciento",
    "doscientos", "trescientos", "quinientos", "mil", "millón", "millones",
    "docena", "mitad", "doble", "triple", "media",
}
PALABRAS_PLATA = {
    "pesos", "peso", "lucas", "luca", "palos", "plata", "mangos", "precio",
    "ahorro", "ahorrás", "ahorrar", "gastás", "gasto", "costo", "cuesta",
    "sale", "salen", "vale", "oferta", "promo", "descuento", "gratis",
    "envío", "litro", "kilo", "bidón", "bidones",
}
# Sustantivos del rubro: un hook que nombra la cosa (la pileta, la grasa, el
# sarro) es más concreto que uno que habla de "la limpieza" en abstracto.
RUBRO = {
    "lavandina", "cloro", "pileta", "piletas", "detergente", "desengrasante",
    "bidón", "bidones", "sarro", "grasa", "moho", "hongos", "mancha", "manchas",
    "campana", "plancha", "parrilla", "baño", "inodoro", "mampara", "azulejos",
    "piso", "pisos", "cerámico", "porcelanato", "alfombra", "ropa", "cocina",
    "horno", "heladera", "vidrio", "vidrios", "lampazo", "trapo", "balde",
    "mopa", "escoba", "secador", "esponja", "guantes", "bolsas", "alguicida",
    "clarificador", "granulado", "pastillas", "suavizante", "jabón", "perfumina",
    "aromatizante", "desinfectante", "limpiador", "concentrado", "granel",
    "agua", "olor", "camión", "almacén", "bar", "restaurante", "hotel",
    "consorcio", "colegio", "club",
}

# Palabras que ponen algo en juego. Sin ninguna, el hook es una afirmación;
# con una, es un motivo para seguir mirando.
EN_JUEGO = {
    "no", "nunca", "jamás", "nadie", "ningún", "ninguna", "nada", "error",
    "errores", "mal", "pierde", "perdés", "perdí", "perdimos", "tirás", "tirando",
    "tiraste", "gastás", "cuesta", "costó", "caro", "estafa", "mentira",
    "verdad", "secreto", "ojo", "cuidado", "peligro", "peligroso", "tóxico",
    "mezclar", "mezcles", "dejá", "basta", "pará", "sin", "pero", "aunque",
    "hasta", "antes", "todavía", "ya", "solo", "sólo", "gratis", "ahorrás",
    "rinde", "dura", "arruina", "arruinás", "arruinando", "comé", "come",
    "verde", "vence", "vencida", "problema", "peor", "falso", "mito", "vs",
    "contra", "recién", "único", "única", "nadie", "evitá", "nunca", "rompe",
    "rompés", "quema", "mancha", "manchás", "deja", "dejás", "olvidate",
}

# Aperturas que gastan el primer segundo sin decir nada.
APERTURAS_FLOJAS = [
    "hola", "buenas", "buen día", "buenos días", "buenas tardes", "qué tal",
    "que tal", "chicos", "chicas", "gente", "bueno", "bien", "entonces", "hoy",
    "este", "esto", "eh", "ehh", "les quiero", "te quiero contar", "quería",
    "les cuento", "te cuento", "vengo a", "en este", "en el video", "cómo están",
    "como están", "bienvenidos", "hay", "esto es", "a ver", "sabías", "sabían",
    "alguna vez", "les traigo", "te traigo", "les voy", "te voy", "me pidieron",
    "como saben", "como sabés", "obviamente", "básicamente", "la verdad",
    "simplemente", "en", "el día de hoy",
]

# Imperativos en voseo que se ganan la primera posición.
IMPERATIVOS = {
    "dejá", "pará", "tirá", "usá", "probá", "mirá", "guardá", "guardate",
    "comprá", "poné", "echá", "sacá", "agarrá", "hacé", "copiá", "robate",
    "no", "nunca", "evitá", "cambiá", "limpiá", "diluí", "calculá", "fijate",
    "ojo", "anotá", "anotate", "olvidate", "frená", "escuchá",
}

# Tuteo: en una cuenta de Río Cuarto suena a traducción o a texto generado.
TUTEO_RE = re.compile(
    r"\b(?:tú|puedes|tienes|quieres|sabes|eres|debes|necesitas|haces|dices|"
    r"vienes|piensas|sientes|crees|buscas|usas|limpias|compras tu|mira esto|"
    r"descubre|aprovecha|escríbenos|síguenos|llámanos|contáctanos|pídelo|"
    r"haz)\b", re.IGNORECASE)

# Segunda persona en voseo: "tenés", "querés", "podés", "limpiás"...
VOSEO_RE = re.compile(r"\b[a-záéíóúñ]{2,}(?:ás|és|ís)\b", re.IGNORECASE)
VOSEO_IMP = {"mirá", "dejá", "pará", "tirá", "usá", "probá", "guardá", "comprá", "poné", "echá", "sacá", "agarrá", "hacé", "escribí", "pedí", "elegí", "conocé", "seguí", "comentá", "compartí", "llamá", "visitá", "consultá", "preguntá", "aprovechá", "vení", "decí", "tené", "salí", "andá", "avisá", "contá", "mandá", "sumá", "limpiá", "lavá", "diluí", "cuidá", "evitá", "cambiá", "calculá", "anotá", "pasá", "traé", "llevá", "buscá", "encontrá", "disfrutá", "agregá", "escuchá", "frená", "fijate", "acordate", "olvidate", "sumate", "animate", "apurate", "llevate", "guardate", "anotate", "escribinos", "escribime", "contanos", "contame", "mandanos", "seguinos", "avisanos", "llamanos", "consultanos", "dejanos", "pedilo", "pedila", "probalo", "guardalo", "compartilo", "llevalo", "aprovechalo", "pasate", "vení"}
NO_VERBOS = {"más", "después", "través", "inglés", "país", "jamás", "además",
             "atrás", "demás", "detrás", "cortés", "francés", "mes", "res",
             "tres", "seis", "gas", "japonés", "interés", "revés", "adiós",
             "maíz", "raíz", "anís", "parís", "lápiz", "compás", "ciprés",
             "marqués", "estrés", "portugués", "holandés", "cordobés"}

DEALBREAKERS = [
    (re.compile(r"(?i)^\s*[¡¿]?\s*(?:no scrollees|par[aá] de scrollear|no pases|esper[aá],? no pases|no te vayas)"),
     "Arranca pidiendo atención. Pedirla es la prueba de que todavía no te la ganaste."),
    (re.compile(r"(?i)\b(?:en (?:este|el) (?:video|reel)(?: de hoy)?|hoy (?:les|te) (?:voy a|traigo|quiero)|(?:les|te) voy a (?:mostrar|enseñar|contar)|vengo a (?:mostrar|contar))\b"),
     "Preámbulo de video. Borralo y arrancá por el resultado."),
    (re.compile(r"(?i)^\s*[¡¿]?\s*(?:hola|buenas|buen d[ií]a|buenos d[ií]as|qu[eé] tal|bienvenid[oa]s|c[oó]mo est[aá]n)\b"),
     "Saludo. Nadie entró al feed para que lo saluden."),
    (HASHTAG_RE,
     "Hashtag en el hook. Los hashtags van abajo del caption, si van."),
    (EMOJI_RE,
     "Emoji en el hook. A tamaño de hook, en pantalla entran palabras o un emoji, no las dos cosas."),
    (TUTEO_RE,
     "Tuteo. En una cuenta de Río Cuarto suena a traducción o a texto generado: pasalo a voseo."),
]


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # "$39.990" es una palabra cuando se dice, así que acá también.
    t = re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", text)
    return WORD_RE.findall(t)


def limpiar(w):
    return w.lower().strip("'’¿?¡!.,;:\"")


def check_length(text):
    """Un hook tiene que llegar antes de que se mueva el dedo. Unos tres segundos."""
    w = words(text)
    n = len(w)
    secs = n / 2.5                       # ~150 palabras por minuto, hablado
    chars = len(text.strip())
    if 5 <= n <= 13:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 13) * 11)
    if chars > 70:                       # dos renglones de texto grande en pantalla
        score -= 12
    return clamp(score), f"{n} palabras, {chars} caracteres, ~{secs:.1f}s hablado (ideal 5-13 palabras)"


def check_specificity(text):
    """Una cosa concreta le gana a tres abstractas."""
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propers = set(PROPER_RE.findall(text))
    low = [limpiar(w) for w in words(text)]
    habladas = [w for w in low if w in NUMEROS_HABLADOS or w in PALABRAS_PLATA]
    rubro = sorted({w for w in low if w in RUBRO})
    hits = len(nums) + len(propers) + len(habladas) + min(len(rubro), 2) * 0.5
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + habladas[:2] + rubro[:2])
    return score, (f"{hits:g} marcador(es) concreto(s)" + (f": {found}" if found else
                   " - ni número, ni nombre, ni producto: nada que se pueda chequear"))


def check_stakes(text):
    """Tensión, costo, negación. Algo que el que mira puede perder."""
    w = [limpiar(x) for x in words(text)]
    markers = sorted({x for x in w if x in EN_JUEGO})
    if re.search(r"\$\s?\d", text):
        markers.append("un precio")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} marcador(es) de tensión" + (f": {', '.join(markers[:4])}" if markers else
                                              " - no hay nada en juego en esta línea")
    return clamp(score), detail


def check_frontload(text):
    """Lo interesante no puede estar en la palabra nueve."""
    w = words(text)
    if not w:
        return 0.0, "vacío"
    low = [limpiar(x) for x in w]
    opener = " ".join(low[:3])
    penalty, hit_opener = 0, None
    for weak in APERTURAS_FLOJAS:
        if opener == weak or opener.startswith(weak + " ") or low[0] == weak:
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        if (token in EN_JUEGO or token in NUMEROS_HABLADOS or token in PALABRAS_PLATA
                or token in RUBRO or NUMBER_RE.match(w[i]) or (i and PROPER_RE.match(w[i]))):
            payload = i
            break
    if payload is None:
        base, where = 30.0, "no hay ninguna palabra con carga en toda la línea"
    elif payload <= 3:
        base, where = 100.0, f"carga en la palabra {payload + 1}"
    elif payload <= 6:
        base, where = 70.0, f"carga en la palabra {payload + 1}, se puede adelantar"
    else:
        base, where = 40.0, f"carga en la palabra {payload + 1}, demasiado tarde"
    detail = where + (f"; apertura floja \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text):
    """Le habla a una persona, o flota en el aire."""
    low = text.lower()
    w = [limpiar(x) for x in words(text)]
    if TUTEO_RE.search(text):
        return 40.0, "le habla al que mira, pero en tuteo"
    voseo = [x for x in VOSEO_RE.findall(low) if x.lower() not in NO_VERBOS]
    voseo += [x for x in w if x in VOSEO_IMP and x not in voseo]
    if re.search(r"\b(vos|te|tu|tus|contigo|vení)\b", low) or voseo:
        return 100.0, "le habla al que mira" + (f" (\"{voseo[0]}\")" if voseo else "")
    if w and w[0] in IMPERATIVOS:
        return 90.0, f"arranca con imperativo (\"{w[0]}\")"
    if re.search(r"\b(ustedes|les)\b", low):
        return 80.0, "le habla a un grupo (ustedes)"
    if re.search(r"\b(yo|mi|mis|me|nosotros|nuestro|nuestra|nuestros|nos)\b", low) or \
            re.search(r"\b\w+(?:amos|emos|imos)\b", low):
        return 70.0, "primera persona, no hay nadie del otro lado"
    return 35.0, "tercera persona, no le habla a nadie"


CHECKS = ["LARGO", "CONCRETO", "EN JUEGO", "ADELANTE", "A QUIÉN"]


def run(text):
    results = {
        "LARGO": check_length(text),
        "CONCRETO": check_specificity(text),
        "EN JUEGO": check_stakes(text),
        "ADELANTE": check_frontload(text),
        "A QUIÉN": check_address(text),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # La propiedad más floja pone el techo: con una sola mala, el dedo sigue.
    overall = clamp(statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15)
    verdict = "FUERTE" if overall >= 70 and min(scores) >= 55 and not flags else (
        "ZAFA" if overall >= 50 else "FLOJO")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nPUNTAJE DEL HOOK", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<10} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<10} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'HOOK':<10} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    for f in flags:
        print(f"\n  FATAL  {f}", file=out)
    if verdict != "FUERTE":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Lo más flojo: {weakest}. Arreglá eso y volvé a correrlo.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nRANKING DE HOOKS\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {r['score']:5.1f} {r['verdict']:<7} {hook}", file=out)
        print(f"        más flojo: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        fatal: {f}", file=out)
    print("\nGrabá el primero. Si el primero está abajo de 50, ninguno de estos es el hook.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Puntúa el hook de un reel en cinco propiedades.")
    ap.add_argument("input", nargs="?", default="-", help="archivo con un hook por línea, o -")
    ap.add_argument("--hook", help="puntuar un solo hook pasado por línea de comandos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("no hay nada para puntuar", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0])
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
