#!/usr/bin/env python3
"""Arte provisoria das cartas do FM 2: degrade de uma cor, um disco claro no meio
e uma fileira de pontos com o tier da carta (1 a 5). PNG em Python puro (sem PIL).
Rodar da raiz do repo:  python tools/fm2/gen_art.py
"""
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "mods" / "fm2-cards" / "images"
W, H = 408, 384  # 4x o tamanho de 102x96 (a arte HD do jogo)

# id -> (cor de cima, cor de baixo, tier)
ART = {
    "pebble-raptor":        ((176, 132, 84), (84, 56, 34), 1),
    "spark-beetle":         ((255, 214, 70), (176, 96, 20), 1),
    "ash-sparrow":          ((200, 190, 180), (96, 70, 60), 1),
    "ember-kindler":        ((236, 92, 168), (112, 24, 90), 2),
    "ashfeather-hawk":      ((255, 150, 60), (150, 54, 20), 2),
    "magma-raptor":         ((226, 72, 40), (100, 24, 16), 2),
    "blazing-wyvern":       ((240, 40, 40), (90, 10, 24), 3),
    "obsidian-colossus":    ((120, 90, 170), (20, 14, 40), 3),
    "caldera-drake":        ((210, 20, 60), (60, 0, 20), 4),
    "solar-phoenix-dragon": ((255, 232, 120), (230, 100, 10), 5),
}


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def render(top, bottom, tier):
    cx, cy, radius = W // 2, int(H * 0.45), int(H * 0.28)
    light = lerp(top, (255, 255, 255), 0.45)
    dot_r, gap = 14, 44
    dots = [(cx + (i - (tier - 1) / 2) * gap, int(H * 0.88)) for i in range(tier)]
    rows = []
    for y in range(H):
        base = lerp(top, bottom, y / (H - 1))
        row = bytearray([0])  # filtro PNG "none"
        for x in range(W):
            px = base
            if (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2:
                px = light
            for dx, dy in dots:
                if (x - dx) ** 2 + (y - dy) ** 2 <= dot_r ** 2:
                    px = (255, 255, 255)
            row += bytes(px)
        rows.append(bytes(row))
    return b"".join(rows)


def png(data):
    def chunk(tag, body):
        return struct.pack(">I", len(body)) + tag + body + struct.pack(">I", zlib.crc32(tag + body))

    header = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(data, 9)) + chunk(b"IEND", b"")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (top, bottom, tier) in ART.items():
        (OUT / f"{name}.png").write_bytes(png(render(top, bottom, tier)))
    print(f"{len(ART)} images -> {OUT}")


if __name__ == "__main__":
    main()
