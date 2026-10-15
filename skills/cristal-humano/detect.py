#!/usr/bin/env python3
"""
detect.py - panel de cinco chequeos que puntúa cuánto parece escrito por una
máquina un borrador en español rioplatense.

Portado y adaptado para Química Cristal a partir del detect.py de
instagram-agent-skill (Jake Schincariol, MIT). El chequeo de VOZ se rehízo para
castellano: en vez de contracciones del inglés mide voseo y habla rioplatense,
y penaliza el tuteo.

Qué es:  cinco heurísticas locales inspiradas en lo que miran los detectores
públicos: variación del largo de las oraciones, cosas concretas, vocabulario de
relleno, huella tipográfica y voz. Todo se calcula acá, con el texto solo.

Qué NO es:  GPTZero, Originality, Copyleaks ni nada parecido. No los llama y no
promete su veredicto. Mide lo mismo de fondo, por eso arreglarlo suele mover
esos números, pero esa es toda la promesa. Nunca le digas a nadie que un texto
es "indetectable".

Cada chequeo da un puntaje HUMANO de 0 a 100. Más alto es mejor.

Uso
  python3 detect.py borrador.txt
  python3 detect.py borrador.txt --json
  python3 detect.py antes.txt despues.txt      # comparar dos versiones
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

LETRAS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(rf"[{LETRAS}']+")
NUMBERS = re.compile(r"\$\s?\d|\b\d[\d.,]*\s?(?:%|kg|l|lts?|litros?|ml|cc|m2)?\b", re.IGNORECASE)
PROPER = re.compile(r"(?<![.!?¿¡]\s)(?<!^)\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}\b", re.MULTILINE)
PRONOMBRES = re.compile(r"\b(yo|me|mi|mis|nosotros|nos|nuestr[oa]s?|vos|te|tu|tus|ustedes)\b", re.IGNORECASE)
VOSEO_RE = re.compile(r"\b[a-záéíóúñ]{2,}(?:ás|és|ís)\b", re.IGNORECASE)
VOSEO_IMP = {"mirá", "dejá", "pará", "tirá", "usá", "probá", "guardá", "comprá", "poné", "echá", "sacá", "agarrá", "hacé", "escribí", "pedí", "elegí", "conocé", "seguí", "comentá", "compartí", "llamá", "visitá", "consultá", "preguntá", "aprovechá", "vení", "decí", "tené", "salí", "andá", "avisá", "contá", "mandá", "sumá", "limpiá", "lavá", "diluí", "cuidá", "evitá", "cambiá", "calculá", "anotá", "pasá", "traé", "llevá", "buscá", "encontrá", "disfrutá", "agregá", "escuchá", "frená", "fijate", "acordate", "olvidate", "sumate", "animate", "apurate", "llevate", "guardate", "anotate", "escribinos", "escribime", "contanos", "contame", "mandanos", "seguinos", "avisanos", "llamanos", "consultanos", "dejanos", "pedilo", "pedila", "probalo", "guardalo", "compartilo", "llevalo", "aprovechalo", "pasate", "vení"}
NO_VERBOS = {"más", "después", "través", "inglés", "país", "jamás", "además", "atrás", "demás",
             "detrás", "cortés", "francés", "mes", "tres", "seis", "gas", "japonés", "interés",
             "revés", "adiós", "maíz", "raíz", "anís", "lápiz", "compás", "estrés", "portugués",
             "cordobés", "holandés", "marqués"}
RIOPLATENSE = {"che", "dale", "posta", "igual", "onda", "tipo", "laburo", "plata", "joya",
               "bárbaro", "ojo", "viste", "mirá", "fijate", "bancá", "listo", "bueno", "re",
               "vos", "sos", "acá", "nomás", "chau", "macanudo", "buenísimo", "barbaro", "copado",
               "ni", "cualquiera", "posta", "bondi", "changuito", "súper", "lucas"}
TUTEO_RE = re.compile(r"\b(?:tú|puedes|tienes|quieres|sabes|eres|debes|necesitas|haces|dices|"
                      r"vienes|piensas|sientes|crees|buscas|usas|contigo|para ti|escríbenos|"
                      r"síguenos|llámanos|contáctanos|descubre|aprovecha)\b", re.IGNORECASE)
RUBRO = {"lavandina", "cloro", "pileta", "piletas", "detergente", "desengrasante", "bidón",
         "bidones", "sarro", "grasa", "moho", "hongos", "campana", "plancha", "parrilla",
         "mampara", "piso", "ropa", "lampazo", "trapo", "balde", "alguicida", "clarificador",
         "granulado", "pastillas", "concentrado", "granel", "camión", "mostrador", "depósito"}


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def check_burstiness(text):
    """La gente varía fuerte el largo de las oraciones. La máquina escribe parejo."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "muy corto para juzgar"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    return scale(cv, human=0.70, machine=0.22), f"variación {cv:.2f} en {len(lens)} oraciones (ideal 0,55+)"


def check_specificity(text):
    """Números, nombres, productos. El relleno es abstracto."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "muy corto para juzgar"
    per100 = 100 / len(w)
    rubro = sum(1 for x in w if x.lower() in RUBRO)
    hits = len(NUMBERS.findall(text)) + len(set(PROPER.findall(text))) + rubro * 0.5
    density = hits * per100
    return scale(density, human=6.0, machine=0.5), f"{hits:g} marcadores concretos, {density:.1f} cada 100 palabras (ideal 4+)"


def check_slop(text, lex):
    w = words(text)
    if not w:
        return 50.0, "vacío"
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        pattern = re.compile(r"(?<![\w])" + re.escape(entry["find"]).replace(r"\ ", r"\s+") + r"(?![\w])",
                             re.IGNORECASE)
        n = len(pattern.findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    detail = f"{hits} términos de relleno, {density:.1f} cada 100 palabras"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return scale(density, human=0.0, machine=4.0), detail


def check_fingerprint(text):
    """Caracteres que el teclado de un celular no produce."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    raya = text.count("—")
    curvas = sum(text.count(c) for c in "‘’“”«»")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "   ")
    total = invisible * 4 + raya * 2 + curvas + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    detail = (f"{invisible} invisibles, {raya} rayas, {curvas} comillas curvas/angulares, "
              f"{ellip} puntos suspensivos, {nbsp} espacios duros")
    return scale(per1k, human=0.0, machine=12.0), detail


def check_voice(text, lex):
    """Voseo, habla de acá, personas, y las formas a las que la IA vuelve siempre."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "muy corto para juzgar"
    per100 = 100 / len(w)
    low = [x.lower() for x in w]
    voseo = [x for x in VOSEO_RE.findall(text) if x.lower() not in NO_VERBOS]
    coloquial = (len(voseo) + sum(1 for x in low if x in RIOPLATENSE or x in VOSEO_IMP)) * per100
    persona = len(PRONOMBRES.findall(text)) * per100
    tuteo = len(TUTEO_RE.findall(text))
    tells, names = 0, []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6
    score = (scale(coloquial, human=3.0, machine=0.0) * 0.35
             + scale(persona, human=6.0, machine=1.0) * 0.35
             + clamp(100 - tells * 22) * 0.30) - tuteo * 15
    if uniform:
        score -= 12
        names.append("viñetas-parejas")
    if tuteo:
        names.insert(0, f"tuteo x{tuteo}")
    detail = (f"{coloquial:.1f} marcas de voseo/habla de acá y {persona:.1f} pronombres cada 100 "
              f"palabras, {tells} marca(s) de estructura")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["RITMO", "CONCRETO", "RELLENO", "HUELLA", "VOZ"]


def run(text, lex):
    results = {
        "RITMO": check_burstiness(text),
        "CONCRETO": check_specificity(text),
        "RELLENO": check_slop(text, lex),
        "HUELLA": check_fingerprint(text),
        "VOZ": check_voice(text, lex),
    }
    scores = [results[c][0] for c in CHECKS]
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    # Dos o más marcas de estructura sin reescribir: no pasa, aunque el resto dé bien.
    # Son justamente lo que el script no arregla solo.
    tells = contar_marcas(text, lex)
    if tells >= 2:
        overall = min(overall, 69.0)
    verdict = "PASA" if overall >= 70 and min(scores) >= 55 else ("REVISAR" if overall >= 50 else "MARCADO")
    return results, overall, verdict


def contar_marcas(text, lex):
    n = 0
    for s in lex["structures"]:
        try:
            n += len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
    return n


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PANEL DE DETECCIÓN" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<9} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<9} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'HUMANO':<9} {bar(overall)} {overall:5.1f}   {verdict}", file=out)
    if verdict != "PASA":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Lo más flojo: {weakest}. Arreglá eso primero.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Puntúa cuánto parece de máquina un borrador.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para stdin")
    ap.add_argument("compare", nargs="?", help="segundo archivo, para ver antes/después")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()
    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        payload.append({"source": name,
                        "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
                        "human_score": round(overall, 1), "verdict": verdict})

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {a['human_score']:.1f} {a['verdict']}  ->  {b['human_score']:.1f} {b['verdict']}   ({delta:+.1f})\n")

    sys.exit(0 if payload[-1]["verdict"] == "PASA" else 1)


if __name__ == "__main__":
    main()
