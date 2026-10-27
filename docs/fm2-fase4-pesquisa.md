# FM 2 - Fase 4: pesquisa do mundo 2D (27/10/2026)

## O que um mod de código consegue

- Compilar: `tools/pc/build_mod.py <pasta>` funciona com o llvm-mingw já baixado em
  `tmp/pc/tools/llvm-mingw/.../bin` (pôr essa pasta no PATH).
- Entrar no mundo: botão novo no menu do título (`menu.buttons` com `action: "event"` + evento `MENU`).
- Ler o controle: `host->pad` e o evento `INPUT` (que também permite zerar os botões para o jogo não reagir).
- Desenhar: overlay com **só texto e retângulos** (`draw_text`, `fill`); sem imagens. Só redesenha quando
  `overlay_signature` muda.
- Iniciar um duelo: como a Torre faz (`src/pc/tower/tower_screen.c`, `step_duel`): `func_80024DC8(-1, duelista, 0x6000, 0x6000)`,
  terreno em `gDuel_bTerrain` e modo de retorno em `D_8009B368`. Vitória lida em `D_8009B362 == 0`.
- Salvar progresso próprio: `open_data` + eventos `SLOT_SAVE`/`SLOT_LOAD` (arquivo por save).
- Duelistas por identidade: `host->duelist_id("fm2-duelists:kael")`.

## Limites

- Sem desenho de imagens no overlay: arte do mapa teria de virar retângulos (pixel art convertida em
  listas de retângulos, gerada por script) ou o port precisaria de uma tela própria em `src/pc/` (como a Torre).
- Voltar do duelo para o mundo exige capturar o retorno do modo do jogo (hook em `Main_ApplyMenuSelection`/evento `SCENE`).
