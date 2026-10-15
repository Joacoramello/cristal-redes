#!/usr/bin/env python3
"""
preparar_video.py - deja un video del celular listo para Instagram y Facebook
Reels: vertical 1080x1920, H.264 + AAC, inicio rápido, y liviano (para que se
pueda subir a GitHub y que Metricool lo tome).

No corta, no edita y no le agrega nada al contenido: solo lo normaliza. Si el
video viene horizontal, lo encuadra en vertical con bandas, sin recortar.

Uso
  python3 preparar_video.py entrada.mov salida.mp4
  python3 preparar_video.py entrada.mp4 salida.mp4 --max-mb 40

Devuelve por stdout un JSON con duración, tamaño y resolución final.
"""

import argparse
import json
import os
import subprocess
import sys


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path],
        capture_output=True, text=True, check=True).stdout
    d = json.loads(out)
    v = next((s for s in d["streams"] if s.get("codec_type") == "video"), None)
    a = next((s for s in d["streams"] if s.get("codec_type") == "audio"), None)
    return {"dur": float(d["format"].get("duration", 0)), "w": v and v.get("width"),
            "h": v and v.get("height"), "audio": a is not None}


def main():
    ap = argparse.ArgumentParser(description="Normaliza un video para Reels.")
    ap.add_argument("entrada")
    ap.add_argument("salida")
    ap.add_argument("--max-mb", type=float, default=45, help="tamaño máximo de salida (default 45 MB)")
    args = ap.parse_args()

    info = probe(args.entrada)
    if info["dur"] <= 0:
        sys.exit("no pude leer la duración del video")
    if info["dur"] > 180:
        print("AVISO: dura más de 3 minutos; Instagram lo puede rechazar como reel.", file=sys.stderr)
    if info["dur"] < 3:
        print("AVISO: dura menos de 3 segundos.", file=sys.stderr)

    # Bitrate de video para no pasar el tamaño máximo (con 128 kbps de audio y margen).
    total_kbps = args.max_mb * 8 * 1024 / info["dur"] * 0.92
    v_kbps = int(max(1500, min(8000, total_kbps - 128)))

    vf = ("scale=1080:1920:force_original_aspect_ratio=decrease,"
          "pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,fps=30,format=yuv420p")
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", args.entrada, "-vf", vf,
           "-c:v", "libx264", "-preset", "medium", "-b:v", f"{v_kbps}k",
           "-maxrate", f"{int(v_kbps * 1.3)}k", "-bufsize", f"{v_kbps * 2}k",
           "-movflags", "+faststart"]
    if info["audio"]:
        cmd += ["-c:a", "aac", "-b:a", "128k", "-ar", "44100"]
    else:
        # Instagram rechaza a veces reels sin pista de audio: se agrega silencio.
        i = cmd.index(args.entrada) + 1
        cmd = cmd[:i] + ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo"] + cmd[i:]
        cmd += ["-map", "0:v:0", "-map", "1:a:0", "-c:a", "aac", "-b:a", "128k", "-shortest"]
    cmd.append(args.salida)
    subprocess.run(cmd, check=True)

    out = probe(args.salida)
    mb = os.path.getsize(args.salida) / 1024 / 1024
    print(json.dumps({"duracion_s": round(out["dur"], 1), "mb": round(mb, 1),
                      "resolucion": f"{out['w']}x{out['h']}", "bitrate_video_kbps": v_kbps}))
    if mb > 95:
        sys.exit("el archivo supera 95 MB: GitHub no lo acepta. Bajá --max-mb.")


if __name__ == "__main__":
    main()
