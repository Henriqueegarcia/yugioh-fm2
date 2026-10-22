# FM 2 — Pesquisa da Fase 1 (cartas e fusões novas)

Resultado da pesquisa que alimenta as regras de balanceamento do `PLANO.md`.
Os números vêm dos dados do jogo (`notes/card-catalog.csv` e
`notes/research/fusion-and-drop-tables/`), não de estimativa.

## 1. O que o motor permite (e o que não)

Fonte: `notes/more-cards.md`, `notes/gameplay-tables.md`.

- Carta nova = **cópia** de uma carta original (`"copy"`), IDs de 723 até 32766.
  Nome, texto, arte, ATK/DEF, tipo, nível, atributo e guardian stars são próprios.
- **Modelo 3D e efeito** vêm da carta-base, a não ser que o mod aponte outros
  (`"model"`, `"effect"`). Não dá para criar modelo 3D novo.
- **Efeitos de monstro** por dados (sem código): até 8 por carta, com gatilhos
  `summon`, `flip`, `draw`, `combat`, `destroyed`, `destroy_opponent`, `face_up`
  e ações `magic`, `boost`, `heal`, `damage`, `destroy`.
- **Magias/armadilhas novas** por dados: `card_effects` (`damage`, `heal`, `boost`,
  `destroy`). A IA só joga uma magia nova se ela tiver `ai_effect` apontando para
  uma carta original equivalente.
- **Fusões**: `{"with": [A, B], "result": C}` em qualquer mod; a IA usa as mesmas
  regras do jogador. Também há `fusions` dentro da própria carta nova.
- **Drops e decks**: pesos de 0 a 2048 por oponente e por pool (`pow`, `bcd`, `tec`,
  `decks`). Carta nova pode entrar direto no pool. Alternativa: `"drops": true`
  na carta, que divide o peso da carta-base entre a base e as cópias.
- **Arte**: PNG próprio (102x96, ou 408x384 para HD). Sem `art`, a carta mostra a
  arte da base — serve como provisória.
- **Starter decks e passwords** são do disco: carta nova não aparece em starter
  deck, e por padrão custa 999999 starchips na loja de passwords.
- Alterar o balanceamento global também é possível sem código: teto de ATK/DEF,
  LP inicial, bônus de equip e de terreno (`examples/mods/community-rules`).

## 2. A base original em números

621 monstros. ATK por faixa:

| Faixa de ATK | Monstros | DEF média |
|---|---|---|
| 0–500 | 66 | 628 |
| 501–1000 | 194 | 877 |
| 1001–1500 | 180 | 1171 |
| 1501–2000 | 122 | 1541 |
| 2001–2500 | 38 | 1926 |
| 2501–3000 | 16 | 2325 |
| 3001+ | 5 | 2940 |

ATK por nível (mínimo / mediana / máximo): nível 3 → 0/900/1600; nível 4 →
500/1300/2200; nível 5 → 0/1605/2100; nível 6 → 1450/2000/2500; nível 7 →
1600/2400/2800; nível 8 → 2450/2850/3500.

Observações:
- O jogo é dominado por monstros de 500–2000 ATK (496 de 621). O topo
  (2500+) tem só 21 cartas, quase todas de fusão ou de chefe.
- Fusão gera 204 resultados distintos, com mediana de 3 receitas por resultado.
  Alguns resultados têm centenas de receitas (Nekogal #2: 1200; Mystical Sand: 1174;
  Cyber Soldier: 1008), por isso **uma receita nova para um resultado já comum
  quase não muda o jogo**, e uma receita para um resultado raro muda bastante.

## 3. Força dos duelistas (deck dealt, ATK médio ponderado pelo peso)

| Fase da campanha | Duelistas (exemplos) | ATK médio do deck |
|---|---|---|
| Início | Teana 222, Villager 1 263, Simon 303, Jono 326, Seto 444 | 200–450 |
| Começo-meio | Rex Raptor 643, Shadi 522, Villager 2/3 ~800–880 | 500–900 |
| Meio | Weevil 995, Mai 1160, Bakura 1208, Kaiba 1439 | 1000–1450 |
| Fim | High Mages 1100–1450, Seto 2nd 1382, Heishin 2nd 1184, Seto 3rd 1867 | 1100–1900 |
| Chefões finais | Heishin 1804, Nitemare 2419 | 1800–2400 |

Os drops têm ATK médio de 300 a 1500 e sobem bem mais devagar que os decks: o
jogo dá cartas **mais fracas** do que as que o oponente usa. O melhor peso
individual num pool fica na faixa de 30 a 250 em 2048 (1,5% a 12%).
(A ordem real dos duelos na campanha fica para a Fase 2.)

## 4. Referências da comunidade

Só consegui páginas de download e resumos, sem changelog. Tratar como pista,
não como fonte:

- **FM Mod 15** (arukadopsx): mantém as 722 cartas; separa raridade por cor,
  muda passwords e preços, novos starter decks, decks e drops de oponentes
  retrabalhados, campanha mais difícil, mais fusões, cor de carta roxa.
- **FM Arrange** (ZetaPhoenix Projects): 436 cartas, mais de 300 novas, mais de 250
  fusões, 5 cartas por duelo, mais de 10 chefes obtidos por fusão. A planilha de
  fusões no Google Sheets citada pelo mod é a referência mais completa.
- **YGO FM Rebalanced** (ShootingStarD): objetivo de manter o espírito do original
  e tornar mais suportáveis o farm e o fim sem cheats; refaz equips (BLS usa a
  Legendary Sword; B. Skull Dragon usa os equips do Summoned Skull); tem planilha
  de plano de drops. A página não detalha ATK/DEF.

Lições que valem para o FM 2:
1. Mods bem recebidos mexem em **drops e decks junto com as cartas**, não só
   adicionam cartas.
2. Aumentar quantidade de drops por duelo ou reduzir o grind é pedido comum;
   isso pode ficar para a Fase 3 (loja/economia).
3. Equips e fusões de chefe dão "momentos" ao jogador sem inflar ATK bruto.

## 5. Regras de balanceamento propostas

Estão em `PLANO.md` (seção "Regras de balanceamento") e esperam a sua validação.
Resumo da lógica: tiers por faixa de ATK ligados aos degraus de dificuldade dos
duelistas, limites por nível calculados da base original, efeitos pequenos e
drops novos sempre com peso baixo.

## 6. Pendências para fechar a Fase 1

- Validar as regras de balanceamento com o usuário.
- Escolher o primeiro lote de ~10 cartas: conceito, tier, tipo, base (cópia de
  qual carta original, por causa do modelo 3D e do efeito) e fusões.
- Decidir a arte provisória (reaproveitar a da base ou gerar PNG simples).
