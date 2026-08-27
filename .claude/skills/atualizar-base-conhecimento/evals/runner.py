#!/usr/bin/env python3
"""Testa se a skill atualizar-base-conhecimento dispara para cada query.

Roda `claude -p <query>` numa cópia isolada do repositório e observa se, entre os
primeiros tool_use da resposta, há uma chamada Skill/Read à skill. Diferente do
run_eval.py do skill-creator, casa pelo nome REAL da skill instalada no projeto.
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

SLUG = "atualizar-base-conhecimento"
CWD = sys.argv[1]
EVALSET = sys.argv[2]
RUNS = int(sys.argv[3]) if len(sys.argv) > 3 else 3
MAX_TURNS = "6"        # limita o custo de cada rodada
TIMEOUT = 240

def uma_rodada(query):
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    cmd = ["claude", "-p", query, "--output-format", "stream-json", "--verbose",
           "--model", "claude-opus-5", "--max-turns", MAX_TURNS]
    try:
        p = subprocess.run(cmd, cwd=CWD, env=env, capture_output=True,
                           timeout=TIMEOUT, text=True)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    # Varre a sessão inteira: disparo tardio, depois de o Claude investigar o repo, ainda é disparo —
    # o que importa é a consolidação acontecer. Registra em que posição veio, para medir a demora.
    vistos, ok = [], False
    for linha in p.stdout.splitlines():
        try: e = json.loads(linha)
        except json.JSONDecodeError: continue
        if e.get("type") == "result":
            ok = not e.get("is_error") and e.get("subtype") == "success"
        if e.get("type") != "assistant": continue
        for c in e.get("message", {}).get("content", []):
            if c.get("type") != "tool_use": continue
            nome, inp = c.get("name",""), c.get("input", {}) or {}
            alvo = (nome == "Skill" and SLUG in str(inp.get("skill",""))) or \
                   (nome == "Read" and SLUG in str(inp.get("file_path","")))
            if alvo:
                return True, f"disparou no tool #{len(vistos)+1}"
            vistos.append(nome)
    if not ok and not vistos:
        return None, "sessão vazia/erro"   # não conta: é falha de execução, não de gatilho
    return False, f"{len(vistos)} tools, sem disparo"

def avaliar(item):
    # Sessão que volta vazia (erro de execução, contenção de API) não é sinal de gatilho:
    # repete até RUNS rodadas válidas, com teto para não rodar para sempre.
    resultados, tentativas = [], 0
    while sum(1 for r in resultados if r[0] is not None) < RUNS and tentativas < RUNS * 3:
        resultados.append(uma_rodada(item["query"])); tentativas += 1
    disparos = [r[0] for r in resultados]
    validos = [d for d in disparos if d is not None]
    taxa = sum(validos)/len(validos) if validos else 0.0
    acertou = (taxa >= 0.5) == item["should_trigger"]
    return {**item, "taxa": taxa, "acertou": acertou,
            "detalhe": [r[1] for r in resultados]}

evals = json.load(open(EVALSET))
with ThreadPoolExecutor(max_workers=3) as ex:
    saida = list(ex.map(avaliar, evals))

acertos = sum(1 for r in saida if r["acertou"])
print(json.dumps({"acertos": acertos, "total": len(saida), "resultados": saida},
                 ensure_ascii=False, indent=1))
print(f"\n=== {acertos}/{len(saida)} corretos ===", file=sys.stderr)
for r in saida:
    esp = "DISPARAR" if r["should_trigger"] else "NÃO disp"
    print(f"{'OK  ' if r['acertou'] else 'FALHA'} esp={esp} taxa={r['taxa']:.2f} "
          f"[{'|'.join(r['detalhe'])}] {r['query'][:60]}", file=sys.stderr)
