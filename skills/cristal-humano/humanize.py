#!/usr/bin/env python3
"""
humanize.py - le saca la huella de máquina a un borrador en español rioplatense.

Portado y ampliado para Química Cristal a partir del humanize.py de
instagram-agent-skill (Jake Schincariol, MIT).

Cuatro pasadas, en este orden:

  1. INVISIBLES   borra o normaliza caracteres que un teclado no produce:
                  espacios de ancho cero, unidores, guiones blandos, BOM,
                  caracteres de etiqueta Unicode, espacios duros y finos.
  2. TIPOGRAFÍA   raya -> coma, comillas curvas y angulares -> rectas,
                  puntos suspensivos de un carácter -> tres puntos, viñeta -> guion.
                  Los signos de apertura ¿ ¡ no se tocan: son castellano, no máquina.
  3. LÉXICO       reemplaza el léxico de slop.json (muletillas de IA, folleto,
                  regionalismos ajenos y tuteo) por palabras llanas, respetando
                  mayúsculas y sin tocar URLs.
  4. VOSEO        pasa a voseo los imperativos en tuteo al principio de oración
                  ("Descubre nuestra línea" -> "Conocé nuestra línea").

Las marcas estructurales (tríadas, "no es solo X, es Y", muro de hashtags,
"precio por privado") se REPORTAN, nunca se reescriben solas: cambiar la forma
de una oración necesita criterio, y eso es trabajo del modelo, no de una regex.

Uso
  python3 humanize.py borrador.txt
  python3 humanize.py borrador.txt --report
  python3 humanize.py borrador.txt -o limpio.txt --report
  python3 humanize.py borrador.txt --json
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+|wa\.me/\S+")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
MAYUS = "A-ZÁÉÍÓÚÜÑ"
MINUS = "a-záéíóúüñ"


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n, "action": entry["action"]})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "otros caracteres de formato invisibles", "count": len(stray), "action": "delete"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n, "to": entry["to"].strip() or "(espacio)"})
        if ch == "—":
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)
            text = re.sub(r"\s+–\s+", ", ", text)
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    text = re.sub(r"(?m)^\s*,\s*", "", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def _pattern(find):
    return re.compile(r"(?<![\w])" + re.escape(find).replace(r"\ ", r"\s+") + r"(?![\w])",
                      re.IGNORECASE)


def pass_lexical(text, lex):
    """Reemplaza palabras y frases. Las más largas primero, así ganan las frases."""
    hits = []
    entries = sorted(lex["phrases"] + lex["words"], key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        pattern = _pattern(entry["find"])
        found = pattern.findall(text)
        if not found:
            continue
        hits.append({"find": entry["find"], "replace": entry["replace"] or "(borrado)",
                     "count": len(found), "family": entry["family"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    return text, hits


def pass_imperativos(text, lex):
    """Imperativos en tuteo al principio de oración -> voseo."""
    hits = []
    for e in lex.get("imperativos_tuteo", []):
        pat = re.compile(r"(?:(?<=^)|(?<=\n)|(?<=[.!?]\s)|(?<=[¡¿]))" + re.escape(e["find"])
                         + r"\b" + (e["requiere"] or ""), re.MULTILINE)
        found = pat.findall(text)
        if found:
            hits.append({"find": e["find"], "replace": e["replace"], "count": len(found), "family": "voseo"})
            text = pat.sub(e["replace"], text)
    return text, hits


def cleanup(text):
    """Borrar una cláusula entera deja puntuación huérfana. Esto la limpia."""
    text = re.sub(r"¿\s*\?|¡\s*!", "", text)                 # "¿Qué esperás?" borrado
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t]+(?=\S)", "", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r"([¿¡])\s+", r"\1", text)
    text = text.replace("...", "\x00ELL\x00")
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00ELL\x00", "...")
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r",\s*(también|entonces|igual|así que)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({"name": f"Oraciones todas del mismo largo (variación {cv:.2f})", "count": len(lens),
                          "fix": "Partí una oración al medio. Dejá que otra se estire. La máquina escribe parejo."})
    return flags


def restore_capitals(original, text):
    """Borrar una apertura deja la palabra siguiente en minúscula. Solo se
    corrige si el que escribe usa mayúscula al empezar: una voz en minúsculas
    a propósito es estilo, no un error."""
    starts = re.findall(rf"(?:^|[.!?]\s+|\n)\s*[¿¡]?([{MAYUS}{MINUS}])", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(rf"((?:^|[.!?] |\n)\s*[¿¡]?)([{MINUS}])",
                  lambda m: m.group(1) + m.group(2).upper(), text)


def humanize(text, lex):
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi = pass_lexical(text, lex)
    text, imp = pass_imperativos(text, lex)
    text = cleanup(text)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi + imp,
        "structures": scan_structures(text, lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for k in ("invisible", "typographic", "lexical") for h in report[k])
    head("REPORTE DEL HUMANIZADOR")
    print(f"{total} marcas de máquina sacadas, {len(report['structures'])} marcas de estructura "
          "para reescribir a mano", file=out)
    if report["invisible"]:
        head("1. CARACTERES INVISIBLES")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['action']}", file=out)
    if report["typographic"]:
        head("2. TIPOGRAFÍA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. LÉXICO, REGIONALISMOS Y VOSEO")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["structures"]:
        head("4. MARCAS DE ESTRUCTURA  (no se arreglan solas: reescribilas vos)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("LIMPIO")
        print("  No había nada para sacar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Le saca la huella de máquina a un borrador.")
    ap.add_argument("input", nargs="?", default="-", help="archivo, o - para stdin")
    ap.add_argument("-o", "--out", help="escribir el texto limpio acá en vez de stdout")
    ap.add_argument("--report", action="store_true", help="mostrar qué cambió (por stderr)")
    ap.add_argument("--json", action="store_true", help="salida {text, report} en JSON")
    ap.add_argument("--lexicon", default=LEX, help="ruta a slop.json")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"escrito: {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
