# 📦 Módulo 5: Dados

## Objetivo

Armazenar o dataset gerado para treino do modelo.

## Conteúdo

### `pacientes.csv` (será gerado)

Dataset com 2000 registros de pacientes

**Estrutura:**
```
nome,idade,glicose,pressao,imc,colesterol,risco
Ana,45,98.5,120.3,22.4,185.0,0
Bruno,63,148.0,155.0,31.5,248.0,2
...
```

## Como Gerar

Execute o módulo 01_Dataset:

```bash
cd ../01_Dataset
python 1_gerar_dataset.py
```

O arquivo `pacientes.csv` será criado automaticamente nesta pasta.

## Estrutura do Dataset

| Coluna | Tipo | Intervalo | Descrição |
|--------|------|-----------|-----------|
| nome | string | - | Nome fictício |
| idade | int | 18-99 | Anos |
| glicose | float | 60-350 | mg/dL |
| pressao | float | 80-220 | mmHg |
| imc | float | 15-55 | kg/m² |
| colesterol | float | 100-400 | mg/dL |
| **risco** | **int** | **0/1/2** | **Classe alvo** |

## Distribuição de Classes

```
Risco Baixo (0):   ~325 registros (16.2%)
Risco Médio (1):  ~1367 registros (68.3%)
Risco Alto (2):    ~308 registros (15.4%)
```

## Uso

Este dataset é usado por:
- **02_ML_Pipeline:** Para treinar os modelos

## Notas

- ✅ Dataset é reprodutível (seed=42)
- ✅ Distribuições seguem padrões clínicos realistas
- ✅ Sem valores ausentes (missing values)

---

**Status:** 📥 À espera de dados  
**Próximo:** Execute `01_Dataset/1_gerar_dataset.py`
