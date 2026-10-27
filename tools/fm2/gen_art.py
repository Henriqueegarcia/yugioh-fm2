#!/usr/bin/env python3
"""Arte das cartas do FM 2: icone de game-icons.net (CC BY 3.0, ver docs/CREDITS-arte.md) pintado
com as cores da carta, sobre fundo em degrade com brilho no centro. Precisa de Pillow
(pip install pillow). Os icones baixados ficam em cache em tmp/art/icons (fora do git).
Rodar da raiz do repo:  python tools/fm2/gen_art.py
"""
import urllib.request
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageOps

from gen_cards import CARDS
from icon_map import ICONS

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "mods" / "fm2-cards" / "images"
CACHE = ROOT / "tmp" / "art" / "icons"
W, H = 408, 384  # 4x o tamanho de 102x96 (a arte HD do jogo)


def icon_mask(path):
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / (path.replace("/", "__") + ".png")
    if not f.exists():
        url = f"https://game-icons.net/icons/ffffff/000000/1x1/{path}.png"
        req = urllib.request.Request(url, headers={"User-Agent": "fm2-art/1.0"})
        f.write_bytes(urllib.request.urlopen(req, timeout=30).read())
    return Image.open(f).convert("L")  # branco = desenho


def gradient(top, bottom):
    col = Image.new("RGB", (1, H))
    for y in range(H):
        t = y / (H - 1)
        col.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return col.resize((W, H))


def render(card):
    top, bottom = card["colors"]
    img = gradient(top, bottom)
    # brilho radial no centro
    glow = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(glow)
    cx, cy, r = W // 2, int(H * 0.5), int(H * 0.42)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=170)
    glow = glow.filter(ImageFilter.GaussianBlur(52))
    light = tuple(min(255, int(c * 0.5 + 255 * 0.5)) for c in top)
    img = Image.composite(Image.new("RGB", (W, H), light), img, glow.point(lambda v: int(v * 0.75)))
    # icone: contorno escuro, sombra e preenchimento claro com degrade
    size = int(H * 0.80)
    mask = ImageOps.autocontrast(icon_mask(ICONS[card["id"]])).resize((size, size), Image.LANCZOS)
    layer = Image.new("L", (W, H), 0)
    ox, oy = (W - size) // 2, (H - size) // 2 - 4
    layer.paste(mask, (ox, oy))
    outline = layer.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(1.5))
    shadow = ImageChops.offset(outline, 8, 10).filter(ImageFilter.GaussianBlur(7))
    img = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), img, shadow.point(lambda v: int(v * 0.55)))
    img = Image.composite(Image.new("RGB", (W, H), tuple(int(c * 0.18) for c in bottom)), img, outline)
    fill = ImageChops.multiply(gradient((255, 255, 255), tuple(min(255, c + 90) for c in top)), Image.new("RGB", (W, H), (255, 255, 255)))
    img = Image.composite(fill, img, layer)
    # moldura fina
    ImageDraw.Draw(img).rectangle((0, 0, W - 1, H - 1), outline=tuple(int(c * 0.35) for c in bottom), width=6)
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for c in CARDS:
        render(c).save(OUT / f"{c['id']}.png", optimize=True)
    print(f"{len(CARDS)} images -> {OUT}")


if __name__ == "__main__":
    main()
