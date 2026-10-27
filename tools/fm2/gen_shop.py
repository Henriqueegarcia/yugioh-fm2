#!/usr/bin/env python3
"""Gera mods/fm2-shop/mod.json: os booster packs do FM 2 e a economia de StarChips.
Rodar da raiz do repo:  python tools/fm2/gen_shop.py

Economia (palpite a calibrar jogando): uma vitoria rende 2 a 10 starchips (rank D a S),
em media ~5. Seeds ~5 vitorias, Forge ~18, Hybrid Crate ~30, Legend Chest ~80.
"""
import json

import gen_cards
from gen_cards import ROOT

MOD = ROOT / "mods" / "fm2-shop"

# True: cada pack so abre depois de vencer o NPC da linha. False: tudo aberto (teste).
USE_GATES = False

STARCHIP_PRIZE = {"S": 10, "A": 8, "B": 5, "C": 3, "D": 2}

OWNER = {c["id"]: blk.NAME for blk in gen_cards.BLOCKS for c in blk.CARDS}
TIER = {c["id"]: c["tier"] for c in gen_cards.CARDS}
NAME = {c["id"]: c["name"] for c in gen_cards.CARDS}


def pool(blocks, tiers):
    return {f"fm2-cards:{i}:1": 1 for i in OWNER if OWNER[i] in blocks and TIER[i] in tiers}


def unlock(**conds):
    return conds if USE_GATES else None


LINES = [
    # id do bloco, NPC da linha, carta de capa do Forge (T4 da linha), cor do texto nao importa
    ("Ember", "kael", "caldera-drake", "fogo"),
    ("Tide", "marin", "tidal-leviathan", "agua"),
    ("Grove", "brenn", "emperor-scarab", "planta"),
    ("Crypt", "morrow", "wraith-king", "mortos-vivos"),
]

packs = []
for block, npc, cover, theme in LINES:
    t1, t2, t3, t4 = (pool([block], [t]) for t in (1, 2, 3, 4))
    packs.append({
        "id": f"{block.lower()}-seeds", "name": f"{block} Seeds",
        "description": f"5 cards of the {block}\nline: mostly basic.",
        "price": 25, "count": 5,
        "tiers": {"common": {"odds": 850, "cards": t1},
                  "uncommon": {"odds": 150, "label": "UNCOMMON", "color": 1, "cards": t2}},
        "max_copies": 3, "duplicates": "allow",
        "cover": f"fm2-cards:{[i for i in OWNER if OWNER[i] == block and TIER[i] == 1][0]}:1",
    })
    forge = {
        "id": f"{block.lower()}-forge", "name": f"{block} Forge",
        "description": f"4 cards of the {block}\nline: fusion fuel.",
        "price": 90, "count": 4,
        "tiers": {"common": {"odds": 800, "cards": t2},
                  "rare": {"odds": 190, "label": "RARE!", "color": 2, "cards": t3},
                  "epic": {"odds": 10, "label": "EPIC!!", "color": 1, "cards": t4, "reveal": "flip"}},
        "pity": {"rare": 6},
        "max_copies": 3, "cover": f"fm2-cards:{cover}:1",
    }
    u = unlock(beat=f"fm2-duelists:{npc}")
    if u:
        forge["unlock"] = u
        forge["locked"] = "shown"
    packs.append(forge)

t3_hyb = pool(["Ember", "Tide", "Grove", "Crypt", "Hibridas"], [3])
packs.append({
    "id": "hybrid-crate", "name": "Hybrid Crate",
    "description": "3 cards, tier 3: all\nlines and hybrids.",
    "price": 150, "count": 3,
    "tiers": {"common": {"odds": 900, "cards": t3_hyb},
              "rare": {"odds": 100, "label": "RARE!", "color": 2,
                       "cards": pool(["Hibridas"], [4])}},
    "pity": {"rare": 8}, "max_copies": 3,
    "cover": "fm2-cards:bone-dragon-overlord:1",
    **({"unlock": unlock(beat="fm2-duelists:coral"), "locked": "shown"} if USE_GATES else {}),
})
packs.append({
    "id": "legend-chest", "name": "Legend Chest",
    "description": "2 cards, tier 4. Five\nchests a save.",
    "price": 400, "count": 2,
    "cards": pool(["Ember", "Tide", "Grove", "Crypt", "Hibridas"], [4]),
    "stock": 5, "max_copies": 3, "duplicates": "unique_in_pack",
    "label": "LEGEND!",
    "cover": "fm2-cards:mangrove-leviathan:1",
    **({"unlock": unlock(beat="fm2-duelists:orin", packs_opened=10), "locked": "shown"} if USE_GATES else {}),
})
# `label` is not a pack key; the single pool has no tiers, so drop it
packs[-1].pop("label")

# Compra por senha na tela de Password: senha 000007NN (NN = ordem da carta no mod, comeca em 723).
# As T5 ficam sem senha: so existem por fusao.
PRICE = {1: 30, 2: 120, 3: 400, 4: 1500}
passwords = {}
for n, c in enumerate(gen_cards.CARDS):
    if c["tier"] <= 4:
        passwords[f"fm2-cards:{c['id']}:1"] = {"password": f"{723 + n:08d}", "starchips": PRICE[c["tier"]]}
    else:
        passwords[f"fm2-cards:{c['id']}:1"] = {"password": ""}

mod = {
    "id": "fm2-shop",
    "name": "FM 2 Shop",
    "version": "0.1",
    "author": "FM 2",
    "description": "Booster packs for the FM 2 card lines, sold on the Password screen behind the triangle button, "
                   "and a better StarChip prize for each win.",
    "enabled": True,
    "min_api": 16,
    "game": "slus_01411",
    "limits": {"starchip_prize": STARCHIP_PRIZE},
    "passwords": passwords,
    "packs": packs,
    "pack_shop": {"password": "both", "when_nothing_left": "refuse"},
}
MOD.mkdir(parents=True, exist_ok=True)
(MOD / "mod.json").write_text(json.dumps(mod, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(len(packs), "packs,", len(passwords), "passwords ->", MOD)
for p in packs:
    print(f"  {p['name']:14} {p['price']:>4} starchips x{p['count']}")
