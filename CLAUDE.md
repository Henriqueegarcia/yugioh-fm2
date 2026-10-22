# CLAUDE.md — Yu-Gi-Oh! Forbidden Memories 2 (projeto pessoal)

Este repositório é um fork pessoal do
[Yu-Gi-Oh! Forbidden Memories Recompiled](https://github.com/Unchiga/Yu-Gi-Oh-Forbidden-Memories-Recompiled)
(decompilação 100% byte-exata do jogo de PS1, portada para PC). O objetivo é criar
uma versão "FM 2" para jogar offline, só na máquina do dono.

O plano completo, com fases e checklist, está em [`PLANO.md`](PLANO.md). Leia antes de começar
qualquer tarefa e atualize o checklist ao concluir etapas.

## Idioma

Converse com o usuário em **português do Brasil**. Código, nomes de arquivos de mod e
commits podem ficar em inglês (padrão do upstream); comentários explicativos para o
usuário em português.

## Ambiente

- Máquina principal: **Windows**, repositório em `C:\Users\henri\yugioh-fm2`.
- Build e execução: `.\play.bat` (baixa sozinho Python, llvm-mingw, CMake e Ninja na
  primeira vez, em `tmp\`). Também há build nativo para macOS (`notes/macos-build.md`).
- Imagem do disco (USA, SLUS-01411) fica em `game\` — **já validada** pelo SHA-256
  `6e22494a45bf50fa2d239cd3819a57163a5f9b91e0365babc3e101509b5c3a7c`.
- Saves, settings e mods do jogador ficam em `Documents\My Games\YFM Re-Decomp`.

## Regras do projeto (não quebrar nada)

1. **Nunca** commitar, copiar ou subir nada de `game\` (imagem do disco, arquivos
   extraídos, BIOS). É conteúdo da Konami; `/game/` já está no `.gitignore`.
   Também não commitar assets gerados a partir do disco (`tmp\pc\images\` etc.).
2. **Tudo como mod sempre que possível**, em `mods/fm2-<nome>/`. Preferir, nesta ordem:
   1. mod de dados (JSON, sem código) — cartas, fusões, drops, duelistas, packs;
   2. mod de código pela API de mods (`notes/modding.md`, seção "Code mods");
   3. só em último caso editar código do jogo/port em `src/` — e, nesse caso,
      isolar a mudança e explicar ao usuário antes.
3. Desenvolvimento no branch **`fm2`**. O `master` acompanha o upstream da Unchiga
   (remote `upstream`) para receber atualizações sem conflito.
4. Antes de dizer que algo está pronto: compilar, rodar o jogo e passar no
   **smoke test** do `PLANO.md`. Se não der para testar algo, dizer claramente.
5. Mudanças de balanceamento (ATK/DEF, drops, preços) seguem as regras de
   balanceamento do `PLANO.md` — nada de cartas que quebram a progressão.
6. Commits pequenos e descritivos; um assunto por commit.

## Documentação do upstream que mais importa

- `notes/modding.md` — guia geral de mods (manifesto, dados, código, o que um mod pode fazer).
- `notes/more-cards.md` — cartas novas (IDs após 722), efeitos, arte, como são ganhas.
- `notes/more-duelists.md` — duelistas novos: deck, drops, retrato, AI, condições de liberação.
- `notes/gameplay-tables.md` — fusões, equips, rituais, drops, decks.
- `notes/card-packs.md` — booster packs vendidos por StarChips.
- `notes/tower-mode.md` — sequência de duelos com história (útil para NPCs intermediários).
- `notes/mod-api-3.md` — API de mods em código.
- `notes/card-catalog.md` / `notes/card-catalog.csv` — catálogo das 722 cartas.
- `mods/` e `examples/mods/` — mods prontos para usar como referência.
