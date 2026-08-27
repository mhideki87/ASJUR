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
MAX_TOOLS = 3          # decide nos primeiros tool_use; skill invocada depois disso é tardia demais
TIMEOUT = 180

def uma_rodada(query):
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    cmd = ["claude", "-p", query, "--output-format", "stream-json", "--verbose",
           "--model", "claude-opus-5", "--max-turns", "3"]
    try:
        p = subprocess.run(cmd, cwd=CWD, env=env, capture_output=True,
                           timeout=TIMEOUT, text=True)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    vistos = []
    for linha in p.stdout.splitlines():
        try: e = json.loads(linha)
        except json.JSONDecodeError: continue
        if e.get("type") != "assistant": continue
        for c in e.get("message", {}).get("content", []):
            if c.get("type") != "tool_use": continue
            nome, inp = c.get("name",""), c.get("input", {}) or {}
            if nome == "Skill" and SLUG in str(inp.get("skill","")):
                return True, "Skill"
            if nome == "Read" and SLUG in str(inp.get("file_path","")):
                return True, "Read"
            vistos.append(nome)
            if len(vistos) >= MAX_TOOLS:
                return False, ",".join(vistos)
    return False, ",".join(vistos) or "só texto"

def avaliar(item):
    resultados = [uma_rodada(item["query"]) for _ in range(RUNS)]
    disparos = [r[0] for r in resultados]
    validos = [d for d in disparos if d is not None]
    taxa = sum(validos)/len(validos) if validos else 0.0
    acertou = (taxa >= 0.5) == item["should_trigger"]
    return {**item, "taxa": taxa, "acertou": acertou,
            "detalhe": [r[1] for r in resultados]}

evals = json.load(open(EVALSET))
with ThreadPoolExecutor(max_workers=6) as ex:
    saida = list(ex.map(avaliar, evals))

acertos = sum(1 for r in saida if r["acertou"])
print(json.dumps({"acertos": acertos, "total": len(saida), "resultados": saida},
                 ensure_ascii=False, indent=1))
print(f"\n=== {acertos}/{len(saida)} corretos ===", file=sys.stderr)
for r in saida:
    esp = "DISPARAR" if r["should_trigger"] else "NÃO disp"
    print(f"{'OK  ' if r['acertou'] else 'FALHA'} esp={esp} taxa={r['taxa']:.2f} "
          f"[{'|'.join(r['detalhe'])}] {r['query'][:60]}", file=sys.stderr)
