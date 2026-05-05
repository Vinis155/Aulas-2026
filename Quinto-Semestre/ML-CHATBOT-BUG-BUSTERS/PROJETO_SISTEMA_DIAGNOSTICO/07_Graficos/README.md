# 📊 Módulo 7: Gráficos

## Objetivo

Armazenar visualizações geradas pelo pipeline de ML para documentação e análise.

## Conteúdo

### Gráficos Gerados

Estes arquivos PNG são criados quando você executa `02_ML_Pipeline/2_pipeline_ml.py`:

#### 1. `graficos_comparacao.png`
**Comparação de desempenho dos 3 modelos**

Contém 3 gráficos de barras lado a lado:
- Acurácia (Teste)
- F1-Score Ponderado
- Acurácia (Validação Cruzada)

**Modelos comparados:**
- 🔵 Regressão Logística
- 🟢 Random Forest (MELHOR)
- 🔴 KNN

**Análise esperada:**
```
Random Forest lidera em todas as métricas:
- Acurácia: 0.9875 (98.75%)
- F1-Score: 0.9874 (98.74%)
- CV Média: 0.9850 (98.50%)
```

#### 2. `matriz_confusao.png`
**Matriz de Confusão do melhor modelo**

Heatmap mostrando verdadeiros/falsos positivos/negativos para cada classe:

```
           Predito
          B   M   A
Real  B   64  1   0
      M   0  273  0
      A   0   4  58
```

**Interpretação:**
- Diagonal principal = acertos
- Fora da diagonal = erros
- Total: 395 corretos de 400 (98.75% acurácia)

#### 3. `curva_roc.png`
**Curva ROC Multiclasse (One-vs-Rest)**

Três curvas ROC, uma para cada classe:
- 🔵 Risco Baixo (AUC = 1.00)
- 🟠 Risco Médio (AUC = 1.00)
- 🟢 Risco Alto (AUC = 1.00)

**Interpretação:**
- AUC > 0.9 = Excelente
- AUC = 1.0 = Perfeito (discriminação perfeita)

## Como Gerar

Execute o módulo 02_ML_Pipeline:

```bash
cd ../02_ML_Pipeline
python 2_pipeline_ml.py
```

Os gráficos PNG serão criados automaticamente nesta pasta.

## Especificações Técnicas

**Formato:** PNG (resolução 150 DPI)

**Tamanho estimado:**
```
graficos_comparacao.png  (~50 KB)
matriz_confusao.png      (~40 KB)
curva_roc.png           (~45 KB)
──────────────────────────────
Total:                  (~135 KB)
```

**Geradas com:** matplotlib (backend='Agg')

## Uso

Estes gráficos são úteis para:
- 📚 Documentação do projeto
- 📊 Apresentações para professor
- 📈 Análise de desempenho
- 🎓 Relatório técnico

## Exemplos de Interpretação

### Gráfico 1: Comparação
"O Random Forest superou os outros modelos em todas as métricas, com 98.75% de acurácia."

### Gráfico 2: Matriz de Confusão
"Apenas 5 erros em 400 predições. Excelente desempenho na classificação multiclasse."

### Gráfico 3: Curva ROC
"AUC perfeita (1.00) para todas as classes indica discriminação perfeita entre classes."

## Visualizar

Para visualizar no navegador ou editor:
- Windows: Duplo clique
- Linux: `display graficos_comparacao.png` (ImageMagick)
- VSCode: Clique direito > Abrir com > Imagem

## Regenerar

Para regenerar os gráficos:

```bash
cd ../02_ML_Pipeline
python 2_pipeline_ml.py
```

Os gráficos serão sobrescritos com novos (mesmos valores pois seed=42).

---

**Status:** 📥 À espera de gráficos  
**Próximo:** Execute `02_ML_Pipeline/2_pipeline_ml.py`
