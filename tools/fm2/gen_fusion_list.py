#!/usr/bin/env python3
"""Gera docs/fm2-fusoes.md: lista de todas as fusoes das cartas do FM 2, por bloco.
Rodar da raiz do repo:  python tools/fm2/gen_fusion_list.py
"""
import collections
from pathlib import Path

import gen_cards as g

OUT = g.ROOT / "docs" / "fm2-fusoes.md"
cat, _ = g.load_retail()
by_id = {c["id"]: c for c in g.CARDS}


def name(x):
    return cat[x]["name"] + " (original)" if isinstance(x, int) else by_id[x]["name"]


def stats(x):
    if isinstance(x, int):
        return cat[x]["attack"], cat[x]["defense"]
    return by_id[x]["attack"], by_id[x]["defense"]


recipe_of = {r: (a, b) for a, b, r in g.RECIPES}


def base_cards(x):
    """Cartas 'cruas' (sem receita) necessarias para montar x, contando copias."""
    if x not in recipe_of:
        return collections.Counter({x: 1})
    a, b = recipe_of[x]
    return base_cards(a) + base_cards(b)


lines = ["# FM 2 - Lista de fusões", "",
         "Gerado por `tools/fm2/gen_fusion_list.py` (não edite à mão). "
         "Cartas marcadas com *(original)* são do jogo base. "
         "\"Cartas cruas\" = quantas cartas sem receita você precisa no baralho para montar tudo do zero.", ""]
for blk in g.BLOCKS:
    lines += [f"## Bloco {blk.NAME}", "",
              "| Receita | Resultado | ATK/DEF | Tier | Cartas cruas |", "|---|---|---|---|---|"]
    for a, b, r in blk.RECIPES:
        atk, df = stats(r)
        raw = base_cards(r)
        raw_txt = ", ".join(f"{n}x {name(k)}" for k, n in raw.items())
        lines.append(f"| {name(a)} + {name(b)} | **{name(r)}** | {atk}/{df} | T{by_id[r]['tier']} | "
                     f"{sum(raw.values())}: {raw_txt} |")
    fused = {r for _, _, r in blk.RECIPES}
    plain = [c["name"] for c in blk.CARDS if c["id"] not in fused]
    lines += ["", "Sem receita (só drop/baralho): " + ", ".join(plain), ""]
lines += ["## Observação", "",
          "Duas fusões não se juntam no campo: se uma receita usa um resultado intermediário, "
          "esse intermediário precisa estar na mão como carta real (e portanto cair de algum duelista).", ""]
OUT.write_text("\n".join(lines), encoding="utf-8")
print("->", OUT)
