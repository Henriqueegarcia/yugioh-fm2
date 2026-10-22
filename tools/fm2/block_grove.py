"""Bloco 3 - linha Grove (planta e inseto). Dados das cartas e das receitas; ver gen_cards.py.

Cadeia: T1 (drop) -> T2 (2 cartas) -> T3 (3 cartas) -> T4 (4 cartas), ate 2300 ATK.
Ancient Treant e feita por duas fusoes: Spore Shaman precisa ser carta real (ter drop).
"""

NAME = "Grove"

RETAIL_KILLER_NEEDLE = 53  # Insect, Wind, 1200/1000

CARDS = [
    # ---- T1: so no baralho/drop ----
    dict(id="leaf-grub", colors=((190, 235, 110), (60, 110, 30)), tier=1, copy=499, name="Leaf Grub",
         type="Insect", attribute="Earth", level=1, stars=["Mercury", "Saturn"], attack=300, defense=500,
         description="It eats one leaf a\nday and dreams of\nwings."),
    dict(id="thorn-sprout", colors=((110, 190, 90), (20, 70, 40)), tier=1, copy=123, name="Thorn Sprout",
         type="Plant", attribute="Earth", level=2, stars=["Saturn", "Venus"], attack=600, defense=500,
         description="A seedling armed\nwith tiny thorns."),
    dict(id="mossback-beetle", colors=((150, 170, 90), (50, 60, 30)), tier=1, copy=479, name="Mossback Beetle",
         type="Insect", attribute="Earth", level=3, stars=["Saturn", "Mercury"], attack=800, defense=900,
         description="Moss grows on its\nback, so the forest\nhides it well."),
    # ---- T2 ----
    dict(id="bramble-mantis", colors=((120, 230, 130), (20, 90, 50)), tier=2, copy=535, name="Bramble Mantis",
         type="Insect", attribute="Earth", level=4, stars=["Mercury", "Mars"], attack=1300, defense=1000,
         description="Fusion: Leaf Grub\n+ Mossback Beetle"),
    dict(id="grove-warden", colors=((60, 160, 100), (10, 60, 50)), tier=2, copy=511, name="Grove Warden",
         type="Plant", attribute="Earth", level=4, stars=["Saturn", "Venus"], attack=1200, defense=1500,
         description="Fusion: Thorn Sprout\n+ Leaf Grub"),
    dict(id="spore-shaman", colors=((200, 140, 230), (80, 30, 110)), tier=2, copy=619, name="Spore Shaman",
         type="Spellcaster", attribute="Earth", level=3, stars=["Saturn", "Moon"], attack=900, defense=800,
         description="{f8 0A 05}<Battle>{f8 0A 00} Gets +300 ATK\nwhile it fights.\nFusion: Thorn Sprout\n+ Mossback Beetle",
         monster_effects=[{"when": "combat", "do": "boost", "target": "self", "attack": 300}]),
    # ---- T3 ----
    dict(id="hornet-duke", colors=((255, 230, 70), (130, 90, 10)), tier=3, copy=614, name="Hornet Duke",
         type="Insect", attribute="Wind", level=5, stars=["Mercury", "Jupiter"], attack=1800, defense=1400,
         description="Fusion: Bramble\nMantis + Killer Needle"),
    dict(id="ancient-treant", colors=((100, 140, 70), (30, 50, 20)), tier=3, copy=594, name="Ancient Treant",
         type="Plant", attribute="Earth", level=5, stars=["Saturn", "Venus"], attack=1700, defense=2200,
         description="Fusion: Grove Warden\n+ Spore Shaman"),
    # ---- T4 ----
    dict(id="emperor-scarab", colors=((90, 220, 170), (10, 80, 70)), tier=4, copy=717, name="Emperor Scarab",
         type="Insect", attribute="Earth", level=7, stars=["Mercury", "Sun"], attack=2300, defense=2000,
         description="{f8 0A 05}<Battle>{f8 0A 00} Gets +300 ATK\nwhile it fights.\nFusion: Hornet Duke\n+ Leaf Grub",
         monster_effects=[{"when": "combat", "do": "boost", "target": "self", "attack": 300}]),
    dict(id="world-tree-guardian", colors=((70, 200, 80), (10, 60, 30)), tier=4, copy=638, name="World Tree Guardian",
         type="Plant", attribute="Earth", level=7, stars=["Saturn", "Venus"], attack=2200, defense=2300,
         description="{f8 0A 05}<Aura>{f8 0A 00} Your other\nPLANT monsters get\n+200 ATK and DEF.\nFusion: Ancient\nTreant + Thorn Sprout",
         monster_effects=[{"when": "face_up", "do": "boost", "target": "others", "type": "Plant",
                           "attack": 200, "defense": 200}]),
]

RECIPES = [
    ("leaf-grub", "mossback-beetle", "bramble-mantis"),
    ("thorn-sprout", "leaf-grub", "grove-warden"),
    ("thorn-sprout", "mossback-beetle", "spore-shaman"),
    ("bramble-mantis", RETAIL_KILLER_NEEDLE, "hornet-duke"),
    ("grove-warden", "spore-shaman", "ancient-treant"),
    ("hornet-duke", "leaf-grub", "emperor-scarab"),
    ("ancient-treant", "thorn-sprout", "world-tree-guardian"),
]
