"""Cartas T5 - so se fazem misturando T4 de blocos diferentes. Ver gen_cards.py.
Custo: uma fusao T4 (4 cartas) + a outra T4 como carta real = 5 cartas, sem efeitos.
"""

NAME = "Mistura T5"

CARDS = [
    dict(id="mangrove-leviathan", colors=((40, 170, 150), (5, 50, 60)), tier=5, copy=718, name="Mangrove Leviathan",
         type="Sea Serpent", attribute="Water", level=8, stars=["Neptune", "Saturn"], attack=2800, defense=2600,
         description="Fusion: Tidal\nLeviathan + World\nTree Guardian"),
    dict(id="infernal-lich-drake", colors=((150, 30, 130), (25, 0, 35)), tier=5, copy=705, name="Infernal Lich Drake",
         type="Dragon", attribute="Dark", level=8, stars=["Pluto", "Mars"], attack=2900, defense=2400,
         description="Fusion: Wraith\nKing + Caldera\nDrake"),
]

RECIPES = [
    ("tidal-leviathan", "world-tree-guardian", "mangrove-leviathan"),
    ("wraith-king", "caldera-drake", "infernal-lich-drake"),
]
