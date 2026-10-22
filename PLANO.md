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

- [x] Fork `Henriqueufu/yugioh-fm2` criado
- [x] Imagem do disco USA validada (SHA-256 confere) e jogo rodando com `play.bat`
- [x] `CLAUDE.md` e `PLANO.md` no repositório
- [ ] Migrar a execução para o **Claude Code no Windows** (pasta `C:\Users\henri\yugioh-fm2`)
- [ ] Adicionar remote `upstream` → `https://github.com/Unchiga/Yu-Gi-Oh-Forbidden-Memories-Recompiled`
- [ ] Criar branch `fm2` (desenvolvimento) e manter `master` = upstream
- [ ] Criar save de teste (início da campanha) e guardar cópia de backup
- [ ] Definir e rodar o **smoke test** (abaixo) uma vez no jogo sem mods do FM 2

### Smoke test (rodar depois de toda mudança)

1. `.\play.bat` compila sem erro e o jogo abre.
2. **Game > Mods** lista os mods `fm2-*` sem erro ao lado.
3. Novo jogo → entrada de nome → primeira cena da história.
4. Um duelo completo (vitória) e a tela de recompensa.
5. Salvar, fechar, abrir e carregar o save.
6. Library e Build Deck abrem e mostram as cartas (incluindo as novas, quando houver).

---

## Fase 1 — Cartas e fusões novas (objetivo 2)

Referências: `notes/more-cards.md`, `notes/gameplay-tables.md`, `notes/card-catalog.csv`, `mods/yamyi-mods`.

- [ ] Pesquisar mods da comunidade como referência de balanceamento
- [ ] Escrever as **regras de balanceamento** (seção abaixo) e validar com o usuário
- [ ] Primeiro lote: ~10 cartas + algumas fusões em `mods/fm2-cards/`, com arte provisória
- [ ] Listar quais cartas novas vão para os decks e drops de cada NPC da Fase 2
- [ ] Testar em duelo, ajustar números, depois expandir em lotes
- [ ] Arte final das cartas (PNG 102x96, ou 408x384 para HD)

### Regras de balanceamento (rascunho — validar)

- Cada carta nova pertence a um **tier** ligado a um ponto da campanha; ATK/DEF dentro da faixa do tier.
- Fusão nova não pode gerar carta acima do tier dos materiais + 1.
- Nenhuma carta nova com ATK maior que as cartas de fim de jogo equivalentes.
- Drops de cartas fortes com peso baixo; nada de "carta quebrada" logo no começo.

## Fase 2 — NPCs intermediários (objetivo 4)

Referências: `notes/more-duelists.md`, `notes/tower-mode.md`, `notes/card-drops.md`.

- [ ] Mapear a progressão da campanha: ordem dos duelos principais e "saltos" de dificuldade
- [ ] Definir os degraus: entre quais duelos entra cada NPC e qual faixa de cartas ele dá
- [ ] Criar o mod `mods/fm2-duelists/` com 3–4 duelistas (deck, drops, retrato, condição de liberação), usando as cartas novas da Fase 1
- [ ] Calibrar: o NPC deve ajudar a passar o próximo chefe, não substituí-lo
- [ ] Rodar a progressão do começo até o primeiro chefe com os NPCs

## Fase 3 — Loja (objetivo 3)

Referências: `notes/card-packs.md`.

- [ ] Desenhar a economia: StarChips ganhos por duelo/rank × preço por raridade
- [ ] Booster packs por fase da campanha (desbloqueados conforme progresso), com pity e limite de cópias
- [ ] Mod `mods/fm2-shop/` com os packs
- [ ] (Extra, código) Compra de carta específica, venda e troca com regras próprias

## Fase 4 — Mundo 2D estilo Stardew (objetivo 1)

Referências: `notes/modding.md` (Code mods, API 4: substituir/envolver funções do jogo).

- [ ] Escolher arte: tileset e sprites livres (CC0) ou arte própria. **Não** usar assets do Stardew
- [ ] Prova de conceito: tela 2D aberta por um item do menu, personagem andando com colisão
- [ ] NPCs no mapa: interagir → diálogo → iniciar duelo (reaproveitando os duelistas da Fase 2)
- [ ] Ligar ao progresso da campanha (flags/save) sem quebrar a história original
- [ ] Decidir: substituir o mapa original ou manter as duas navegações
- [ ] Mais mapas, música, polimento

---

## Decisões registradas

- 2026-10-22 — Cartas novas vêm antes dos NPCs (fases 1 e 2 trocadas), para os duelistas novos já usarem as cartas.
- 2026-10-22 — Base do projeto: fork do port decompilado da Unchiga (não usar REA / engenharia reversa do zero).
- 2026-10-22 — Repositório na conta `Henriqueufu`; conta `cadulugaresi` fica para a faculdade (colaboradora do repo).
- 2026-10-22 — Execução do desenvolvimento pelo Claude Code no Windows; planejamento no projeto "Criação de jogo" do claude.ai.
- 2026-10-22 — Tudo como mod em `mods/fm2-*`; branch `fm2`; nunca versionar arquivos do jogo.
