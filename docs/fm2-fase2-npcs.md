# FM 2 - Fase 2: NPCs intermediários

Mod `mods/fm2-duelists/` (gerado por `tools/fm2/gen_duelists.py`; edite o script, não os JSON).
São 10 duelistas novos no **Duelo Livre** (casas 40-49 da grade, páginas 2), os 4 primeiros um por linha de cartas e os 6 do segundo grupo entre eles e no fim.
Cada um só aparece quando a campanha libera um duelista original (flag `0x6E0 + n`).

| NPC | Linha | Aparece depois de | Joga como (IA/base) | Deck (40 cartas fixas) |
|---|---|---|---|---|
| Kael | Ember (fogo) | Seto (7) | Villager 2 | 18 cartas Ember até T3 + 22 originais de apoio |
| Marin | Tide (água) | Mai Valentine (11) | Mai Valentine | 21 cartas Tide até T3 + 19 de apoio |
| Brenn | Grove (planta/inseto) | Kaiba (17) | Weevil Underwood | 23 cartas Grove até T4 + 17 de apoio |
| Morrow | Crypt (mortos-vivos) | Forest Mage (23) | High Mage Atenza | 22 cartas Crypt até T4 + 18 de apoio |

### Segundo grupo (casas 44-49)

| NPC | Papel | Aparece depois de | IA como | Cartas |
|---|---|---|---|---|
| Pip | iniciante: T1 de todas as linhas | Teana (2) | Villager 1 | T1 das 4 linhas; drops T1 e 3 T2 chave |
| Hana | Ember + Grove | Rex Raptor (9) | Rex Raptor | T1/T2 das duas; drops até T3 |
| Ignis | Ember + Crypt | Yami Bakura (14) | Yami Bakura | T1-T3 + Caldera Drake; drops T4 (Caldera, Wraith King, Grim Harvester) e híbridas Cinder Knight/Bone Dragon Overlord |
| Coral | Tide + Grove | Ocean Mage (21) | Ocean Mage | T1-T3 + 4 T4; drops T3, T4 e híbridas Reefstone Sentinel/Thornwolf Alpha |
| Vesper | todas as linhas, fim de jogo | Seto 2nd (32) | Seto 2nd | T3 x2 + T4 de todas; drops T3/T4 |
| Orin | chefe: deck com as 3 T5 | Seto 3rd (36) | Seto 3rd | T3, T4 e T5; drops T3/T4 (as T5 nunca caem) |

## Drops (só cartas do próprio bloco)

| Rank | O que cai |
|---|---|
| B/C/D (`bcd`) | T1 (peso 30 cada) e T2 (peso 8-12) |
| S/A poder (`pow`) | T1 e T2 (peso 20 cada) e T3 (peso 8) |
| S/A técnica (`tec`) | T2 (20), T3 (12) e **um T4 (peso 4)** |

Isso cobre as cartas intermediárias que as receitas exigem como carta real: Magma Raptor, Ember Kindler,
Obsidian Colossus (Kael), Deepwater Serpent (Marin), Spore Shaman (Brenn), Sepulchre Golem (Morrow).
Os T4 (Caldera Drake, Tidal Leviathan, World Tree Guardian, Wraith King, Grim Harvester) saem só com S/A de técnica,
e servem de carta real para as duas T5. As híbridas e as T5 só se fazem por fusão.

## Decisões provisórias (mudar em `gen_duelists.py`)

- Os pontos de liberação (`gate`) são palpite pela tabela de força dos duelistas da pesquisa; ajustar depois de jogar.
- As cartas de apoio originais são escolhidas por atributo/ATK, sem curadoria.
- Retratos provisórios feitos com ícones de game-icons.net (ver `CREDITS-arte.md`).
- `USE_GATES = False` em `gen_duelists.py` libera os 4 desde o início (modo de teste); `True` ativa as liberações da tabela.
- NPCs no mapa 2D só na Fase 4; por enquanto são oponentes do Duelo Livre.
