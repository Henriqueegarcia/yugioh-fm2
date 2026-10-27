#!/usr/bin/env python3
"""Gera mods/fm2-duelists/: os 4 NPCs intermediarios do FM 2 (um por bloco de cartas).
Cada NPC: duelo livre liberado por uma etapa da campanha, deck fixo de 40 cartas (cartas
novas do bloco + originais de apoio) e drops so do proprio bloco.
Rodar da raiz do repo:  python tools/fm2/gen_duelists.py   (precisa de Pillow)
"""
import json

import gen_art
import icon_map
from gen_cards import ROOT, load_retail

MOD = ROOT / "mods" / "fm2-duelists"
NON_MONSTER = ("Magic", "Trap", "Ritual", "Equip")


def C(card_id):
    return f"fm2-cards:{card_id}:1"


# gate = duelista da campanha cuja liberacao no Duelo Livre abre o NPC (flag 0x6E0 + n)
NPCS = [
    dict(id="kael", name="Kael", base="Villager 2", gate=7, slot=40,
         icon="delapouite/dwarf-face", colors=((255, 150, 60), (120, 30, 20)),
         deck={"ash-sparrow": 3, "pebble-raptor": 3, "spark-beetle": 3, "ember-kindler": 3,
               "ashfeather-hawk": 3, "magma-raptor": 3, "blazing-wyvern": 1},
         filler=dict(attrs=("Fire", "Earth"), atk=(600, 1300)),
         bcd={"ash-sparrow": 30, "pebble-raptor": 30, "spark-beetle": 30,
              "ember-kindler": 12, "magma-raptor": 12, "ashfeather-hawk": 8},
         pow={"ash-sparrow": 20, "pebble-raptor": 20, "spark-beetle": 20, "ember-kindler": 20,
              "magma-raptor": 20, "ashfeather-hawk": 20, "obsidian-colossus": 8, "blazing-wyvern": 8},
         tec={"ember-kindler": 20, "magma-raptor": 20, "ashfeather-hawk": 20, "obsidian-colossus": 12,
              "blazing-wyvern": 12, "caldera-drake": 4}),
    dict(id="marin", name="Marin", base="Mai Valentine", gate=11, slot=41,
         icon="delapouite/woman-elf-face", colors=((120, 200, 235), (20, 60, 130)),
         deck={"foam-sprite": 3, "reef-crab": 3, "brine-eel": 3, "tide-priestess": 3, "coral-guardian": 3,
               "razor-barracuda": 3, "deepwater-serpent": 2, "abyssal-nautilus": 1},
         filler=dict(attrs=("Water",), atk=(800, 1600)),
         bcd={"foam-sprite": 30, "reef-crab": 30, "brine-eel": 30,
              "tide-priestess": 12, "coral-guardian": 12, "razor-barracuda": 8},
         pow={"foam-sprite": 20, "reef-crab": 20, "brine-eel": 20, "tide-priestess": 20,
              "coral-guardian": 20, "razor-barracuda": 20, "deepwater-serpent": 8, "abyssal-nautilus": 8},
         tec={"tide-priestess": 20, "coral-guardian": 20, "razor-barracuda": 20, "deepwater-serpent": 12,
              "abyssal-nautilus": 12, "tidal-leviathan": 4}),
    dict(id="brenn", name="Brenn", base="Weevil Underwood", gate=17, slot=42,
         icon="delapouite/monk-face", colors=((140, 210, 110), (20, 80, 40)),
         deck={"leaf-grub": 3, "thorn-sprout": 3, "mossback-beetle": 3, "bramble-mantis": 3, "grove-warden": 3,
               "spore-shaman": 3, "hornet-duke": 2, "ancient-treant": 2, "emperor-scarab": 1},
         filler=dict(attrs=("Earth", "Wind"), types=("Plant", "Insect", "Beast", "Beast-Warrior"), atk=(900, 1700)),
         bcd={"leaf-grub": 30, "thorn-sprout": 30, "mossback-beetle": 30,
              "bramble-mantis": 12, "grove-warden": 12, "spore-shaman": 12},
         pow={"leaf-grub": 20, "thorn-sprout": 20, "mossback-beetle": 20, "bramble-mantis": 20,
              "grove-warden": 20, "spore-shaman": 20, "hornet-duke": 8, "ancient-treant": 8},
         tec={"bramble-mantis": 20, "grove-warden": 20, "spore-shaman": 20, "hornet-duke": 12,
              "ancient-treant": 12, "world-tree-guardian": 4}),
    dict(id="morrow", name="Morrow", base="High Mage Atenza", gate=23, slot=43,
         icon="darkzaitzev/hooded-figure", colors=((170, 130, 210), (30, 10, 60)),
         deck={"bone-pup": 3, "grave-wisp": 3, "rattle-squire": 3, "crypt-keeper": 3, "hollow-knight": 3,
               "wailing-banshee": 3, "revenant-lord": 2, "sepulchre-golem": 2, "wraith-king": 1,
               "bone-dragon-overlord": 1},
         filler=dict(attrs=("Dark",), types=("Zombie", "Fiend", "Spellcaster"), atk=(1000, 1800)),
         bcd={"bone-pup": 30, "grave-wisp": 30, "rattle-squire": 30,
              "crypt-keeper": 12, "hollow-knight": 12, "wailing-banshee": 12},
         pow={"bone-pup": 20, "grave-wisp": 20, "rattle-squire": 20, "crypt-keeper": 20,
              "hollow-knight": 20, "wailing-banshee": 20, "revenant-lord": 8, "sepulchre-golem": 8},
         tec={"crypt-keeper": 20, "hollow-knight": 20, "wailing-banshee": 20, "revenant-lord": 12,
              "sepulchre-golem": 12, "wraith-king": 4, "grim-harvester": 4}),
]


def fillers(cat, spec, need):
    """Escolhe cartas originais de apoio (3 copias cada) para completar o deck de 40."""
    lo, hi = spec["atk"]
    pool = []
    for r in cat.values():
        if r["type"] in NON_MONSTER or not r["attack"]:
            continue
        if r["attribute"] not in spec["attrs"] or not (lo <= int(r["attack"]) <= hi):
            continue
        if "types" in spec and r["type"] not in spec["types"]:
            continue
        if r["starchip_cost"] in ("N/A", "999999") or int(r["level"]) > 6:
            continue
        pool.append(r)
    pool.sort(key=lambda r: (-int(r["attack"]), int(r["id"])))
    count = (need + 2) // 3
    step = max(1, len(pool) // count)  # espalha pela faixa em vez de pegar so os mais fortes
    picked = [pool[i] for i in range(0, len(pool), step)][:count]
    deck, left = {}, need
    for r in picked:
        n = min(3, left)
        if n:
            deck[int(r["id"])] = n
            left -= n
    assert left == 0, (spec, left, len(pool))
    return deck


def main():
    cat, _ = load_retail()
    (MOD / "duelists").mkdir(parents=True, exist_ok=True)
    (MOD / "portraits").mkdir(parents=True, exist_ok=True)
    decks, drops, notes = {}, {}, []
    for n in NPCS:
        duelist = {"copy": n["base"], "name": n["name"], "slot": n["slot"],
                   "unlock": {"story": 0x6E0 + n["gate"]}}
        (MOD / "duelists" / f"{n['id']}.json").write_text(json.dumps(duelist, indent=2) + "\n", encoding="utf-8")
        fill = fillers(cat, n["filler"], 40 - sum(n["deck"].values()))
        deck = {"fixed": True}
        deck.update({C(k): v for k, v in n["deck"].items()})
        deck.update({str(k): v for k, v in fill.items()})
        assert sum(v for k, v in deck.items() if k != "fixed") == 40, n["id"]
        decks[n["id"]] = deck
        drops[n["id"]] = {pool: {"replace": True, **{C(k): v for k, v in n[pool].items()}}
                          for pool in ("pow", "bcd", "tec")}
        # retrato: icone sobre degrade, recortado em quadrado
        icon_map.ICONS["_" + n["id"]] = n["icon"]
        img = gen_art.render({"id": "_" + n["id"], "colors": n["colors"]})
        img = img.crop((12, 0, 12 + 384, 384)).resize((192, 192))
        img.save(MOD / "portraits" / f"{n['id']}.png", optimize=True)
        notes.append((n, fill))
    mod = {
        "id": "fm2-duelists",
        "name": "FM 2 Duelists",
        "version": "0.1",
        "author": "FM 2",
        "description": "FM 2's intermediate opponents: four Free Duel characters, one per card line, "
                       "who give the new cards.",
        "enabled": True,
        "min_api": 16,
        "game": "slus_01411",
        "decks": decks,
        "drops": drops,
    }
    (MOD / "mod.json").write_text(json.dumps(mod, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("4 duelists ->", MOD)
    for n, fill in notes:
        print(n["name"], "apoio:", ", ".join(f"{cat[k]['name']} x{v}" for k, v in fill.items()))


if __name__ == "__main__":
    main()
