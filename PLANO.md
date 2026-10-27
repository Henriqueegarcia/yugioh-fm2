# PLANO — Yu-Gi-Oh! Forbidden Memories 2

Objetivo: transformar o FM original numa versão "minha", jogável offline no PC, sem
quebrar o jogo. Ordem das fases: do menor risco para o maior. As fases 1 a 3 já
entregam um FM 2 jogável; a fase 4 é a mais ambiciosa e não trava as outras.

Legenda: `[ ]` a fazer · `[~]` em andamento · `[x]` feito

---

## Visão geral dos 4 objetivos

| # | Objetivo | Viabilidade | Como |
|---|----------|-------------|------|
| 1 | Cartas e fusões novas, balanceadas | ✅ Viável | Mod de dados: `cards` (IDs > 722) + tabelas de fusão/drops. Limite: carta nova copia uma original e herda o **modelo 3D** dela; precisa de **arte** própria |
| 2 | NPCs que dão cartas intermediárias | ✅ Fácil | Mod de dados: duelistas novos (deck, drops, retrato, AI, condição de liberação) |
| 3 | Loja de cartas melhor que a de StarChips | 🟡 Parcial | Booster packs já existem (raridade, pity, estoque, desbloqueio). Compra direta / venda / troca exigem **mod em código** |
| 4 | Navegação 2D estilo Stardew Valley | 🔴 Grande | Mod em código substituindo/complementando o mapa. Precisa de **arte** (tileset/sprites livres, ex. CC0) e cuidado com flags da campanha |

---

## Fase 0 — Fundação

- [x] Fork `Henriqueegarcia/yugioh-fm2` criado
- [x] Imagem do disco USA validada (SHA-256 confere) e jogo rodando com `play.bat`
- [x] `CLAUDE.md` e `PLANO.md` no repositório
- [x] Migrar a execução para o **Claude Code no Windows** (pasta `C:\Users\henri\yugioh-fm2`)
- [x] Adicionar remote `upstream` → `https://github.com/Unchiga/Yu-Gi-Oh-Forbidden-Memories-Recompiled`
- [x] Criar branch `fm2` (desenvolvimento) e manter `master` = upstream
- [x] Criar save de teste (início da campanha) e guardar cópia de backup (em `C:\Users\henri\fm2-backups\`, fora do repo)
- [x] Definir e rodar o **smoke test** (abaixo) uma vez no jogo sem mods do FM 2

### Smoke test (rodar depois de toda mudança)

1. `.\play.bat` compila sem erro e o jogo abre.
2. **Game > Mods** lista os mods `fm2-*` sem erro ao lado.
3. Novo jogo → entrada de nome → primeira cena da história.
4. Um duelo completo (vitória) e a tela de recompensa.
5. Salvar, fechar, abrir e carregar o save.
6. Library e Build Deck abrem e mostram as cartas (incluindo as novas, quando houver).

---

## Fase 1 — Cartas e fusões novas (objetivo 1)

Referências: `notes/more-cards.md`, `notes/gameplay-tables.md`, `notes/card-catalog.csv`, `mods/yamyi-mods`.

- [x] Pesquisar mods da comunidade como referência de balanceamento (`docs/fm2-pesquisa-balanceamento.md`)
- [~] Escrever as **regras de balanceamento** (seção abaixo) e validar com o usuário (rascunho pronto, falta validar)
- [x] Primeiro lote: linha Ember, 10 cartas + 7 fusões em `mods/fm2-cards/`, arte provisória (`docs/fm2-lote1-ember.md`), testado no jogo
- [x] Verificador de balanceamento (`tools/fm2/check_balance.py`), com o limite de cartas do baralho
- [x] Expandir (plano aprovado): **4 blocos-base** (Ember, Tide, Grove, Crypt), de T1 até ~2300 ATK; testados em jogo os três primeiros, Crypt aguarda teste. **Decisão (26/10): cartas novas não têm efeitos de monstro.** Lista de receitas em `docs/fm2-fusoes.md`
- [x] **2 cartas T5** (Mangrove Leviathan = Tidal Leviathan + World Tree Guardian; Infernal Lich Drake = Wraith King + Caldera Drake), aguardam teste
- [x] **4 cartas híbridas** (Cinder Knight, Reefstone Sentinel, Thornwolf Alpha, Bone Dragon Overlord), aguardam teste
- [x] Listar quais cartas novas vão para os decks e drops de cada NPC da Fase 2 (`docs/fm2-fase2-npcs.md`)
- [ ] Testar em duelo, ajustar números, depois expandir em lotes
- [ ] Arte final das cartas (PNG 102x96, ou 408x384 para HD)

### Regras de balanceamento (rascunho — validar)

Base dos números: `docs/fm2-pesquisa-balanceamento.md`.

**Tiers** (por ATK; ligados ao ATK médio dos decks dos duelistas):

| Tier | ATK máx. | Ponto da campanha | Cartas originais na faixa |
|---|---|---|---|
| T1 | 1000 | início (decks de 200–450) | 260 |
| T2 | 1500 | começo-meio a meio (decks de 500–1450) | 180 |
| T3 | 2000 | meio a fim (decks de 1100–1900) | 122 |
| T4 | 2500 | fim de jogo | 38 |
| T5 | 3000 | chefes / fusões raras | 21 |

1. Cada carta nova tem um tier; ATK dentro da faixa dele e **nunca acima do máximo do tier**.
2. ATK/DEF seguem o **nível** da carta: entre o 1º e o 3º quartil das originais daquele nível (ex.: nível 4 → ~900–1600 de ATK). Acima disso só com custo (ex.: DEF baixa, tipo raro, efeito ruim).
3. Efeito de monstro: **no máximo 1** nas cartas de T1–T2 e 2 nas demais; valores pequenos (`boost` ≤ 300 em T1–T2, ≤ 500 depois; `damage`/`heal` ≤ 500 em T1–T2, ≤ 1000 depois). Nada de `destroy` em massa antes do T4.
4. Fusão nova não gera carta acima do tier dos materiais + 1. Receita nova para resultado que já tem centenas de receitas quase não muda o jogo; prefira resultados raros.
5. Nenhuma carta nova com ATK maior que as originais de fim de jogo equivalentes (máx. 3000, exceto chefes decididos caso a caso).
6. Drops: carta do tier atual com peso 8–40 em 2048 (0,4%–2%); carta do tier seguinte com peso ≤ 10; T4 e T5 só em duelistas do fim. Nenhuma carta T3+ em drops de duelista do começo.
7. Magia/armadilha nova precisa de `ai_effect` para a IA usá-la; o dano/cura segue os valores da regra 3.
8. Todo lote novo é testado em duelo (como jogador e como oponente) antes do próximo.
9. **Limite de cartas no baralho** (baralho de 40, no máx. 3 cópias de cada, mão de 5): o resultado de uma fusão não vai para a coleção e uma cadeia usa só a mão e 1 monstro do campo. Por isso cada carta feita por fusão tem teto de **cartas exigidas**: T2 ≤ 2, T3 ≤ 3, T4 ≤ 4, T5 ≤ 6; nenhuma carta exigida mais de 3 vezes. Se as duas entradas de uma receita forem fusões, uma delas precisa existir como carta real (com drop). `python tools/fm2/check_balance.py` confere tudo isso e deve passar antes de cada lote.


## Fase 2 — NPCs intermediários (objetivo 2)

Referências: `notes/more-duelists.md`, `notes/tower-mode.md`, `notes/card-drops.md`.

- [~] Mapear a progressão da campanha: ordem dos duelos principais e "saltos" de dificuldade (usei a tabela de força da pesquisa; falta conferir jogando)
- [x] Definir os degraus: entre quais duelos entra cada NPC e qual faixa de cartas ele dá
- [x] Criar o mod `mods/fm2-duelists/` com 3–4 duelistas (deck, drops, retrato, condição de liberação), usando as cartas novas da Fase 1
- [ ] Calibrar: o NPC deve ajudar a passar o próximo chefe, não substituí-lo
- [ ] Rodar a progressão do começo até o primeiro chefe com os NPCs

## Fase 3 — Loja (objetivo 3)

Referências: `notes/card-packs.md`.

- [x] Desenhar a economia (`docs/fm2-fase3-loja.md`; números a calibrar jogando): StarChips ganhos por duelo/rank × preço por raridade
- [x] Booster packs por fase da campanha (desbloqueados conforme progresso), com pity e limite de cópias
- [x] Mod `mods/fm2-shop/` com os packs
- [x] Compra de carta específica por senha (`docs/fm2-senhas.md`); venda e troca ficam de fora por exigirem código

## Fase 4 — Mundo 2D estilo Stardew (objetivo 4)

Referências: `notes/modding.md` (Code mods, API 4: substituir/envolver funções do jogo).

- [~] Pesquisa feita (27/10): o mod de código só desenha texto e retângulos (sem imagens); duelo se inicia como a Torre faz (`func_80024DC8`); compilador de mods funciona. Ver `docs/fm2-fase4-pesquisa.md`
- [ ] Escolher arte: tileset e sprites livres (CC0) ou arte própria. **Não** usar assets do Stardew
- [~] Prova de conceito (`mods/fm2-world/`, aguardando teste do usuário): tela 2D aberta por um item do menu, personagem andando com colisão
- [~] NPCs no mapa (os 10 já estão na prova de conceito): interagir → diálogo → iniciar duelo (reaproveitando os duelistas da Fase 2)
- [ ] Ligar ao progresso da campanha (flags/save) sem quebrar a história original
- [x] Decidir: substituir o mapa original ou manter as duas navegações — **conviver** (botão WORLD no segundo menu; decidido em 27/10)
- [ ] Mais mapas, música, polimento

---

## Decisões registradas

- 2026-10-22 — Cartas novas vêm antes dos NPCs (fases 1 e 2 trocadas), para os duelistas novos já usarem as cartas.
- 2026-10-22 — Base do projeto: fork do port decompilado da Unchiga (não usar REA / engenharia reversa do zero).
- 2026-10-22 — Repositório na conta `Henriqueegarcia` (fork do port da Unchiga); remote `origin` = fork, `upstream` = Unchiga.
- 2026-10-22 — Execução do desenvolvimento pelo Claude Code no Windows; planejamento no projeto "Criação de jogo" do claude.ai.
- 2026-10-22 — Tudo como mod em `mods/fm2-*`; branch `fm2`; nunca versionar arquivos do jogo.
