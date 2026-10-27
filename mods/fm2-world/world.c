/* FM 2 World - prova de conceito do mundo 2D.
 *
 * O botao WORLD do segundo menu do titulo leva a um modo proprio (o modo 13, o slot "developer" que a
 * Torre tambem usa; aqui um hook em Main_RunUnusedDeveloperMode cuida dele enquanto o mundo esta ligado).
 * O personagem anda por um mapa feito de retangulos (o overlay so desenha texto e retangulos), fala com os
 * NPCs do mod fm2-duelists e inicia o duelo como a Torre faz. Depois do duelo o jogo volta ao modo 13 e o
 * mundo continua de onde parou.
 *
 * Controles: direcionais andam, Cross fala/confirma, Circle sai/cancela.
 */
#include "types.h"
#include "pc/mods/modapi.h"

extern u8 D_8009B26C, D_8009B268, D_8009B26D, D_8009B368, D_8009B362, gDuel_bTerrain;
extern u16 gDuel_awPlayerDeck[];
extern void func_80024DC8(s32, s32, s32, s32);
extern void Fade_WaitIn(void);
extern void SD_BGMFadeOut(void);
extern void SD_BGMPlay(u32);
extern void SD_SEPlayFull(u32);
extern void Main_RunUnusedDeveloperMode(void);

#define WORLD_MODE 13           /* o slot do modo "developer" (a Torre usa o mesmo) */
#define WORLD_SELECTION 100     /* o numero que o botao devolve ao titulo e o SCENE reconhece */
#define SECOND_MENU 5
#define MAIN_MODE_MENU 8
#define WORLD_SONG 0x72D0

#define PAD_UP 0x0010u
#define PAD_RIGHT 0x0020u
#define PAD_DOWN 0x0040u
#define PAD_LEFT 0x0080u
#define PAD_CIRCLE 0x2000u
#define PAD_CROSS 0x4000u

#define MAPW 24
#define MAPH 15

/* # arvore, ~ agua (solidos), . grama, = trilha */
static const char *const MAP[MAPH] = {
    "########################",
    "#......................#",
    "#..##....~~~~.....##...#",
    "#..##....~~~~.....##...#",
    "#........~~~~..........#",
    "#......=======.........#",
    "#......=.....=.........#",
    "#..~~..=.....=....##...#",
    "#..~~..=.....=....##...#",
    "#......=======.........#",
    "#......................#",
    "#..##........~~.....#..#",
    "#..##........~~.....#..#",
    "#......................#",
    "########################",
};

typedef struct {
    const char *identity;   /* do fm2-duelists */
    const char *name;
    const char *line[3];
    int x, y;
    unsigned robe;          /* cor da roupa (a linha de cartas dele) */
} Npc;

#define EMBER 0xD9482Bu
#define TIDE 0x3F7FD9u
#define GROVE 0x4CAF50u
#define CRYPT 0x8E5CC4u
#define GOLD 0xE2B93Bu

static const Npc NPCS[] = {
    {"fm2-duelists:pip", "Pip", {"I only know the basic cards.", "Beat me and take a few!", ""}, 5, 11, GOLD},
    {"fm2-duelists:kael", "Kael", {"Embers make the best fuel.", "Show me your fire.", ""}, 6, 5, EMBER},
    {"fm2-duelists:marin", "Marin", {"The tide brings strange", "cards to my net.", ""}, 8, 4, TIDE},
    {"fm2-duelists:brenn", "Brenn", {"The grove remembers every", "duelist who walks through.", ""}, 3, 9, GROVE},
    {"fm2-duelists:morrow", "Morrow", {"The crypt is quiet.", "Let us not wake it.", ""}, 20, 13, CRYPT},
    {"fm2-duelists:hana", "Hana", {"Fire and leaves, a fine mix.", "Care to test it?", ""}, 14, 2, 0xC9B03Cu},
    {"fm2-duelists:ignis", "Ignis", {"Flames and bones, my specialty.", "", ""}, 19, 6, 0xB8506Eu},
    {"fm2-duelists:coral", "Coral", {"Water and wood. Calm, until", "the storm comes.", ""}, 12, 9, 0x3FA68Au},
    {"fm2-duelists:vesper", "Vesper", {"I have watched every line", "grow. Now, face them all.", ""}, 21, 2, 0xD8CFA0u},
    {"fm2-duelists:orin", "Orin", {"Few reach me.", "None have beaten me.", ""}, 17, 11, 0xE0443Eu},
};
#define NPC_COUNT ((int)(sizeof(NPCS) / sizeof(NPCS[0])))

static const MemoriesModHost *host;
static void *original;

/* Estado: sem ponteiros, so numeros. */
static int world_on;        /* o mundo esta ligado (modo 13 e dele) */
static int px = 3, py = 12, face = 2;   /* face: 0 cima, 1 direita, 2 baixo, 3 esquerda */
static int state;           /* 0 andando, 1 conversa, 2 aviso */
static int talking = -1;    /* NPC da conversa */
static int duel_npc = -1;   /* NPC do duelo em andamento, -1 se nenhum */
static char beaten[16];
static const char *notice_a = "", *notice_b = "";
static unsigned revision;   /* muda a cada coisa que o overlay precisa redesenhar */
static unsigned prev_pad;
static uint64_t last_move;

static int streq(const char *a, const char *b)
{
    while (*a && *a == *b) a++, b++;
    return *a == *b;
}

static int solid(int x, int y)
{
    char c;
    int i;
    if (x < 0 || y < 0 || x >= MAPW || y >= MAPH) return 1;
    c = MAP[y][x];
    if (c == '#' || c == '~') return 1;
    for (i = 0; i < NPC_COUNT; i++)
        if (NPCS[i].x == x && NPCS[i].y == y) return 1;
    return 0;
}

static int npc_at(int x, int y)
{
    int i;
    for (i = 0; i < NPC_COUNT; i++)
        if (NPCS[i].x == x && NPCS[i].y == y) return i;
    return -1;
}

static void show_notice(const char *a, const char *b)
{
    notice_a = a;
    notice_b = b;
    state = 2;
    revision++;
}

static void leave_world(void)
{
    SD_SEPlayFull(8);
    SD_BGMFadeOut();
    world_on = 0;
    state = 0;
    D_8009B268 = 1;
    D_8009B26D = SECOND_MENU;
    D_8009B26C = MAIN_MODE_MENU;
}

static void start_duel(int n)
{
    int id = host->duelist_id(host, NPCS[n].identity), i;
    if (id <= 0) {
        SD_SEPlayFull(9);
        show_notice("This duelist is not here.", "(fm2-duelists is off?)");
        return;
    }
    for (i = 0; i < 40; i++) {
        if (gDuel_awPlayerDeck[i] == 0) {
            SD_SEPlayFull(9);
            show_notice("Your deck needs 40 cards.", "Fix it in Build Deck first.");
            return;
        }
    }
    SD_SEPlayFull(0x30);
    SD_BGMFadeOut();
    duel_npc = n;
    state = 0;
    func_80024DC8(-1, id, 0x6000, 0x6000);   /* a Torre arma o duelo assim */
    gDuel_bTerrain = 0;
    D_8009B368 = WORLD_MODE;                 /* o duelo acaba voltando aqui */
    if (host->log_enabled(host)) host->log(host, "world: duel against %s (duelist %d)", NPCS[n].name, id);
}

static void try_move(int dx, int dy)
{
    if (!solid(px + dx, py + dy)) {
        px += dx;
        py += dy;
    }
}

static void update(void)
{
    unsigned pad = host->pad(host, 0), pressed = pad & ~prev_pad;
    prev_pad = pad;
    if (state == 0) {
        int dx = 0, dy = 0, dir = -1;
        if (pad & PAD_UP) { dy = -1; dir = 0; }
        else if (pad & PAD_DOWN) { dy = 1; dir = 2; }
        else if (pad & PAD_LEFT) { dx = -1; dir = 3; }
        else if (pad & PAD_RIGHT) { dx = 1; dir = 1; }
        if (dir >= 0) {
            uint64_t now = host->now_us(host);
            if (face != dir) { face = dir; revision++; }
            if (now - last_move > 130000u) {
                last_move = now;
                try_move(dx, dy);
                revision++;
            }
        }
        if (pressed & PAD_CROSS) {
            static const int fx[4] = {0, 1, 0, -1}, fy[4] = {-1, 0, 1, 0};
            int n = npc_at(px + fx[face], py + fy[face]);
            if (n >= 0) {
                talking = n;
                state = 1;
                SD_SEPlayFull(0x30);
                revision++;
            }
        } else if (pressed & PAD_CIRCLE) {
            leave_world();
        }
    } else if (state == 1) {
        if (pressed & PAD_CROSS) start_duel(talking);
        else if (pressed & PAD_CIRCLE) { state = 0; SD_SEPlayFull(8); revision++; }
    } else if (pressed & (PAD_CROSS | PAD_CIRCLE)) {
        state = 0;
        SD_SEPlayFull(8);
        revision++;
    }
}

/* O runner do modo 13: do mundo enquanto ele esta ligado, da Torre (o original) nos outros casos. */
static void runner(void)
{
    if (!world_on) {
        ((void (*)(void))original)();
        return;
    }
    if ((D_8009B26C & 0x40) == 0) {
        D_8009B26C |= 0x40;
        prev_pad = 0xFFFFu;   /* o botao que abriu o mundo nao conta */
        SD_BGMPlay(WORLD_SONG);
        if (duel_npc >= 0) {
            int won = D_8009B362 == 0;
            if (won) beaten[duel_npc] = 1;
            if (host->log_enabled(host)) host->log(host, "world: back from %s, %s", NPCS[duel_npc].name, won ? "won" : "lost");
            duel_npc = -1;
            if (won) show_notice("You won!", "Check your new cards.");
            else show_notice("You lost...", "Train and try again.");
        }
        revision++;
        Fade_WaitIn();
        return;
    }
    update();
}

/* ---- desenho ---- */

static void tile_color(char c, int x, int y, unsigned *base, unsigned *dark)
{
    unsigned v = (unsigned)(x * 7 + y * 13) % 5;
    if (c == '#') { *base = 0x2F6B34u; *dark = 0x1D4A22u; }
    else if (c == '~') { *base = 0x2F6FB8u; *dark = 0x5A93D6u; }
    else if (c == '=') { *base = 0xCDB07Au; *dark = 0xB79A66u; }
    else { *base = v == 0 ? 0x5DAA4Au : 0x66B352u; *dark = 0x4F9540u; }
}

static void draw_world(void)
{
    int w, h, sc, ts, ox, oy, x, y, i, small;
    host->overlay_size(host, &w, &h, &sc);
    if (w <= 0 || h <= 0) return;
    small = sc > 1 ? sc / 2 : 1;
    ts = w / MAPW;
    if (h / (MAPH + 4) < ts) ts = h / (MAPH + 4);
    if (ts < 8) ts = 8;
    ox = (w - MAPW * ts) / 2;
    oy = (h - MAPH * ts) / 2;
    host->fill(host, 0, 0, w, h, 0x0E1A12u, 255);
    for (y = 0; y < MAPH; y++) {
        for (x = 0; x < MAPW; x++) {
            unsigned base, dark;
            int tx = ox + x * ts, ty = oy + y * ts, q = ts / 4;
            char c = MAP[y][x];
            tile_color(c, x, y, &base, &dark);
            host->fill(host, tx, ty, ts, ts, base, 255);
            if (c == '#') {   /* copa e tronco */
                host->fill(host, tx + q / 2, ty + q / 2, ts - q, ts - q - q / 2, dark, 255);
                host->fill(host, tx + q, ty + q, ts - 2 * q, q, base, 255);
                host->fill(host, tx + ts / 2 - q / 2, ty + ts - q, q, q, 0x5B3A1Eu, 255);
            } else if (c == '~') {
                host->fill(host, tx + q, ty + q, ts / 2, q / 2 + 1, dark, 255);
                host->fill(host, tx + q * 2, ty + q * 3, ts / 2, q / 2 + 1, dark, 255);
            } else if (c == '.') {
                host->fill(host, tx + q, ty + q * 2, q / 2 + 1, q / 2 + 1, dark, 255);
            }
        }
    }
    for (i = 0; i < NPC_COUNT; i++) {   /* NPCs */
        int tx = ox + NPCS[i].x * ts, ty = oy + NPCS[i].y * ts, q = ts / 8;
        host->fill(host, tx + 2 * q, ty + 6 * q, 4 * q, 2 * q, 0x00000000u, 70);          /* sombra */
        host->fill(host, tx + 2 * q, ty + 3 * q, 4 * q, 4 * q, NPCS[i].robe, 255);          /* roupa */
        host->fill(host, tx + 2 * q, ty + q, 4 * q, 3 * q, 0xF2CFA0u, 255);                  /* cabeca */
        host->fill(host, tx + 2 * q, ty + q, 4 * q, q, NPCS[i].robe, 255);                   /* capuz */
        host->fill(host, tx + 3 * q, ty + 2 * q, q / 2 + 1, q / 2 + 1, 0x201810u, 255);
        host->fill(host, tx + 5 * q, ty + 2 * q, q / 2 + 1, q / 2 + 1, 0x201810u, 255);
        if (beaten[i]) host->fill(host, tx + 6 * q, ty, 2 * q, 2 * q, 0xFFD54Au, 255);       /* estrela: vencido */
        {
            int tw = host->text_width(host, NPCS[i].name, small);
            host->draw_text(host, tx + ts / 2 - tw / 2, ty - 8 * small, NPCS[i].name, 0xFFFFFFu, small);
        }
    }
    {   /* o personagem */
        int tx = ox + px * ts, ty = oy + py * ts, q = ts / 8;
        host->fill(host, tx + 2 * q, ty + 6 * q, 4 * q, 2 * q, 0x00000000u, 70);
        host->fill(host, tx + 2 * q, ty + 3 * q, 4 * q, 4 * q, 0xF0F0F0u, 255);             /* casaco */
        host->fill(host, tx + 2 * q, ty + 3 * q, 4 * q, q, 0x2060C0u, 255);                  /* cachecol */
        host->fill(host, tx + 2 * q, ty + q, 4 * q, 3 * q, 0xF2CFA0u, 255);                  /* cabeca */
        host->fill(host, tx + 2 * q, ty, 4 * q, 2 * q, 0x5A3A22u, 255);                      /* cabelo */
        if (face == 2 || face == 1 || face == 3) {
            int ex = face == 3 ? 2 : face == 1 ? 4 : 3;
            host->fill(host, tx + ex * q, ty + 2 * q, q / 2 + 1, q / 2 + 1, 0x201810u, 255);
            if (face == 2) host->fill(host, tx + 5 * q, ty + 2 * q, q / 2 + 1, q / 2 + 1, 0x201810u, 255);
        }
    }
    host->draw_text(host, ox, oy - 14 * sc, "FM 2 WORLD", 0xFFE08Au, sc);
    host->draw_text(host, ox + MAPW * ts - host->text_width(host, "Cross: talk   Circle: exit", small),
                    oy - 14 * sc, "Cross: talk   Circle: exit", 0xC8D8C0u, small);
    if (state == 1) {   /* conversa */
        const Npc *n = &NPCS[talking];
        int bw = MAPW * ts - 4 * ts, bh = 6 * ts, bx = ox + 2 * ts, by = oy + (MAPH - 7) * ts;
        host->fill(host, bx - 4, by - 4, bw + 8, bh + 8, 0xF0E6C8u, 255);
        host->fill(host, bx, by, bw, bh, 0x1B2A3Au, 255);
        host->draw_text(host, bx + ts / 2, by + ts / 2, n->name, n->robe | 0x404040u, sc);
        host->draw_text(host, bx + ts / 2, by + ts + ts / 2, n->line[0], 0xFFFFFFu, small);
        host->draw_text(host, bx + ts / 2, by + 2 * ts + ts / 4, n->line[1], 0xFFFFFFu, small);
        host->draw_text(host, bx + ts / 2, by + bh - ts / 2, beaten[talking] ? "Cross: duel again   Circle: leave" : "Cross: duel   Circle: leave",
                        0xFFE08Au, small);
    } else if (state == 2) {
        int bw = 12 * ts, bh = 3 * ts, bx = (w - bw) / 2, by = (h - bh) / 2;
        host->fill(host, bx - 4, by - 4, bw + 8, bh + 8, 0xF0E6C8u, 255);
        host->fill(host, bx, by, bw, bh, 0x1B2A3Au, 255);
        host->draw_text(host, bx + ts / 2, by + ts / 2 + 4, notice_a, 0xFFFFFFu, small + (sc > 1 ? 1 : 0));
        host->draw_text(host, bx + ts / 2, by + 2 * ts, notice_b, 0xC8D8C0u, small);
    }
}

static int showing(void)
{
    return world_on && (D_8009B26C & 0x5F) == (0x40 | WORLD_MODE);
}

static void overlay(void)
{
    if (showing()) draw_world();
}

static unsigned overlay_signature(void)
{
    return showing() ? revision * 2 + 1 : 0;
}

/* ---- eventos ---- */

static void on_menu(MemoriesModEvent *e)
{
    const char *name;
    if (e->phase != MEMORIES_BEFORE) return;
    name = host->menu_item(host, e->a);
    if (name && streq(name, "fm2-world:world")) {
        e->handled = 1;
        e->result = WORLD_SELECTION;   /* o titulo desliza para fora e chama o SCENE com este numero */
    }
}

static void on_scene(MemoriesModEvent *e)
{
    if (e->phase != MEMORIES_BEFORE || e->a != WORLD_SELECTION) return;
    e->handled = 1;
    world_on = 1;
    state = 0;
    D_8009B268 = 1;
    D_8009B26C = WORLD_MODE;           /* sem o 0x40: o runner comeca pela inicializacao */
    revision++;
    if (host->log_enabled(host)) host->log(host, "world: entered");
}

static void applied(int on)
{
    if (!on) world_on = 0;
}

static void reset(void)
{
    world_on = 0;      /* um save state foi carregado: o mundo se desliga */
    duel_npc = -1;
}

int MemoriesModInit(const MemoriesModHost *from, MemoriesMod *mod)
{
    if (from->api < 9) return 0;
    host = from;
    mod->api = 9;
    mod->applied = applied;
    mod->reset = reset;
    mod->overlay = overlay;
    mod->overlay_signature = overlay_signature;
    if (!host->subscribe(host, MEMORIES_EVENT_MENU, 0, on_menu)) return 0;
    if (!host->subscribe(host, MEMORIES_EVENT_SCENE, 0, on_scene)) return 0;
    return host->hook(host, (void *)Main_RunUnusedDeveloperMode, (void *)runner, &original) != 0;
}
