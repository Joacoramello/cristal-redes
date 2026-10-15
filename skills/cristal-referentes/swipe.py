#!/usr/bin/env python3
"""
swipe.py - rankea los reels que juntaste según cuánto le ganaron a su propia
cuenta, nombra la fórmula de hook de cada uno y arma el archivo de referentes.

Portado al español para Química Cristal a partir del swipe.py de
instagram-agent-skill (Jake Schincariol, MIT).

La idea es una sola corrección: las vistas solas no prueban nada. Una cuenta
de 2 millones que hace 400 mil vistas tuvo un martes tranquilo. Una de 4 mil
que hace 400 mil encontró algo, y ese algo se puede copiar (la forma, nunca el
video). Por eso se ordena por el MÚLTIPLO sobre la mediana de la propia cuenta.

Entrada: un archivo separado por tabulaciones, una fila por reel, con encabezado:

    cuenta    seguidores   mediana   vistas   hook                         formato   largo   cta
    @alguien  4800         1200      38000    nadie te dice que el cloro...  reel      28      comentá PILETA

Obligatorias: vistas y hook. `mediana` es lo típico de esa cuenta en sus
últimos 12 reels: es la mejor base. Si solo tenés seguidores, el script avisa.

Uso
  python3 swipe.py capturados.tsv
  python3 swipe.py capturados.tsv --md referentes.md
  python3 swipe.py capturados.tsv --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LETRAS = "A-Za-zÁÉÍÓÚÜÑáéíóúüñ"
WORD_RE = re.compile(rf"[{LETRAS}0-9$%'’-]+")

ALIAS = {"account": "cuenta", "followers": "seguidores", "median": "mediana", "views": "vistas",
         "reproducciones": "vistas", "length": "largo", "segundos": "largo", "format": "formato",
         "link": "url"}


def buscar(nombre):
    """Busca un archivo hermano: en esta carpeta, o en la skill cristal-reel."""
    for base in (HERE, os.path.join(HERE, "..", "cristal-reel")):
        p = os.path.join(base, nombre)
        if os.path.exists(p):
            return p
    return None


_hs = buscar("hookscore.py")
score_hook = None
if _hs:
    try:
        sys.path.insert(0, os.path.dirname(_hs))
        from hookscore import run as score_hook  # noqa: E402
    except Exception:
        score_hook = None


def load_formulas(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    by_id = {h["id"]: h for h in d["hooks"]}
    order = d.get("orden_clasificacion") or sorted(by_id)
    return [(i, by_id[i]["nombre"], re.compile(by_id[i]["match"], re.IGNORECASE)) for i in order if i in by_id]


def classify(hook, formulas):
    if not formulas:
        return None, "sin clasificar"
    for fid, name, pattern in formulas:
        if pattern.search(hook):
            return fid, name
    return None, "sin clasificar"


def numero(v):
    v = (v or "").strip().lower().replace(" ", "")
    m = re.match(r"^([\d.,]+)\s*(k|mil|m|mill|millones)?$", v)
    if not m:
        d = re.sub(r"[^\d]", "", v)
        return int(d) if d else None
    base, suf = m.group(1), m.group(2)
    if suf:
        base = float(base.replace(".", "").replace(",", ".")) if "," in base else float(base)
        return int(base * (1000 if suf in ("k", "mil") else 1_000_000))
    return int(re.sub(r"[^\d]", "", base) or 0)


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    head = [ALIAS.get(c.strip().lower(), c.strip().lower()) for c in lines[0].split("\t")]
    if "vistas" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["cuenta", "seguidores", "vistas", "hook"], lines
    rows = []
    for line in body:
        cells = line.split("\t")
        cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [c.strip() for c in cells]))
        r["vistas"] = numero(r.get("vistas"))
        for k in ("seguidores", "mediana", "largo"):
            r[k] = numero(r.get(k)) if r.get(k) else None
        if r["vistas"] and r.get("hook"):
            rows.append(r)
    return rows


def analyse(rows, formulas):
    used_median = any(r.get("mediana") for r in rows)
    for r in rows:
        base = r.get("mediana") or r.get("seguidores") or 0
        r["base"] = base
        r["tipo_base"] = "mediana" if r.get("mediana") else ("seguidores" if r.get("seguidores") else "-")
        r["multiplo"] = round(r["vistas"] / base, 2) if base else None
        r["formula_id"], r["formula"] = classify(r["hook"], formulas)
        r["palabras"] = len(WORD_RE.findall(r["hook"]))
        if score_hook:
            _, overall, verdict, _ = score_hook(r["hook"])
            r["hook_score"], r["hook_verdict"] = round(overall, 1), verdict
        else:
            r["hook_score"], r["hook_verdict"] = None, None
    ranked = sorted(rows, key=lambda r: -(r["multiplo"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    def cuenta(items, key):
        c = {}
        for r in items:
            v = r.get(key) or "-"
            c[v] = c.get(v, 0) + 1
        return sorted(c.items(), key=lambda kv: -kv[1])

    return {
        "base": ("mediana de la cuenta" if all(r.get("mediana") for r in rows) else
                 "mezclada (ver *)" if used_median else "seguidores (más flojo: conseguí la mediana)"),
        "n": len(ranked), "cuentas": len({r.get("cuenta", "") for r in ranked}), "reels": ranked,
        "formulas_arriba": cuenta(top, "formula"), "formulas_abajo": cuenta(bottom, "formula"),
        "formatos_arriba": cuenta(top, "formato") if any(r.get("formato") for r in rows) else [],
        "hook_arriba": med(top, "hook_score"), "hook_abajo": med(bottom, "hook_score"),
        "palabras_arriba": med(top, "palabras"), "palabras_abajo": med(bottom, "palabras"),
        "largo_arriba": med(top, "largo"), "largo_abajo": med(bottom, "largo"),
        "sin_clasificar": [r["hook"] for r in ranked if r["formula"] == "sin clasificar"],
        "outliers": sum(1 for r in ranked if (r["multiplo"] or 0) >= 3),
    }


def miles(n):
    return f"{n:,}".replace(",", ".")


def render(a, out=sys.stdout):
    head = f"REFERENTES  ·  {a['n']} reels  ·  {a['cuentas']} cuentas  ·  base: {a['base']}"
    print("\n" + head, file=out)
    print("=" * max(len(head), 78), file=out)
    for r in a["reels"]:
        mult = (f"{r['multiplo']:.1f}x" + ("*" if r["tipo_base"] == "seguidores" else "")) if r["multiplo"] else "   ?"
        score = f"{r['hook_score']:.0f}" if r["hook_score"] is not None else " -"
        fid = f"#{r['formula_id']:<2}" if r["formula_id"] else "-  "
        print(f"  {mult:>7}  hook {score:>3}  {fid} {r['formula'][:22]:<22} "
              f"{(r.get('cuenta') or '')[:16]:<16} {miles(r['vistas']):>10}", file=out)
        print(f"           \"{r['hook'][:96]}\"", file=out)
    print("-" * max(len(head), 78), file=out)
    if any(r["tipo_base"] == "seguidores" for r in a["reels"]):
        print("  * múltiplo contra seguidores, no contra la mediana: no es comparable con los demás. "
              "Conseguí la mediana de esa cuenta.", file=out)
    print("QUÉ ESTÁ FUNCIONANDO EN ESTA TANDA", file=out)
    print(f"  outliers (3x o más):    {a['outliers']} de {a['n']}", file=out)
    if a["formulas_arriba"]:
        print("  tercio de arriba:       " + ", ".join(f"{n} x{c}" for n, c in a["formulas_arriba"][:4]), file=out)
        print("  tercio de abajo:        " + ", ".join(f"{n} x{c}" for n, c in a["formulas_abajo"][:4]), file=out)
    if a["formatos_arriba"]:
        print("  formatos arriba:        " + ", ".join(f"{n} x{c}" for n, c in a["formatos_arriba"][:4]), file=out)
    if a["hook_arriba"] is not None:
        print(f"  puntaje de hook (med.): arriba {a['hook_arriba']:.0f}  vs  abajo {a['hook_abajo']:.0f}", file=out)
    print(f"  largo del hook (med.):  arriba {a['palabras_arriba']} palabras  vs  abajo {a['palabras_abajo']}", file=out)
    if a["largo_arriba"] is not None:
        print(f"  largo del reel (med.):  arriba {a['largo_arriba']}s  vs  abajo {a['largo_abajo']}s", file=out)
    print(f"  sin clasificar:         {len(a['sin_clasificar'])} de {a['n']}. Leelos a mano: ahí se esconde "
          "la fórmula que todavía no tenés.", file=out)
    print("\n  Una tanda juntada a mano es evidencia, no prueba. Doce reels no muestran nada;\n"
          "  cuarenta en seis cuentas muestran algo. Juntá más antes de creerle.\n", file=out)


def to_markdown(a):
    lines = ["# Referentes", "", f"{a['n']} reels en {a['cuentas']} cuentas. Ordenados por múltiplo sobre {a['base']}.", ""]
    for r in a["reels"]:
        mult = f"{r['multiplo']:.1f}x" if r["multiplo"] else "?"
        lines += [f"## {mult}  {r['formula']}  ({r.get('cuenta', '')})",
                  f"- vistas: {miles(r['vistas'])}  base: {miles(r['base'])}",
                  f"- puntaje de hook: {r['hook_score']}  palabras: {r['palabras']}",
                  f"- hook: \"{r['hook']}\"", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Rankea reels juntados a mano por múltiplo sobre su cuenta.")
    ap.add_argument("input", nargs="?", default="-", help="archivo TSV, o - para stdin")
    ap.add_argument("--hooks", default=buscar("hooks.json"), help="ruta a hooks.json")
    ap.add_argument("--md", help="escribir también el archivo de referentes en markdown")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("no hay filas útiles. Hace falta un TSV con al menos vistas y hook.", file=sys.stderr)
        sys.exit(2)
    formulas = load_formulas(args.hooks) if args.hooks else None
    a = analyse(rows, formulas)
    if not formulas:
        print("aviso: no encontré hooks.json, las fórmulas no tienen nombre. Pasá --hooks.", file=sys.stderr)
    if score_hook is None:
        print("aviso: no pude importar hookscore.py, sin puntaje de hooks.", file=sys.stderr)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    if args.md:
        open(os.path.expanduser(args.md), "w", encoding="utf-8").write(to_markdown(a))
        print(f"escrito: {args.md}", file=sys.stderr)


if __name__ == "__main__":
    main()
