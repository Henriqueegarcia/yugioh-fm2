#!/usr/bin/env python3
"""Gera mods/fm2-cards/mod.json (cartas do FM 2, lote 1: linha Ember).

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


RETAIL_SUNBIRD = 467  # Crimson Sunbird (Winged Beast, Fire, 2300/1800)

CARDS = [
    # ---- T1: so no baralho/drop, sem receita para fazer ----
    dict(id="pebble-raptor", tier=1, copy=105, name="Pebble Raptor", type="Dinosaur", attribute="Earth",
         level=2, stars=["Saturn", "Moon"], attack=700, defense=500,
         description="A small raptor that\nnests in warm ash\nand cracked stone."),
    dict(id="spark-beetle", tier=1, copy=53, name="Spark Beetle", type="Insect", attribute="Fire",
         level=2, stars=["Mars", "Mercury"], attack=600, defense=500,
         description="Its wings leave a\ntrail of sparks. It\nis the seed of the\nEmber line."),
    dict(id="ash-sparrow", tier=1, copy=207, name="Ash Sparrow", type="Winged Beast", attribute="Fire",
         level=2, stars=["Mars", "Sun"], attack=700, defense=400,
         description="Born from the embers\nof a dead volcano."),
    # ---- T2 ----
    dict(id="ember-kindler", tier=2, copy=106, name="Ember Kindler", type="Spellcaster", attribute="Fire",
         level=3, stars=["Sun", "Mars"], attack=900, defense=900,
         description="{f8 0A 05}<Aura>{f8 0A 00} Your other\nFIRE monsters get\n+200 ATK.\nFusion: Ash Sparrow\n+ Pebble Raptor",
         monster_effects=[{"when": "face_up", "do": "boost", "target": "others",
                          "attribute": "Fire", "attack": 200}]),
    dict(id="ashfeather-hawk", tier=2, copy=581, name="Ashfeather Hawk", type="Winged Beast", attribute="Fire",
         level=4, stars=["Mars", "Sun"], attack=1400, defense=1000,
         description="Fusion: Ash Sparrow\n+ Spark Beetle"),
    dict(id="magma-raptor", tier=2, copy=80, name="Magma Raptor", type="Dinosaur", attribute="Fire",
         level=4, stars=["Mars", "Saturn"], attack=1500, defense=900,
         description="Fusion: Pebble Raptor\n+ Spark Beetle"),
    # ---- T3 ----
    dict(id="blazing-wyvern", tier=3, copy=383, name="Blazing Wyvern", type="Dragon", attribute="Fire",
         level=6, stars=["Mars", "Jupiter"], attack=1900, defense=1500,
         description="Fusion: Ashfeather\nHawk + Magma Raptor"),
    dict(id="obsidian-colossus", tier=3, copy=531, name="Obsidian Colossus", type="Rock", attribute="Earth",
         level=6, stars=["Saturn", "Mars"], attack=1800, defense=2300,
         description="Fusion: Magma\nRaptor + Ember\nKindler"),
    # ---- T4 ----
    dict(id="caldera-drake", tier=4, copy=571, name="Caldera Drake", type="Dragon", attribute="Fire",
         level=7, stars=["Mars", "Uranus"], attack=2400, defense=1900,
         description="{f8 0A 05}<Destroyed>{f8 0A 00} Deals 600\ndamage to the opponent.\nFusion: Blazing\nWyvern + Obsidian\nColossus",
         monster_effects=[{"when": "destroyed", "do": "damage", "amount": 600}]),
    # ---- T5: chefe das fusoes, precisa de uma carta original rara ----
    dict(id="solar-phoenix-dragon", tier=5, copy=713, name="Solar Phoenix Dragon", type="Dragon",
         attribute="Fire", level=8, stars=["Sun", "Mars"], attack=2900, defense=2300,
         description="{f8 0A 05}<Aura>{f8 0A 00} Your other\nFIRE monsters get\n+300 ATK and DEF.\n{f8 0A 05}<Destroyed>{f8 0A 00} Deals\n800 damage.\nFusion: Caldera Drake\n+ Crimson Sunbird",
         monster_effects=[
             {"when": "face_up", "do": "boost", "target": "others", "attribute": "Fire",
              "attack": 300, "defense": 300},
             {"when": "destroyed", "do": "damage", "amount": 800}]),
]

# receitas entre as cartas novas (e com a unica carta original exigida)
RECIPES = [
    ("ash-sparrow", "pebble-raptor", "ember-kindler"),
    ("ash-sparrow", "spark-beetle", "ashfeather-hawk"),
    ("pebble-raptor", "spark-beetle", "magma-raptor"),
    ("ashfeather-hawk", "magma-raptor", "blazing-wyvern"),
    ("magma-raptor", "ember-kindler", "obsidian-colossus"),
    ("blazing-wyvern", "obsidian-colossus", "caldera-drake"),
    ("caldera-drake", RETAIL_SUNBIRD, "solar-phoenix-dragon"),
]


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
        "description": "FM 2 cards, batch 1: the Ember line. Ten new fire cards built to be fused "
                       "(Ash Sparrow + Spark Beetle -> Ashfeather Hawk -> ... -> Solar Phoenix Dragon). "
                       "Artwork is the base card's until the final art is made.",
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
