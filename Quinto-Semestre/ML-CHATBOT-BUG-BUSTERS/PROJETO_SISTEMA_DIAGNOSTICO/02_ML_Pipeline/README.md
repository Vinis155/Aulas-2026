# 🧠 Módulo 2: Pipeline de Machine Learning

## Objetivo

Treinar múltiplos modelos de ML no dataset, comparar desempenho, selecionar o melhor e salvá-lo para uso em produção.

## Arquivo

- **`2_pipeline_ml.py`** - Pipeline completo de ML

## Como Usar

```bash
cd 02_ML_Pipeline
python 2_pipeline_ml.py
```

## Pré-requisitos

- ✅ Dataset gerado (execute `01_Dataset/1_gerar_dataset.py` primeiro)
- ✅ Arquivo `../05_Dados/pacientes.csv` existente

## Saídas

O script gera:

### Arquivos de Modelo (em `../06_Modelos/`):
```
melhor_modelo.pkl      → Modelo Random Forest serializado
scaler.pkl             → StandardScaler para normalização
metadados_modelo.pkl   → Informações do modelo
```

### Gráficos (em `../07_Graficos/`):
```
graficos_comparacao.png  → 3 gráficos comparando acurácia dos modelos
matriz_confusao.png      → Matriz de confusão do melhor modelo
curva_roc.png            → Curva ROC multiclasse
```

## Processo (10 Etapas)

### Etapa 1: Leitura do Dataset
- Carrega `pacientes.csv`
- Verifica integridade
- Exibe distribuição de classes

### Etapa 2: Separação Features/Target
- Features (X): idade, glicose, pressão, IMC, colesterol
- Target (y): risco (0/1/2)

### Etapa 3: Divisão Treino/Teste
- 80% treino (1600 amostras)
- 20% teste (400 amostras)
- Mantém proporção de classes (stratified)

### Etapa 4: Normalização
- StandardScaler normaliza cada feature
- Média = 0, Desvio = 1
- Essencial para modelos sensíveis à escala

### Etapa 5: Treinamento de 3 Modelos
1. **Logistic Regression**
   - Modelo linear
   - Baseline simples
   - Fácil interpretação

2. **Random Forest** ⭐ (Melhor)
   - Ensemble de árvores
   - Robusto a outliers
   - Alta acurácia

3. **KNN (K-Nearest Neighbors)**
   - Lazy learner
   - Basado em distância
   - Sensível à normalização

### Etapa 6: Avaliação de Métricas
Para cada modelo:
- **Acurácia** - % de acertos
- **Precision** - De quem disse positivo, quantos eram?
- **Recall** - De quem era positivo, quantos acertou?
- **F1-Score** - Média harmônica entre precision e recall

### Etapa 7: Validação Cruzada (k-fold)
- Divide dados em 5 partes
- Treina/testa em cada combinação
- Mais confiável que divisão única

### Etapa 8: Seleção do Melhor Modelo
- Ranking por F1-Score
- Escolhe o melhor (Random Forest)
- Exibe comparativo

### Etapa 9: Visualizações
- **Gráfico 1:** Comparação de acurácia dos 3 modelos
- **Gráfico 2:** Matriz de confusão do melhor modelo
- **Gráfico 3:** Curva ROC multiclasse

### Etapa 10: Predição de Teste
- Simula novo paciente (exemplo: Fernanda)
- Mostra resultado da predição
- Exibe probabilidades por classe

### Etapa 11: Salvar Modelo (⭐ Crítico para API)
- Serializa modelo com joblib
- Salva scaler para normalização futura
- Salva metadados para documentação

## Resultados Esperados

```
RANKING (por F1-Score ponderado):

1. Random Forest       F1=0.9874  Acurácia=0.9875  ⭐ MELHOR
2. KNN                F1=0.8708  Acurácia=0.8750
3. Regressão Logística F1=0.7489  Acurácia=0.7625

>>> MELHOR MODELO: Random Forest <<<

Validação Cruzada (5-fold):
Random Forest:  98.50% ± 0.72%
```

## Matriz de Confusão (Random Forest)

```
Classe Real  │ Predito B │ Predito M │ Predito A
─────────────┼──────────┼──────────┼──────────
Baixo (0)    │    64    │    1     │    0
Médio (1)    │    0     │   273    │    0
Alto (2)     │    0     │    4     │   58

Acurácia: 98.75% (395/400 acertos)
```

## Curva ROC

```
AUC Scores (One-vs-Rest):
- Risco Baixo (0):   AUC = 1.00 ✅ Perfeito
- Risco Médio (1):   AUC = 1.00 ✅ Perfeito
- Risco Alto (2):    AUC = 1.00 ✅ Perfeito
```

## Arquivos Gerados

```
📦 06_Modelos/
├── melhor_modelo.pkl        (Random Forest treinado)
├── scaler.pkl               (Normalizador)
└── metadados_modelo.pkl     (Info do modelo)

📊 07_Graficos/
├── graficos_comparacao.png  (3 gráficos)
├── matriz_confusao.png      (Matriz)
└── curva_roc.png           (Curva ROC)
```

## Próximo Passo

Após executar este script:

1. ✅ Arquivos `.pkl` estarão prontos para a **API (03_API)**
2. ✅ Gráficos PNG estarão prontos para **documentação**
3. ➡️ Execute o módulo **03_API** para expor o modelo

## Notas Técnicas

- Todas as operações usam `random_state=42` para reprodutibilidade
- StandardScaler é ajustado APENAS no treino (evita data leakage)
- Validação cruzada usa StratifiedKFold para manter proporções de classe
- Gráficos são salvos como PNG (sem abrir janelas)

---

**Status:** ✅ Pronto para usar  
**Data:** 27/04/2026  
**Modelo Recomendado:** Random Forest (98.75% acurácia)
