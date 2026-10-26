"""Bloco 4 - linha Crypt (mortos-vivos). Dados das cartas e das receitas; ver gen_cards.py.

Cadeia: T1 (drop) -> T2 (2 cartas) -> T3 (3 cartas) -> T4 (4 cartas), ate 2300 ATK. Sem efeitos.
"""

NAME = "Crypt"

RETAIL_ZOMBIE_WARRIOR = 30  # Zombie, Dark, 1200/900

CARDS = [
    # ---- T1: so no baralho/drop ----
    dict(id="bone-pup", colors=((225, 220, 205), (90, 85, 80)), tier=1, copy=548, name="Bone Pup",
         type="Zombie", attribute="Dark", level=2, stars=["Pluto", "Moon"], attack=500, defense=400,
         description="A puppy that never\nleft its master's\ngrave."),
    dict(id="grave-wisp", colors=((170, 230, 215), (30, 80, 90)), tier=1, copy=203, name="Grave Wisp",
         type="Zombie", attribute="Dark", level=2, stars=["Pluto", "Mercury"], attack=600, defense=800,
         description="A pale flame that\nflickers over old\ntombs."),
    dict(id="rattle-squire", colors=((150, 150, 175), (45, 45, 70)), tier=1, copy=154, name="Rattle Squire",
         type="Zombie", attribute="Dark", level=3, stars=["Pluto", "Mars"], attack=800, defense=500,
         description="A skeleton still\ncarrying a rusty\nshield."),
    # ---- T2 ----
    dict(id="crypt-keeper", colors=((140, 110, 170), (40, 25, 70)), tier=2, copy=351, name="Crypt Keeper",
         type="Zombie", attribute="Dark", level=4, stars=["Pluto", "Saturn"], attack=1200, defense=1500,
         description="Fusion: Bone Pup\n+ Grave Wisp"),
    dict(id="hollow-knight", colors=((120, 130, 150), (25, 30, 50)), tier=2, copy=241, name="Hollow Knight",
         type="Zombie", attribute="Dark", level=4, stars=["Pluto", "Mars"], attack=1500, defense=900,
         description="Fusion: Bone Pup\n+ Rattle Squire"),
    dict(id="wailing-banshee", colors=((200, 190, 255), (70, 50, 130)), tier=2, copy=470, name="Wailing Banshee",
         type="Spellcaster", attribute="Dark", level=4, stars=["Pluto", "Moon"], attack=1100, defense=1200,
         description="Fusion: Grave Wisp\n+ Rattle Squire"),
    # ---- T3 ----
    dict(id="revenant-lord", colors=((90, 60, 120), (15, 5, 35)), tier=3, copy=545, name="Revenant Lord",
         type="Zombie", attribute="Dark", level=6, stars=["Pluto", "Jupiter"], attack=1900, defense=1500,
         description="Fusion: Hollow\nKnight + Grave Wisp"),
    dict(id="sepulchre-golem", colors=((150, 140, 120), (50, 45, 35)), tier=3, copy=99, name="Sepulchre Golem",
         type="Rock", attribute="Earth", level=6, stars=["Saturn", "Pluto"], attack=1700, defense=2200,
         description="Fusion: Crypt\nKeeper + Bone Pup"),
    # ---- T4 ----
    dict(id="wraith-king", colors=((70, 20, 110), (5, 0, 25)), tier=4, copy=564, name="Wraith King",
         type="Zombie", attribute="Dark", level=7, stars=["Pluto", "Uranus"], attack=2300, defense=1900,
         description="Fusion: Revenant\nLord + Sepulchre\nGolem"),
    dict(id="grim-harvester", colors=((60, 60, 70), (0, 0, 10)), tier=4, copy=719, name="Grim Harvester",
         type="Zombie", attribute="Dark", level=7, stars=["Pluto", "Saturn"], attack=2200, defense=2000,
         description="Fusion: Sepulchre\nGolem + Zombie\nWarrior"),
]

RECIPES = [
    ("bone-pup", "grave-wisp", "crypt-keeper"),
    ("bone-pup", "rattle-squire", "hollow-knight"),
    ("grave-wisp", "rattle-squire", "wailing-banshee"),
    ("hollow-knight", "grave-wisp", "revenant-lord"),
    ("crypt-keeper", "bone-pup", "sepulchre-golem"),
    ("revenant-lord", "sepulchre-golem", "wraith-king"),
    ("sepulchre-golem", RETAIL_ZOMBIE_WARRIOR, "grim-harvester"),
]
