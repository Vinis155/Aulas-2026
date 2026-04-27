"""
=============================================================================
BLOCO 1 — GERADOR DE DATASET SINTÉTICO
=============================================================================
Projeto  : Sistema de Previsão de Risco Clínico
Arquivo  : 1_gerar_dataset.py
Saída    : pacientes.csv
 
Variáveis geradas:
    nome        → nome fictício simples (sem sobrenome)
    idade       → 18 a 99 anos
    glicose     → mg/dL (glicemia de jejum)
    pressao     → mmHg  (pressão arterial sistólica)
    imc         → kg/m² (índice de massa corporal)
    colesterol  → mg/dL (colesterol total)
    risco       → 0 = baixo | 1 = médio | 2 = alto
 
Regra de classificação de risco (baseada em critérios clínicos reais):
    Cada variável fora da faixa saudável soma +1 ponto de risco.
    Pontuação 0       → classe 0 (baixo risco)
    Pontuação 1 ou 2  → classe 1 (risco médio)
    Pontuação 3 a 5   → classe 2 (alto risco)
=============================================================================
"""
 
import numpy as np
import pandas as pd
 
# ── Semente: garante que o mesmo dataset seja gerado toda vez ────────────────
np.random.seed(42)
 
N = 2000   # Total de registros a gerar
 
# ── 1. NOMES FICTÍCIOS ───────────────────────────────────────────────────────
nomes_pool = [
    "Ana", "Bruno", "Carla", "Diego", "Elena", "Fabio", "Gisele", "Hugo",
    "Iris", "Joao", "Karen", "Lucas", "Mariana", "Nelson", "Olga", "Paulo",
    "Quenia", "Rafael", "Sara", "Tiago", "Ursula", "Vitor", "Wanda", "Xenia",
    "Yago", "Zara", "Bento", "Clarice", "Davi", "Estela", "Felipe", "Gabi",
    "Henrique", "Isadora", "Julio", "Lais", "Marcos", "Nina", "Oscar",
    "Patricia", "Rodrigo", "Simone", "Thales", "Valentina", "William",
    "Andreia", "Cesar", "Debora", "Eduardo", "Fernanda"
]
 
nomes = np.random.choice(nomes_pool, size=N, replace=True)
 
# ── 2. IDADE (anos) ──────────────────────────────────────────────────────────
idade = np.random.randint(18, 100, size=N)
 
# ── 3. GLICOSE mg/dL ─────────────────────────────────────────────────────────
# Normal < 100 | Pre-diabetes 100-125 | Diabetes >= 126
glicose = np.random.normal(loc=105, scale=30, size=N).clip(60, 350).round(1)
 
# ── 4. PRESSAO ARTERIAL SISTOLICA mmHg ──────────────────────────────────────
# Otima < 120 | Normal 120-129 | Hipertensao >= 130
pressao = np.random.normal(loc=125, scale=22, size=N).clip(80, 220).round(1)
 
# ── 5. IMC kg/m2 ─────────────────────────────────────────────────────────────
# Normal 18.5-24.9 | Sobrepeso 25-29.9 | Obesidade >= 30
imc = np.random.normal(loc=27, scale=5, size=N).clip(15, 55).round(1)
 
# ── 6. COLESTEROL TOTAL mg/dL ────────────────────────────────────────────────
# Desejavel < 200 | Limitrofe 200-239 | Alto >= 240
colesterol = np.random.normal(loc=210, scale=40, size=N).clip(100, 400).round(1)
 
# ── 7. REGRA DE CLASSIFICACAO DE RISCO ──────────────────────────────────────
# Cada criterio soma +1 ponto de risco:
#   glicose  >= 126  → diabetes
#   pressao  >= 140  → hipertensao estagio 2
#   imc      >= 30   → obesidade
#   colesterol >= 240 → colesterol alto
#   idade    >= 60   → fator etario
 
pontos = (
    (glicose    >= 126).astype(int) +
    (pressao    >= 140).astype(int) +
    (imc        >= 30 ).astype(int) +
    (colesterol >= 240).astype(int) +
    (idade      >= 60 ).astype(int)
)
 
risco = np.where(pontos == 0, 0,
        np.where(pontos <= 2, 1, 2))
 
# ── 8. DATAFRAME ──────────────────────────────────────────────────────────────
df = pd.DataFrame({
    "nome"      : nomes,
    "idade"     : idade,
    "glicose"   : glicose,
    "pressao"   : pressao,
    "imc"       : imc,
    "colesterol": colesterol,
    "risco"     : risco
})
 
# ── 9. RELATORIO ──────────────────────────────────────────────────────────────
print("=" * 58)
print("   GERADOR DE DATASET — RISCO CLINICO")
print("=" * 58)
print(f"  Registros gerados : {len(df)}")
print()
print("  Distribuicao das classes de risco:")
for cls, label in zip([0, 1, 2], ["Baixo", "Medio", "Alto "]):
    qtd = (df["risco"] == cls).sum()
    pct = qtd / N * 100
    barra = "#" * int(pct / 2)
    print(f"    Classe {cls} ({label}): {qtd:5d}  {pct:5.1f}%  {barra}")
 
print()
print("  Estatisticas das variaveis:")
print(df.drop(columns=["nome","risco"]).describe().round(2).to_string())
 
# ── 10. EXPORTACAO ────────────────────────────────────────────────────────────
df.to_csv("pacientes.csv", index=False, encoding="utf-8")
print()
print("  Arquivo 'pacientes.csv' salvo com sucesso.")
print("=" * 58)
 