# FM 2 - Fase 3: loja de packs

Mod `mods/fm2-shop/` (gerado por `tools/fm2/gen_shop.py`; edite o script, não o JSON).
Na tela de Password, **△ abre os packs**. Cada vitória rende mais StarChips (`limits.starchip_prize`):
S 10, A 8, B 5, C 3, D 2 (original: 5, 4, 3, 2, 1).

| Pack | Preço | Cartas | Conteúdo | Limite |
|---|---|---|---|---|
| Ember / Tide / Grove / Crypt **Seeds** | 25 | 5 | 85% T1, 15% T2 da linha | máx. 3 cópias de cada carta |
| Ember / Tide / Grove / Crypt **Forge** | 90 | 4 | 80% T2, 19% T3, 1% T4; pity: T3 a cada 6 packs | idem |
| **Hybrid Crate** | 150 | 3 | T3 de todas as linhas e híbridas; 10% Bone Dragon Overlord (T4) | idem |
| **Legend Chest** | 400 | 2 | T4 de todas as linhas, sem repetir no pack | 5 compras por save |

As T5 (Solar Phoenix Dragon, Mangrove Leviathan, Infernal Lich Drake) **não** estão em nenhum pack: só por fusão.
`max_copies: 3` impede o pack de dar mais cópias do que o baralho aceita; quando você já tem tudo, o pack mostra ALL OWNED.

## Liberações

`USE_GATES = False` (modo de teste): todos os packs abertos desde o início. Com `True`:
Forge abre ao vencer o NPC da linha (Kael, Marin, Brenn, Morrow), Hybrid Crate ao vencer Coral,
Legend Chest ao vencer Orin e abrir 10 packs. Packs trancados aparecem como ??????.

## O que ainda é palpite

Preços e a média de StarChips por vitória precisam ser calibrados jogando.
Ainda não feito (extra, exige código): comprar carta específica, vender e trocar.
