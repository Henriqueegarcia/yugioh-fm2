#!/usr/bin/env python3
"""Gera mods/fm2-cards/mod.json (cartas do FM 2: blocos Ember, Tide, Grove, Crypt, hibridas e T5; dados em block_*.py).

Uma carta nova copia uma carta original ("base") e herda as receitas de fusao
dela. Para manter o balanceamento do PLANO.md (resultado <= tier do material +1),
este script bloqueia (resultado null) toda receita herdada que passe do teto do
tier da carta. Rodar da raiz do repo:  python tools/fm2/gen_cards.py
"""
import csv
import json
import collections
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MOD_ID = "fm2-cards"

# tier -> ATK maximo da carta; o teto de resultado herdado e o do tier seguinte
TIER_ATK = {1: 1000, 2: 1500, 3: 2000, 4: 2500, 5: 3000}


def ident(card_id):
    return f"{MOD_ID}:{card_id}:1"


import block_ember
import block_tide
import block_grove
import block_crypt
import block_hybrid
import block_mix

# a ordem importa: os ids de execucao (723+) seguem a ordem das cartas
BLOCKS = [block_ember, block_tide, block_grove, block_crypt, block_hybrid, block_mix]
CARDS = [c for blk in BLOCKS for c in blk.CARDS]
RECIPES = [r for blk in BLOCKS for r in blk.RECIPES]


def ref(x):
    return x if isinstance(x, int) else ident(x)


def load_retail():
    base = ROOT / "notes"
    cat = {int(r["id"]): r for r in csv.DictReader(open(base / "card-catalog.csv", encoding="utf-8"))}
    rec = collections.defaultdict(list)
    path = base / "research" / "fusion-and-drop-tables" / "fusions.csv"
    for f in csv.DictReader(open(path, encoding="utf-8")):
        a, b, r = int(f["material_a_id"]), int(f["material_b_id"]), int(f["result_id"])
        rec[a].append((b, r))
        if a != b:
            rec[b].append((a, r))
    return cat, rec


def atk_of(cat, i):
    try:
        return int(cat[i]["attack"])
    except (KeyError, ValueError):
        return 0


def main():
    cat, rec = load_retail()
    ids = {c["id"] for c in CARDS}
    for a, b, r in RECIPES:
        for x in (a, b):
            assert isinstance(x, int) or x in ids, x
        assert r in ids, r

    cards, fusions = [], []
    for c in CARDS:
        assert c["attack"] <= TIER_ATK[c["tier"]], c["id"]
        entry = {k: c[k] for k in ("id", "copy", "name", "type", "attribute", "level", "stars",
                                    "attack", "defense", "description")}
        entry["art"] = f"images/{c['id']}.png"
        entry["tags"] = [f"tier{c['tier']}"]
        entry["drops"] = False
        if "monster_effects" in c:
            entry["monster_effects"] = c["monster_effects"]
        cards.append(entry)
        # bloqueia receitas herdadas da base acima do teto do tier seguinte
        ceiling = TIER_ATK[min(c["tier"] + 1, 5)]
        seen = set()
        for partner, result in rec.get(c["copy"], []):
            if atk_of(cat, result) > ceiling and partner not in seen:
                seen.add(partner)
                fusions.append({"with": [ident(c["id"]), partner], "result": None})
    for a, b, r in RECIPES:
        fusions.append({"with": [ref(a), ref(b)], "result": ident(r)})

    mod = {
        "id": MOD_ID,
        "name": "FM 2 Cards",
        "version": "0.1",
        "author": "FM 2",
        "description": "FM 2 cards: the Ember, Tide, Grove and Crypt lines, hybrids and T5 mixes; new cards built to be fused "
                       "from weak cards into strong ones. "
                       "Placeholder artwork (gradient + tier dots) until the final art is made.",
        "enabled": True,
        "min_api": 16,
        "game": "slus_01411",
        "cards": cards,
        "fusions": fusions,
    }
    out = ROOT / "mods" / MOD_ID / "mod.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(mod, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    nulls = sum(1 for f in fusions if f["result"] is None)
    print(f"{len(cards)} cards, {len(RECIPES)} recipes, {nulls} inherited recipes blocked -> {out}")


if __name__ == "__main__":
    main()
