#!/usr/bin/env python3
"""
beats.py - convierte un guion de reel en una hoja de tiempos antes de grabarlo.

Portado al español rioplatense para Química Cristal, a partir del beats.py de
instagram-agent-skill (Jake Schincariol, MIT).

Estima cuánto tarda cada línea en decirse, las apila en tiempos y marca las
cuatro cosas que matan un reel en la edición: un hook que pasa los tres
segundos, un bloque tan largo que da tiempo a irse, una racha de líneas sin
nada concreto, y un largo total que no coincide con lo que dijiste que hacías.
También avisa si no hay loop (la última línea no repite nada del hook).

Los tiempos salen de contar palabras a un ritmo dado. Sirven para planificar
el corte, no reemplazan grabarlo. En español a cámara el ritmo natural ronda
las 150 palabras por minuto; si Joaco se cronometró leyendo un guion, pasá su
número con --wpm.

Uso
  python3 beats.py guion.txt
  python3 beats.py guion.txt --target 30
  python3 beats.py guion.txt --wpm 165 --target 45
  python3 beats.py guion.txt --json
"""

import argparse
import json
import re
import sys

LETRAS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
WORD_RE = re.compile(rf"[{LETRAS}0-9$%'’-]+")
SENT_RE = re.compile(r"(?:\d[.,]\d|[^.!?])+[.!?]*")      # no corta en $39.990
CONCRETE_RE = re.compile(
    r"\$\s?\d|\b\d[\d.,]*\b|(?<![.!?¿¡]\s)(?<!^)\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}\b", re.MULTILINE)
NUMEROS_HABLADOS = {
    "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez",
    "quince", "veinte", "treinta", "cincuenta", "cien", "mil", "media", "mitad",
    "doble", "triple",
}
RUBRO = {
    "lavandina", "cloro", "pileta", "detergente", "desengrasante", "bidón",
    "bidones", "sarro", "grasa", "moho", "hongos", "mancha", "manchas",
    "campana", "plancha", "parrilla", "baño", "inodoro", "mampara", "piso",
    "pisos", "ropa", "horno", "vidrio", "lampazo", "trapo", "balde", "mopa",
    "esponja", "alguicida", "clarificador", "granulado", "pastillas",
    "suavizante", "concentrado", "granel", "litro", "litros", "kilo", "kilos",
    "precio", "camión", "pH",
}
STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas", "y", "o", "pero",
    "si", "de", "del", "a", "al", "en", "con", "por", "para", "que", "qué",
    "este", "esta", "esto", "es", "son", "era", "fue", "ser", "estar", "está",
    "vos", "te", "tu", "tus", "yo", "me", "mi", "mis", "nos", "nosotros", "lo",
    "le", "les", "se", "su", "sus", "ya", "no", "sí", "más", "muy", "así",
    "cuando", "como", "cómo", "hay", "eso", "esa", "ese", "ahí", "acá",
}

HOOK_WINDOW = 3.0        # segundos. Pasado esto, el dedo ya decidió.
MAX_BEAT = 4.0           # segundos en una idea sin que cambie nada en pantalla.
ABSTRACT_RUN = 3         # bloques seguidos sin nada chequeable.


def words(text):
    t = re.sub(r"(?<=\d)[.,](?=\d{3}\b)", "", text)
    return WORD_RE.findall(t)


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}"


def concretos(text):
    low = [w.lower() for w in words(text)]
    return (len(CONCRETE_RE.findall(text))
            + sum(1 for w in low if w in NUMEROS_HABLADOS)
            + sum(1 for w in low if w in RUBRO))


def raiz(w):
    w = w.lower().strip("'’¿?¡!.,;:")
    return w[:-2] if w.endswith("es") and len(w) > 5 else (w[:-1] if w.endswith("s") and len(w) > 3 else w)


def split_beats(raw, wps):
    """Una línea es un bloque, salvo que sea demasiado larga para serlo."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if len(words(line)) / wps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            candidate = (buf + " " + part).strip()
            if buf and len(words(candidate)) / wps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, wpm=150, target=None):
    wps = wpm / 60.0
    beats = split_beats(raw, wps)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        n = len(words(text))
        dur = n / wps
        rows.append({"n": i + 1, "start": round(clock, 2), "dur": round(dur, 2), "words": n,
                     "text": text, "concrete": concretos(text), "label": "", "flags": []})
        clock += dur
    total = clock

    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "HOOK"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "HOOK" else "HOOK/CTA"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "MEDIO"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"el hook dura {rows[0]['dur']:.1f}s, pasa los {HOOK_WINDOW:.0f}s")
        notes.append(f"El bloque 1 tarda {rows[0]['dur']:.1f}s en decirse. Cortalo a "
                     f"{int(HOOK_WINDOW * wps)} palabras o menos, o el hook llega cuando el "
                     "dedo ya decidió.")
    if rows[0]["concrete"] == 0:
        notes.append("El bloque 1 no tiene número, nombre ni producto. Los hooks sin nada "
                     "chequeable son los que se pasan de largo.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f}s en un solo bloque")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"Bloque(s) {', '.join(map(str, long_beats))} pasan los {MAX_BEAT:.0f}s. "
                     "Partí la línea o cambiá lo que se ve en pantalla adentro de ella. "
                     "Un plano quieto es donde la gente se va.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Los bloques {start}-{r['n']} no tienen nada concreto. Meté un "
                             "número, un producto o un precio en alguno.")
        else:
            run, start = 0, None

    first = {raiz(w) for w in words(rows[0]["text"]) if w.lower() not in STOPWORDS}
    last = {raiz(w) for w in words(rows[-1]["text"]) if w.lower() not in STOPWORDS}
    loop = sorted(first & last)
    if loop and len(rows) > 1:
        notes.append(f"Loop: el último bloque repite \"{', '.join(loop[:3])}\" del hook. "
                     "La segunda vista es alcance gratis.")
    else:
        notes.append("Sin loop. El último bloque no comparte ninguna palabra con el hook y el "
                     "video termina plano. Repetir una palabra del bloque 1 es la segunda "
                     "vista más barata que hay.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"Largo en objetivo ({total:.1f}s contra {target:g}s).")
        elif delta > 0:
            notes.append(f"{delta:.1f}s de más. Sacá unas {int(delta * wps)} palabras.")
        else:
            notes.append(f"{-delta:.1f}s de menos. Agregá {int(-delta * wps)} palabras o "
                         "grabalo corto. Corto suele estar bien.")

    return {"wpm": wpm, "target": target, "total_seconds": round(total, 2),
            "total_words": sum(r["words"] for r in rows), "beats": rows, "notes": notes}


def render(a, out=sys.stdout):
    head = (f"HOJA DE TIEMPOS  ·  {a['total_words']} palabras  ·  ~{a['total_seconds']:.1f}s "
            f"a {a['wpm']:g} ppm" + (f"  ·  objetivo {a['target']:g}s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<9}" if r["label"] else " " * 9
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<9}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Arma la hoja de tiempos de un guion de reel.")
    ap.add_argument("input", nargs="?", default="-", help="archivo del guion, o - para stdin")
    ap.add_argument("--wpm", type=float, default=150, help="palabras por minuto (default 150)")
    ap.add_argument("--target", type=float, help="largo objetivo en segundos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, wpm=args.wpm, target=args.target)
    if not a:
        print("guion vacío", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
