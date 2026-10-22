"""Bloco 1 - linha Ember (fogo). Dados das cartas e das receitas; ver gen_cards.py."""

NAME = "Ember"

RETAIL_SUNBIRD = 467  # Crimson Sunbird (Winged Beast, Fire, 2300/1800)

CARDS = [
    # ---- T1: so no baralho/drop, sem receita para fazer ----
    dict(id="pebble-raptor", colors=((176, 132, 84), (84, 56, 34)), tier=1, copy=105, name="Pebble Raptor", type="Dinosaur", attribute="Earth",
         level=2, stars=["Saturn", "Moon"], attack=700, defense=500,
         description="A small raptor that\nnests in warm ash\nand cracked stone."),
    dict(id="spark-beetle", colors=((255, 214, 70), (176, 96, 20)), tier=1, copy=53, name="Spark Beetle", type="Insect", attribute="Fire",
         level=2, stars=["Mars", "Mercury"], attack=600, defense=500,
         description="Its wings leave a\ntrail of sparks. It\nis the seed of the\nEmber line."),
    dict(id="ash-sparrow", colors=((200, 190, 180), (96, 70, 60)), tier=1, copy=207, name="Ash Sparrow", type="Winged Beast", attribute="Fire",
         level=2, stars=["Mars", "Sun"], attack=700, defense=400,
         description="Born from the embers\nof a dead volcano."),
    # ---- T2 ----
    dict(id="ember-kindler", colors=((236, 92, 168), (112, 24, 90)), tier=2, copy=106, name="Ember Kindler", type="Spellcaster", attribute="Fire",
         level=3, stars=["Sun", "Mars"], attack=900, defense=900,
         description="{f8 0A 05}<Aura>{f8 0A 00} Your other\nFIRE monsters get\n+200 ATK.\nFusion: Ash Sparrow\n+ Pebble Raptor",
         monster_effects=[{"when": "face_up", "do": "boost", "target": "others",
                          "attribute": "Fire", "attack": 200}]),
    dict(id="ashfeather-hawk", colors=((255, 150, 60), (150, 54, 20)), tier=2, copy=581, name="Ashfeather Hawk", type="Winged Beast", attribute="Fire",
         level=4, stars=["Mars", "Sun"], attack=1400, defense=1000,
         description="Fusion: Ash Sparrow\n+ Spark Beetle"),
    dict(id="magma-raptor", colors=((226, 72, 40), (100, 24, 16)), tier=2, copy=80, name="Magma Raptor", type="Dinosaur", attribute="Fire",
         level=4, stars=["Mars", "Saturn"], attack=1500, defense=900,
         description="Fusion: Pebble Raptor\n+ Spark Beetle"),
    # ---- T3 ----
    dict(id="blazing-wyvern", colors=((240, 40, 40), (90, 10, 24)), tier=3, copy=383, name="Blazing Wyvern", type="Dragon", attribute="Fire",
         level=6, stars=["Mars", "Jupiter"], attack=1900, defense=1500,
         description="Fusion: Ashfeather\nHawk + Magma Raptor"),
    dict(id="obsidian-colossus", colors=((120, 90, 170), (20, 14, 40)), tier=3, copy=531, name="Obsidian Colossus", type="Rock", attribute="Earth",
         level=6, stars=["Saturn", "Mars"], attack=1800, defense=2300,
         description="Fusion: Magma\nRaptor + Ember\nKindler"),
    # ---- T4 ----
    dict(id="caldera-drake", colors=((210, 20, 60), (60, 0, 20)), tier=4, copy=571, name="Caldera Drake", type="Dragon", attribute="Fire",
         level=7, stars=["Mars", "Uranus"], attack=2400, defense=1900,
         description="{f8 0A 05}<Destroyed>{f8 0A 00} Deals 600\ndamage to the opponent.\nFusion: Blazing\nWyvern + Obsidian\nColossus",
         monster_effects=[{"when": "destroyed", "do": "damage", "amount": 600}]),
    # ---- T5: chefe das fusoes, precisa de uma carta original rara ----
    dict(id="solar-phoenix-dragon", colors=((255, 232, 120), (230, 100, 10)), tier=5, copy=713, name="Solar Phoenix Dragon", type="Dragon",
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
