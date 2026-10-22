#!/usr/bin/env python3
"""Verificador de balanceamento dos mods fm2-* (regras do PLANO.md).

Le mods/fm2-*/mod.json + notes/card-catalog.csv e confere, para cada carta e
receita nova:
  - ATK/DEF validos, ATK dentro do tier (tag "tierN") e coerente com o nivel;
  - efeitos de monstro dentro dos limites do tier;
  - fusoes: resultado <= tier dos materiais + 1; resultado melhor que os materiais;
    ciclos; duas receitas diferentes para o mesmo par;
  - receitas herdadas da carta-base que passam do teto do tier (devem estar bloqueadas);
  - LIMITE DE CARTAS: quantas cartas do baralho a receita exige (custo em cadeia).
    No FM a fusao em duelo e uma cadeia: cartas da mao (5) e/ou um monstro do campo;
    dois monstros do campo nao se fundem e o resultado nao vai para a colecao. Entao:
      * custo em cadeia por tier: T2<=2, T3<=3, T4<=4, T5<=6 (MAX_CHAIN);
      * nenhuma carta pode ser exigida mais de 3 vezes (limite de copias do baralho);
      * receita com as duas entradas sendo fusoes exige uma delas como carta real no
        baralho (ela precisa ter drop): vira aviso.

Rodar da raiz do repo:  python tools/fm2/check_balance.py   (sai com 1 se houver erro)
"""
import collections
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

TIER_ATK = {1: 1000, 2: 1500, 3: 2000, 4: 2500, 5: 3000}
MAX_CHAIN = {1: 1, 2: 2, 3: 3, 4: 4, 5: 6}   # cartas do baralho por receita, por tier do resultado
DECK_COPIES = 3
HAND_SIZE = 5
NON_MONSTER = ("Magic", "Trap", "Ritual", "Equip")


def tier_of_atk(atk):
    for t in (1, 2, 3, 4):
        if atk <= TIER_ATK[t]:
            return t
    return 5


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def load_catalog():
    path = ROOT / "notes" / "card-catalog.csv"
    return {int(r["id"]): r for r in csv.DictReader(open(path, encoding="utf-8"))}


def load_retail_recipes():
    path = ROOT / "notes" / "research" / "fusion-and-drop-tables" / "fusions.csv"
    rec = collections.defaultdict(list)
    for f in csv.DictReader(open(path, encoding="utf-8")):
        a, b, r = int(f["material_a_id"]), int(f["material_b_id"]), int(f["result_id"])
        rec[a].append((b, r))
        if a != b:
            rec[b].append((a, r))
    return rec


def level_stats(cat):
    by = collections.defaultdict(list)
    for x in cat.values():
        if x["type"] not in NON_MONSTER:
            by[int(x["level"])].append(int(x["attack"]))
    out = {}
    for lv, v in by.items():
        v.sort()
        n = len(v)
        out[lv] = (v[0], v[n // 4], v[(3 * n) // 4], v[-1], n)
    return out


def load_mods():
    mods = []
    for path in sorted((ROOT / "mods").glob("fm2-*/mod.json")):
        d = json.loads(path.read_text(encoding="utf-8"))
        if d.get("cards"):
            mods.append(d)
    return mods


def main():
    rep = Report()
    cat = load_catalog()
    retail_rec = load_retail_recipes()
    lv = level_stats(cat)
    mods = load_mods()
    if not mods:
        print("nenhum mods/fm2-*/mod.json com cartas")
        return 1

    cards = {}          # identidade -> dados
    nulls = set()       # (identidade, parceiro) bloqueados
    recipes = []        # (a, b, resultado) com resultado nao nulo
    pair_result = {}

    def ident(mod, c):
        return f"{mod['id']}:{c['id']}:1"

    for mod in mods:
        for c in mod["cards"]:
            i = ident(mod, c)
            if i in cards:
                rep.err(f"{i}: identidade duplicada")
            cards[i] = c
    ids = set(cards)

    def key(x):
        return x if isinstance(x, int) else str(x)

    def retail(x):
        return isinstance(x, int)

    # ---------- cartas ----------
    for i, c in cards.items():
        tier = next((int(t[4:]) for t in c.get("tags", []) if t.startswith("tier") and t[4:].isdigit()), None)
        c["_tier"] = tier
        if tier is None:
            rep.err(f"{i}: falta a tag \"tierN\" (1 a 5)")
            continue
        atk, dfs = c.get("attack"), c.get("defense")
        base = cat.get(c["copy"]) if isinstance(c.get("copy"), int) else None
        if base is None:
            rep.err(f"{i}: \"copy\" precisa ser o numero de uma carta original")
            continue
        if atk is None or dfs is None:
            rep.err(f"{i}: faltam attack/defense")
            continue
        if atk % 10 or dfs % 10 or not (0 <= atk <= 5110 and 0 <= dfs <= 5110):
            rep.err(f"{i}: ATK/DEF devem ser multiplos de 10 entre 0 e 5110 ({atk}/{dfs})")
        if atk > TIER_ATK[tier]:
            rep.err(f"{i}: ATK {atk} acima do maximo do tier {tier} ({TIER_ATK[tier]})")
        level = c.get("level")
        if level in lv:
            mn, q1, q3, mx, n = lv[level]
            if atk > mx:
                rep.err(f"{i}: ATK {atk} acima do maior ATK original de nivel {level} ({mx})")
            elif atk > q3 or atk < q1:
                rep.warn(f"{i}: ATK {atk} fora da faixa tipica do nivel {level} ({q1}-{q3})")
        # efeitos
        effects = c.get("monster_effects", [])
        if len(effects) > (1 if tier <= 2 else 2):
            rep.err(f"{i}: {len(effects)} efeitos demais para o tier {tier}")
        for e in effects:
            do = e.get("do")
            if do == "boost":
                cap = 300 if tier <= 2 else 500
                for k in ("attack", "defense"):
                    if abs(e.get(k, 0)) > cap:
                        rep.err(f"{i}: boost de {k} {e[k]} acima de {cap} no tier {tier}")
            elif do in ("damage", "heal"):
                cap = 500 if tier <= 2 else 1000
                if e.get("amount", 0) > cap:
                    rep.err(f"{i}: {do} {e['amount']} acima de {cap} no tier {tier}")
            elif do in ("destroy", "magic") and tier < 4:
                rep.err(f"{i}: efeito \"{do}\" so a partir do tier 4")
        if not c.get("art"):
            rep.warn(f"{i}: sem arte propria")
        if c.get("drops", True):
            rep.warn(f"{i}: \"drops\" ligado entra no drop da carta-base; use false ate decidir os drops")

    # ---------- fusoes: regras e bloqueios ----------
    for mod in mods:
        for f in mod.get("fusions", []):
            a, b = f["with"]
            if f.get("result") is None:
                nulls.add((key(a), key(b)))
                nulls.add((key(b), key(a)))
                continue
            r = f["result"]
            recipes.append((a, b, r))
            pair = frozenset((key(a), key(b)))
            if pair in pair_result and pair_result[pair] != key(r):
                rep.err(f"par {sorted(pair)}: dois resultados diferentes")
            pair_result[pair] = key(r)

    def tier_of(x):
        if retail(x):
            row = cat.get(x)
            if row is None:
                rep.err(f"carta original {x} nao existe")
                return 1
            return tier_of_atk(int(row["attack"])) if row["type"] not in NON_MONSTER else 1
        return cards[x]["_tier"] if x in cards and cards[x].get("_tier") else 1

    def atk_of(x):
        if retail(x):
            row = cat.get(x)
            return int(row["attack"]) if row and row["type"] not in NON_MONSTER else 0
        return cards[x].get("attack", 0) if x in cards else 0

    def name_of(x):
        if retail(x):
            return f"{cat[x]['name']}({x})" if x in cat else str(x)
        return cards[x]["name"] if x in cards else x

    for a, b, r in recipes:
        for x in (a, b, r):
            if not retail(x) and x not in ids:
                rep.err(f"receita {a} + {b} -> {r}: carta {x} nao existe nos mods")
        if r not in ids and not retail(r):
            continue
        ta, tb, tr = tier_of(a), tier_of(b), tier_of(r)
        label = f"{name_of(a)} + {name_of(b)} -> {name_of(r)}"
        if tr > max(ta, tb) + 1:
            rep.err(f"{label}: tier {tr} acima do maximo dos materiais ({max(ta, tb)}) + 1")
        if atk_of(r) <= max(atk_of(a), atk_of(b)):
            rep.warn(f"{label}: resultado ({atk_of(r)} ATK) nao supera os materiais")

    # ---------- receitas herdadas da carta-base ----------
    for i, c in cards.items():
        tier = c.get("_tier")
        if not tier or not isinstance(c.get("copy"), int):
            continue
        ceiling = TIER_ATK[min(tier + 1, 5)]
        leaks = [(p, res) for p, res in retail_rec.get(c["copy"], [])
                 if cat.get(res) and cat[res]["type"] not in NON_MONSTER
                 and int(cat[res]["attack"]) > ceiling and (i, p) not in nulls]
        if leaks:
            p, res = leaks[0]
            rep.err(f"{i}: {len(leaks)} receita(s) herdada(s) da base passam de {ceiling} ATK sem bloqueio "
                    f"(ex.: + {cat[p]['name']} -> {cat[res]['name']})")

    # ---------- limite de cartas (custo em cadeia) ----------
    made = collections.defaultdict(list)
    for a, b, r in recipes:
        made[key(r)].append((a, b))

    state = {}

    def cost(x, stack=()):
        """(custo, Counter de cartas, avisos) da forma mais barata de ter x em duelo."""
        k = key(x)
        if k in stack:
            rep.err(f"ciclo de fusao em {name_of(x)}")
            return 99, collections.Counter({k: 99}), []
        if k in state:
            return state[k]
        if k not in made:
            return 1, collections.Counter({k: 1}), []
        best = None
        for a, b in made[k]:
            ca, la, wa = cost(a, stack + (k,))
            cb, lb, wb = cost(b, stack + (k,))
            a_prod, b_prod = key(a) in made, key(b) in made
            if a_prod and b_prod:
                # as duas sao fusoes: uma delas precisa ser carta real no baralho
                options = [(ca + 1, la + collections.Counter({key(b): 1}), wa + [f"{name_of(b)} como carta real"]),
                           (cb + 1, lb + collections.Counter({key(a): 1}), wb + [f"{name_of(a)} como carta real"])]
                opt = min(options, key=lambda o: (o[0], max(o[1].values())))
            else:
                opt = (ca + cb, la + lb, wa + wb)
            if best is None or (opt[0], max(opt[1].values())) < (best[0], max(best[1].values())):
                best = opt
        state[k] = best
        return best

    for i, c in cards.items():
        if i not in made or not c.get("_tier"):
            continue
        n, leaves, owned = cost(i)
        cap = MAX_CHAIN[c["_tier"]]
        names = ", ".join(f"{name_of(k)} x{v}" if v > 1 else name_of(k) for k, v in leaves.items())
        if n > cap:
            rep.err(f"{c['name']}: precisa de {n} cartas do baralho ({names}); maximo do tier {c['_tier']} e {cap}")
        if n > HAND_SIZE:
            rep.warn(f"{c['name']}: {n} cartas > mao de {HAND_SIZE}: so em varios turnos, mantendo a fusao no campo")
        for k, v in leaves.items():
            if v > DECK_COPIES:
                rep.err(f"{c['name']}: exige {v} copias de {name_of(k)} (limite do baralho: {DECK_COPIES})")
        for o in owned:
            rep.warn(f"{c['name']}: a receita exige {o}; ela precisa ter drop ou deck de duelista")
        print(f"  {c['name']:24} T{c['_tier']}  {n} carta(s): {names}")

    print()
    for w in rep.warnings:
        print("AVISO", w)
    for e in rep.errors:
        print("ERRO ", e)
    print(f"\n{len(cards)} cartas, {len(recipes)} receitas, {len(nulls) // 2} bloqueios: "
          f"{len(rep.errors)} erro(s), {len(rep.warnings)} aviso(s)")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main())
