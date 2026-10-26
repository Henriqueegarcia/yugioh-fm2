"""Cartas hibridas - uma carta nova de cada bloco fundida com uma carta ORIGINAL. Ver gen_cards.py.
Todas T3/T4, 2 cartas de custo, sem efeitos.
"""

NAME = "Hibridas"

CARDS = [
    dict(id="cinder-knight", colors=((255, 170, 90), (130, 50, 30)), tier=3, copy=15, name="Cinder Knight",
         type="Warrior", attribute="Fire", level=5, stars=["Mars", "Sun"], attack=1900, defense=1600,
         description="Fusion: Ashfeather\nHawk + Celtic\nGuardian"),
    dict(id="reefstone-sentinel", colors=((110, 190, 205), (30, 70, 90)), tier=3, copy=74, name="Reefstone Sentinel",
         type="Rock", attribute="Water", level=5, stars=["Neptune", "Saturn"], attack=1600, defense=2300,
         description="Fusion: Coral\nGuardian + Giant\nSoldier of Stone"),
    dict(id="thornwolf-alpha", colors=((130, 175, 80), (45, 75, 30)), tier=3, copy=65, name="Thornwolf Alpha",
         type="Beast", attribute="Earth", level=5, stars=["Saturn", "Venus"], attack=1900, defense=1500,
         description="Fusion: Grove\nWarden + Silver Fang"),
    dict(id="bone-dragon-overlord", colors=((190, 180, 200), (50, 30, 70)), tier=4, copy=97, name="Bone Dragon Overlord",
         type="Dragon", attribute="Dark", level=7, stars=["Pluto", "Jupiter"], attack=2300, defense=1700,
         description="Fusion: Crypt\nKeeper + Curse of\nDragon"),
]

RECIPES = [
    ("ashfeather-hawk", 41, "cinder-knight"),          # Celtic Guardian
    ("coral-guardian", 74, "reefstone-sentinel"),      # Giant Soldier of Stone
    ("grove-warden", 65, "thornwolf-alpha"),           # Silver Fang
    ("crypt-keeper", 39, "bone-dragon-overlord"),      # Curse of Dragon
]
