# Lote 1 — linha Ember (mods/fm2-cards)

10 cartas de fogo feitas para serem **fundidas**: as fracas se juntam em cartas
médias, as médias em fortes, e a mais forte exige uma carta original rara.
Gerado por `python tools/fm2/gen_cards.py` (edite o script, não o `mod.json`).

| ID | Carta | Tier | Tipo/Atributo | ATK/DEF | Base (modelo/arte) | Como se obtém |
|---|---|---|---|---|---|---|
| 723 | Pebble Raptor | T1 | Dinosaur/Earth | 700/500 | Tomozaurus | só drop/deck |
| 724 | Spark Beetle | T1 | Insect/Fire | 600/500 | Killer Needle | só drop/deck |
| 725 | Ash Sparrow | T1 | Winged Beast/Fire | 700/400 | Droll Bird | só drop/deck |
| 726 | Ember Kindler | T2 | Spellcaster/Fire | 900/900 | Spirit of the Winds | Ash Sparrow + Pebble Raptor |
| 727 | Ashfeather Hawk | T2 | Winged Beast/Fire | 1400/1000 | Takuhee | Ash Sparrow + Spark Beetle |
| 728 | Magma Raptor | T2 | Dinosaur/Fire | 1500/900 | Uraby | Pebble Raptor + Spark Beetle |
| 729 | Blazing Wyvern | T3 | Dragon/Fire | 1900/1500 | Parrot Dragon | Ashfeather Hawk + Magma Raptor |
| 730 | Obsidian Colossus | T3 | Rock/Earth | 1800/2300 | Mystical Sand | Magma Raptor + Ember Kindler |
| 731 | Caldera Drake | T4 | Dragon/Fire | 2400/1900 | B. Dragon Jungle King | Blazing Wyvern + Obsidian Colossus |
| 732 | Solar Phoenix Dragon | T5 | Dragon/Fire | 2900/2300 | Meteor B. Dragon | Caldera Drake + Crimson Sunbird (original) |

Os IDs de execução (723+) dependem da ordem de carga dos mods; o save guarda a
identidade estável `fm2-cards:<id>:1`.

## Efeitos
- Ember Kindler: enquanto virada para cima, seus outros monstros FIRE ganham +200 ATK.
- Caldera Drake: ao ser destruída, causa 600 de dano ao oponente.
- Solar Phoenix Dragon: seus outros monstros FIRE ganham +300 ATK/DEF; ao ser destruída, 800 de dano.

## Decisões
- **Fusão de 4 níveis até o T5**: 4 fusões em cadeia (Spark Beetle/Ash Sparrow → Hawk →
  Wyvern → Drake → Phoenix), e a última precisa de Crimson Sunbird (700 starchips, fim de jogo).
- **Receitas herdadas bloqueadas**: uma carta nova herda as receitas de fusão da
  base. O script bloqueia (`result: null`) toda receita herdada cujo resultado passe do
  teto do tier seguinte (99 bloqueios), para o T1 não fundir direto em carta de fim de jogo.
- `"drops": false` em todas: não entram no drop das cartas-base. Entrada em decks e drops
  é decidida junto com os NPCs na Fase 2.
- Arte provisória: a da carta-base.

## Ver no save
O arquivo `cards/000C30F1.txt` na pasta de dados do jogo
(`Documents\My Games\YFM Re-Decomp`) dá 3 cópias de cada carta ao save atual
(duelista `000C30F1`). Para o Solar Phoenix Dragon falta ter Crimson Sunbird (id 467).
