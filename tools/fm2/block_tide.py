"""Bloco 2 - linha Tide (agua). Dados das cartas e das receitas; ver gen_cards.py.

Cadeia: T1 (drop) -> T2 (2 cartas) -> T3 (3 cartas) -> T4 (4 cartas), ate 2300 ATK.
Os T4 exigem Abyssal Nautilus (T3) como carta real no baralho: ela precisa ter drop.
"""

NAME = "Tide"

RETAIL_ARMORED_STARFISH = 615   # Aqua, Water, 850/1400
RETAIL_GIANT_RED_SEASNAKE = 447  # Aqua, Water, 1800/800

CARDS = [
    # ---- T1: so no baralho/drop ----
    dict(id="foam-sprite", colors=((170, 232, 240), (40, 110, 150)), tier=1, copy=444, name="Foam Sprite",
         type="Aqua", attribute="Water", level=2, stars=["Neptune", "Mercury"], attack=500, defense=600,
         description="A shy spirit made of\nsea foam. It pops\nwhen it laughs."),
    dict(id="reef-crab", colors=((250, 150, 120), (150, 50, 60)), tier=1, copy=451, name="Reef Crab",
         type="Aqua", attribute="Water", level=3, stars=["Neptune", "Saturn"], attack=800, defense=900,
         description="Its shell is built\nfrom coral and\nstubbornness."),
    dict(id="brine-eel", colors=((90, 200, 170), (10, 70, 80)), tier=1, copy=475, name="Brine Eel",
         type="Sea Serpent", attribute="Water", level=3, stars=["Neptune", "Pluto"], attack=800, defense=500,
         description="It hunts in the dark\nwater under the reef."),
    # ---- T2 ----
    dict(id="tide-priestess", colors=((150, 160, 255), (40, 40, 140)), tier=2, copy=525, name="Tide Priestess",
         type="Spellcaster", attribute="Water", level=3, stars=["Moon", "Neptune"], attack=800, defense=1000,
         description="Fusion: Foam Sprite\n+ Reef Crab"),
    dict(id="coral-guardian", colors=((255, 120, 150), (120, 20, 70)), tier=2, copy=71, name="Coral Guardian",
         type="Aqua", attribute="Water", level=4, stars=["Neptune", "Saturn"], attack=1200, defense=1500,
         description="Fusion: Reef Crab\n+ Brine Eel"),
    dict(id="razor-barracuda", colors=((190, 200, 215), (50, 70, 100)), tier=2, copy=60, name="Razor Barracuda",
         type="Fish", attribute="Water", level=4, stars=["Neptune", "Mars"], attack=1500, defense=800,
         description="Fusion: Brine Eel\n+ Foam Sprite"),
    # ---- T3 ----
    dict(id="deepwater-serpent", colors=((40, 150, 200), (5, 30, 90)), tier=3, copy=442, name="Deepwater Serpent",
         type="Sea Serpent", attribute="Water", level=6, stars=["Neptune", "Jupiter"], attack=1900, defense=1500,
         description="Fusion: Razor\nBarracuda + Brine Eel"),
    dict(id="abyssal-nautilus", colors=((200, 170, 255), (60, 20, 110)), tier=3, copy=639, name="Abyssal Nautilus",
         type="Aqua", attribute="Water", level=5, stars=["Neptune", "Uranus"], attack=1700, defense=2000,
         description="Fusion: Coral Guardian\n+ Armored Starfish"),
    # ---- T4 ----
    dict(id="tidal-leviathan", colors=((20, 110, 190), (0, 10, 60)), tier=4, copy=718, name="Tidal Leviathan",
         type="Fish", attribute="Water", level=7, stars=["Neptune", "Moon"], attack=2300, defense=2000,
         description="Fusion: Deepwater\nSerpent + Abyssal\nNautilus"),
    dict(id="maelstrom-serpent", colors=((120, 230, 230), (10, 60, 110)), tier=4, copy=223, name="Maelstrom Serpent",
         type="Sea Serpent", attribute="Water", level=7, stars=["Neptune", "Pluto"], attack=2200, defense=1700,
         description="Fusion: Abyssal\nNautilus + Giant Red\nSeasnake"),
]

RECIPES = [
    ("foam-sprite", "reef-crab", "tide-priestess"),
    ("reef-crab", "brine-eel", "coral-guardian"),
    ("brine-eel", "foam-sprite", "razor-barracuda"),
    ("razor-barracuda", "brine-eel", "deepwater-serpent"),
    ("coral-guardian", RETAIL_ARMORED_STARFISH, "abyssal-nautilus"),
    ("deepwater-serpent", "abyssal-nautilus", "tidal-leviathan"),
    ("abyssal-nautilus", RETAIL_GIANT_RED_SEASNAKE, "maelstrom-serpent"),
]
