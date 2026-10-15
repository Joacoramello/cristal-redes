#!/usr/bin/env python3
"""
auditoria.py - post mortem de lo publicado por Química Cristal.

Lee las publicaciones del tablero (los JSON que deja ArtifactData con
`out_dir`, una carpeta con un archivo por publicación, o un único archivo con
una lista) y calcula lo que importa en vez de las vistas solas:

  múltiplo            vistas / mediana de vistas de la cuenta en el período
  no seguidores       % del alcance que no seguía la cuenta (¿viajó?)
  retención 3 s       % que pasó los 3 segundos (la nota del hook)
  envíos / alcance    compartidos cada 1.000 cuentas alcanzadas
  guardados / alcance guardados cada 1.000
  seguidores / alcance
  conversaciones      mensajes de WhatsApp con el mensaje precargado del posteo
  ventas              pedidos atribuibles en Odoo

Y agrupa por fórmula de hook, formato, segmento, pilar y largo, separando el
tercio de arriba del de abajo. Marca los candidatos a anuncio (múltiplo 3x o
más con al menos una conversación) para pasarle a meta-ads-cristal.

No inventa nada: si un campo no está cargado, la cuenta no se hace y se dice.

Uso
  python3 auditoria.py carpeta_publicaciones/
  python3 auditoria.py publicaciones.json --desde 2026-09-01 --hasta 2026-10-31
  python3 auditoria.py carpeta/ --json
"""

import argparse
import glob
import json
import os
import re
import statistics
import sys


def cargar(ruta):
    filas = []
    if os.path.isdir(ruta):
        for p in sorted(glob.glob(os.path.join(ruta, "**", "*.json"), recursive=True)):
            d = json.load(open(p, encoding="utf-8"))
            d = d.get("data", d) if isinstance(d, dict) else d
            if isinstance(d, dict):
                d.setdefault("id", os.path.splitext(os.path.basename(p))[0])
                filas.append(d)
    else:
        d = json.load(open(ruta, encoding="utf-8"))
        for x in (d if isinstance(d, list) else d.get("documents", d.get("publicaciones", []))):
            filas.append(x.get("data", x) | {"id": x.get("id", x.get("data", {}).get("id", ""))}
                         if isinstance(x, dict) and "data" in x else x)
    return filas


def a_numero(v):
    """Lee números como los muestra Insights en Argentina: 6.100, 1,2 mil, 18k, 45 %."""
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    t = str(v).strip().lower().replace("%", "").replace(" ", "")
    mult = 1
    for suf, m in (("mill", 1_000_000), ("m", 1_000_000), ("mil", 1000), ("k", 1000)):
        if t.endswith(suf):
            t, mult = t[: -len(suf)], m
            break
    if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", t):      # 6.100 / 1.234,5
        t = t.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d+,\d+", t):                    # 1,2 / 45,5
        t = t.replace(",", ".")
    try:
        return float(t) * mult
    except ValueError:
        return None


def num(m, k):
    return a_numero((m or {}).get(k))


def por_mil(a, b):
    return round(a * 1000 / b, 1) if a is not None and b else None


def med(xs):
    v = [x for x in xs if x is not None]
    return round(statistics.median(v), 1) if v else None


def grupo_largo(seg):
    if seg is None:
        return "sin dato"
    return "<15 s" if seg < 15 else "15-30 s" if seg <= 30 else "30-60 s" if seg <= 60 else ">60 s"


def analizar(filas, desde=None, hasta=None):
    pubs = [f for f in filas if f.get("estado") == "publicado"
            and (not desde or str(f.get("fecha", "")) >= desde)
            and (not hasta or str(f.get("fecha", "")) <= hasta)]
    con_vistas = [p for p in pubs if num(p.get("metricas"), "vistas")]
    base = med([num(p["metricas"], "vistas") for p in con_vistas])
    for p in pubs:
        m = p.get("metricas") or {}
        v, alc = num(m, "vistas"), num(m, "alcance")
        p["_mult"] = round(v / base, 2) if v and base else None
        p["_envios"] = por_mil(num(m, "compartidos"), alc)
        p["_guard"] = por_mil(num(m, "guardados"), alc)
        p["_seg"] = por_mil(num(m, "seguidores"), alc)
        p["_conv"] = num(m, "conversaciones")
        p["_ventas"] = num(m, "ventas")
        p["_ventas_est"] = num(m, "ventas_estimadas")
        p["_tprom"] = num(m, "tiempo_promedio_s")
        p["_ret"] = num(m, "retencion_3s_pct")
        p["_nos"] = num(m, "no_seguidores_pct")
        p["_largo"] = grupo_largo(a_numero(p.get("largo_s")) or num(m, "largo_s"))
        p["_formula"] = (f"#{p['formula_id']} {p.get('formula') or ''}".strip()
                         if p.get("formula_id") not in (None, "") else (p.get("formula") or None))
    rank = sorted([p for p in pubs if p["_mult"] is not None], key=lambda p: -p["_mult"])
    tercio = max(1, len(rank) // 3)
    arriba, abajo = rank[:tercio], rank[-tercio:] if len(rank) > 1 else []

    def resumen(items):
        return {"n": len(items), "multiplo": med([i["_mult"] for i in items]),
                "retencion_3s": med([i["_ret"] for i in items]),
                "tiempo_promedio_s": med([i["_tprom"] for i in items]),
                "no_seguidores": med([i["_nos"] for i in items]),
                "envios_x1000": med([i["_envios"] for i in items]),
                "conversaciones": sum(i["_conv"] or 0 for i in items)}

    def agrupar(clave):
        g = {}
        for p in rank:
            g.setdefault(str(p.get(clave) or "sin dato"), []).append(p)
        return sorted(({"valor": k, "n": len(v), "multiplo": med([x["_mult"] for x in v]),
                        "conversaciones": sum(x["_conv"] or 0 for x in v)} for k, v in g.items()),
                      key=lambda r: -(r["multiplo"] or 0))

    faltan = [p.get("id") or p.get("hook", "")[:40] for p in pubs if not num(p.get("metricas"), "vistas")]
    candidatos = [p for p in rank if p["_mult"] >= 3 and (p["_conv"] or 0) >= 1]
    vistas_sin_seguir = [p for p in rank if p["_mult"] >= 2 and (p["_nos"] or 0) >= 50 and p["_seg"] is not None and p["_seg"] < 2]
    return {
        "periodo": {"desde": desde, "hasta": hasta}, "publicados": len(pubs), "con_metricas": len(rank),
        "mediana_vistas": base, "ranking": rank, "arriba": resumen(arriba), "abajo": resumen(abajo),
        "por_formula": agrupar("_formula"), "por_formato": agrupar("formato"),
        "por_segmento": agrupar("segmento"), "por_pilar": agrupar("pilar"), "por_largo": agrupar("_largo"),
        "sin_metricas": faltan, "candidatos_a_anuncio": candidatos,
        "problema_de_perfil": vistas_sin_seguir,
        "conversaciones_total": sum(p["_conv"] or 0 for p in rank),
        "ventas_total": sum(p["_ventas"] or 0 for p in rank),
        "ventas_estimadas_total": sum(p["_ventas_est"] or 0 for p in rank),
    }


def fmt(x, suf=""):
    return "–" if x is None else f"{x:g}{suf}".replace(".", ",")


def render(a, out=sys.stdout):
    p = a["periodo"]
    head = (f"AUDITORÍA  ·  {a['con_metricas']} de {a['publicados']} publicados con métricas  ·  "
            f"mediana {fmt(a['mediana_vistas'])} vistas" + (f"  ·  {p['desde'] or '…'} a {p['hasta'] or '…'}" if p["desde"] or p["hasta"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 78), file=out)
    if not a["ranking"]:
        print("  No hay publicaciones con vistas cargadas. Primero hay que cargar métricas.\n", file=out)
        return
    print("  mult.  ret3s  t.prom  no seg.  env/1000  WhatsApp  ventas  fórmula / hook", file=out)
    for r in a["ranking"]:
        print(f"  {fmt(r['_mult'], 'x'):>6} {fmt(r['_ret'], '%'):>6} {fmt(r['_tprom'], 's'):>7} {fmt(r['_nos'], '%'):>8} "
              f"{fmt(r['_envios']):>9} {fmt(r['_conv']):>9} {fmt(r['_ventas']):>7}  {r.get('formato', '')} · {r['_formula'] or 'sin fórmula'}", file=out)
        print(f"  {'':>58}\"{str(r.get('hook', ''))[:70]}\"", file=out)
    print("-" * 78, file=out)
    ar, ab = a["arriba"], a["abajo"]
    print(f"  TERCIO DE ARRIBA (n={ar['n']}): múltiplo {fmt(ar['multiplo'], 'x')}, retención 3 s {fmt(ar['retencion_3s'], '%')}, "
          f"tiempo promedio {fmt(ar['tiempo_promedio_s'], ' s')}, "
          f"no seguidores {fmt(ar['no_seguidores'], '%')}, {fmt(ar['conversaciones'])} conversaciones", file=out)
    print(f"  TERCIO DE ABAJO  (n={ab['n']}): múltiplo {fmt(ab['multiplo'], 'x')}, retención 3 s {fmt(ab['retencion_3s'], '%')}, "
          f"tiempo promedio {fmt(ab['tiempo_promedio_s'], ' s')}, "
          f"no seguidores {fmt(ab['no_seguidores'], '%')}, {fmt(ab['conversaciones'])} conversaciones", file=out)
    for titulo, clave in (("POR FÓRMULA", "por_formula"), ("POR FORMATO", "por_formato"),
                          ("POR SEGMENTO", "por_segmento"), ("POR PILAR", "por_pilar"), ("POR LARGO", "por_largo")):
        filas = a[clave]
        if len(filas) > 1:
            print(f"\n  {titulo}", file=out)
            for g in filas:
                print(f"    {g['valor'][:34]:<34} n={g['n']:<3} múltiplo mediano {fmt(g['multiplo'], 'x'):>6}  "
                      f"WhatsApp {fmt(g['conversaciones'])}", file=out)
    if a["candidatos_a_anuncio"]:
        print("\n  CANDIDATOS A ANUNCIO (3x o más y al menos una conversación) -> meta-ads-cristal", file=out)
        for r in a["candidatos_a_anuncio"]:
            print(f"    {fmt(r['_mult'], 'x')}  \"{str(r.get('hook', ''))[:70]}\"", file=out)
    if a["problema_de_perfil"]:
        print("\n  VIAJARON PERO NO CONVIRTIERON (muchas vistas de no seguidores, casi nadie siguió):", file=out)
        print("    eso es un problema de perfil, no de hook -> cristal-perfil", file=out)
    if a["ventas_estimadas_total"]:
        print(f"\n  Ventas estimadas (sin marca de origen en Odoo): {fmt(a['ventas_estimadas_total'])}. "
              "No cuentan para decidir pauta.", file=out)
    if a["sin_metricas"]:
        print(f"\n  SIN MÉTRICAS ({len(a['sin_metricas'])}): {', '.join(map(str, a['sin_metricas'][:6]))}", file=out)
    n = a["con_metricas"]
    conf = "baja: con menos de 10 posteos no hay patrón, hay anécdotas" if n < 10 else (
        "media: alcanza para ver tendencias grandes" if n < 25 else "razonable")
    print(f"\n  Confianza: {conf} (n={n}).\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Post mortem de las publicaciones de Química Cristal.")
    ap.add_argument("entrada", help="carpeta con los JSON del tablero, o un JSON con la lista")
    ap.add_argument("--desde")
    ap.add_argument("--hasta")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    a = analizar(cargar(args.entrada), args.desde, args.hasta)
    if args.json:
        limpio = json.loads(json.dumps(a, default=str))
        print(json.dumps(limpio, indent=2, ensure_ascii=False))
    else:
        render(a)


if __name__ == "__main__":
    main()
