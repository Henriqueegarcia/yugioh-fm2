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

from gen_cards import CARDS  # cada carta traz colors=(cor de cima, cor de baixo) e tier


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
    for c in CARDS:
        top, bottom = c["colors"]
        (OUT / f"{c['id']}.png").write_bytes(png(render(top, bottom, c["tier"])))
    print(f"{len(CARDS)} images -> {OUT}")


if __name__ == "__main__":
    main()
