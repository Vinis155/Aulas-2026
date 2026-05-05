# 📊 Módulo 1: Gerador de Dataset

## Objetivo

Gerar um dataset sintético de 2000 pacientes com dados biomédicos realistas para treinamento do modelo de ML.

## Arquivo

- **`1_gerar_dataset.py`** - Gerador de dataset

## Como Usar

```bash
cd 01_Dataset
python 1_gerar_dataset.py
```

## Saída

O script gera:
- **`../05_Dados/pacientes.csv`** - Dataset com 2000 registros

## Estrutura do Dataset

| Coluna | Tipo | Intervalo | Descrição |
|--------|------|-----------|-----------|
| nome | string | - | Nome fictício do paciente |
| idade | int | 18-99 | Idade em anos |
| glicose | float | 60-350 | Glicose em mg/dL |
| pressao | float | 80-220 | Pressão arterial sistólica em mmHg |
| imc | float | 15-55 | Índice de Massa Corporal em kg/m² |
| colesterol | float | 100-400 | Colesterol total em mg/dL |
| **risco** | **int** | **0/1/2** | **Classe alvo (0=Baixo, 1=Médio, 2=Alto)** |

## Distribuição de Classes

```
Classe 0 (Baixo):   ~325 registros (16.2%)
Classe 1 (Médio):  ~1367 registros (68.3%)
Classe 2 (Alto):    ~308 registros (15.4%)
```

## Regra de Classificação de Risco

Cada critério clínico fora dos limites normais soma +1 ponto:

- ✅ Glicose ≥ 126 → Diabetes
- ✅ Pressão ≥ 140 → Hipertensão Estágio 2
- ✅ IMC ≥ 30 → Obesidade
- ✅ Colesterol ≥ 240 → Colesterol Alto
- ✅ Idade ≥ 60 → Fator Etário

**Classificação Final:**
- 0 pontos → Risco **Baixo** (classe 0)
- 1-2 pontos → Risco **Médio** (classe 1)
- 3+ pontos → Risco **Alto** (classe 2)

## Exemplo de Output

```
============================================================
   GERADOR DE DATASET — RISCO CLINICO
============================================================
  Registros gerados : 2000

  Distribuicao das classes de risco:
    Classe 0 (Baixo):  325  16.2%  ########
    Classe 1 (Medio):  1367 68.3%  ##################################
    Classe 2 (Alto ):  308  15.4%  #######

  Estatisticas das variaveis:
                idade    glicose    pressao        imc  colesterol
        count  2000.00   2000.00   2000.00   2000.00     2000.00
        mean     57.75    106.03    125.30    27.05      209.87
        ...

  Arquivo '../05_Dados/pacientes.csv' salvo com sucesso.
============================================================
```

## Notas Importantes

- ✅ Seed = 42 garante que os dados sejam sempre iguais (reprodutibilidade)
- ✅ Distribuições seguem padrões clínicos realistas
- ✅ Dataset pronto para o próximo módulo (ML Pipeline)

## Próximo Passo

Após executar este script, execute o módulo **02_ML_Pipeline** para treinar os modelos.

---

**Status:** ✅ Pronto para usar  
**Data:** 27/04/2026
