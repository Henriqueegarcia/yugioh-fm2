# Blocos 2 e 3 — Tide (água) e Grove (planta e inseto)

Mesma lógica da linha Ember (`docs/fm2-lote1-ember.md`): T1 só por drop, T2 a partir de
2 cartas, T3 a partir de 3, T4 a partir de 4, no máximo 2300 de ATK. Dados em
`tools/fm2/block_tide.py` e `tools/fm2/block_grove.py`; `python tools/fm2/gen_cards.py`
regera o mod e `python tools/fm2/check_balance.py` confere o balanceamento.

## Tide (IDs 733–742)

| Carta | Tier | ATK/DEF | Receita | Efeito |
|---|---|---|---|---|
| Foam Sprite | T1 | 500/600 | drop | — |
| Reef Crab | T1 | 800/900 | drop | — |
| Brine Eel | T1 | 800/500 | drop | — |
| Tide Priestess | T2 | 800/1000 | Foam Sprite + Reef Crab | no seu turno, cura 300 LP |
| Coral Guardian | T2 | 1200/1500 | Reef Crab + Brine Eel | — |
| Razor Barracuda | T2 | 1500/800 | Brine Eel + Foam Sprite | — |
| Deepwater Serpent | T3 | 1900/1500 | Razor Barracuda + Brine Eel | — |
| Abyssal Nautilus | T3 | 1700/2000 | Coral Guardian + Armored Starfish (original) | — |
| Tidal Leviathan | T4 | 2300/2000 | Deepwater Serpent + Abyssal Nautilus | em batalha, o rival perde 300 ATK |
| Maelstrom Serpent | T4 | 2200/1700 | Abyssal Nautilus + Giant Red Seasnake (original) | destrói monstro: cura 500 LP |

## Grove (IDs 743–752)

| Carta | Tier | ATK/DEF | Receita | Efeito |
|---|---|---|---|---|
| Leaf Grub | T1 | 300/500 | drop | — |
| Thorn Sprout | T1 | 600/500 | drop | — |
| Mossback Beetle | T1 | 800/900 | drop | — |
| Bramble Mantis | T2 | 1300/1000 | Leaf Grub + Mossback Beetle | — |
| Grove Warden | T2 | 1200/1500 | Thorn Sprout + Leaf Grub | — |
| Spore Shaman | T2 | 900/800 | Thorn Sprout + Mossback Beetle | em batalha, +300 ATK |
| Hornet Duke | T3 | 1800/1400 | Bramble Mantis + Killer Needle (original) | — |
| Ancient Treant | T3 | 1700/2200 | Grove Warden + Spore Shaman | — |
| Emperor Scarab | T4 | 2300/2000 | Hornet Duke + Leaf Grub | em batalha, +300 ATK |
| World Tree Guardian | T4 | 2200/2300 | Ancient Treant + Thorn Sprout | outras PLANT: +200 ATK/DEF |

## Cartas que precisam de drop (aviso do verificador)

Quando as duas entradas de uma receita são fusões, uma delas tem de existir como carta
real no baralho (fusão não vai para a coleção). Na Fase 2 estas precisam cair de algum duelista:
Magma Raptor, Obsidian Colossus, Ember Kindler (Ember); Deepwater Serpent (Tide);
Spore Shaman (Grove). Sem isso as receitas T4/T5 listadas pelo verificador não são alcançáveis.
