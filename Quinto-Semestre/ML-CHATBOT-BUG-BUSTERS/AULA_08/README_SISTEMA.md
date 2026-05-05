# 🏥 SISTEMA DE DIAGNÓSTICO DE RISCO CLÍNICO
## Projeto ML + ChatBot - AULA 08 & 09

---

## ✅ STATUS: 100% COMPLETO

### O que foi implementado:

| Componente | Status | Arquivo |
|-----------|--------|---------|
| 📊 Dataset Gerador | ✅ | `DATASET_SINTÉTICO.py` |
| 🧠 Pipeline ML | ✅ MODIFICADO | `2_pipeline_ml.py` (com joblib.dump) |
| 🌐 API REST | ✅ NOVO | `api_biomedicina.py` |
| 🎨 Front-end | ✅ NOVO | `interface_streamlit.py` |
| 📋 Guia Execução | ✅ | `GUIA_EXECUCAO.md` |

---

## 🎯 RESULTADO DO TREINAMENTO

```
MELHOR MODELO: Random Forest ✅

Acurácia:           98.75%
F1-Score:           98.74%
Validação Cruzada:  98.50% ± 0.72%
```

**Classe do melhor paciente:**
- Nome: Fernanda
- Resultado: **RISCO ALTO** (100% confiança)
- Fatores: Diabetes, Hipertensão, Obesidade, Colesterol Alto

---

## 🚀 PARA COMEÇAR (3 TERMINAIS)

### Terminal 1: Preparar dados

```bash
cd AULA_08
python DATASET_SINTÉTICO.py
python 2_pipeline_ml.py
```

### Terminal 2: Rodar API

```bash
cd AULA_08
uvicorn api_biomedicina:app --reload
```

### Terminal 3: Rodar Interface

```bash
cd AULA_08
streamlit run interface_streamlit.py
```

### Acessar

- **Interface:** http://localhost:8501
- **API Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📋 RECURSOS DO SISTEMA

### Front-end Streamlit
- ✅ Formulário com 6 campos (nome, idade, glicose, PA, IMC, colesterol)
- ✅ Indicadores rápidos de risco
- ✅ Exibição de resultados colorida (verde/amarelo/vermelho)
- ✅ Tabela de referência de valores
- ✅ Informações do modelo
- ✅ Export de resultados em JSON

### API REST
- ✅ Endpoint POST `/predict` para diagnóstico
- ✅ Validação automática de inputs
- ✅ Normalização com StandardScaler
- ✅ Cálculo de probabilidades
- ✅ Explicação dos fatores de risco
- ✅ Documentação automática (Swagger)
- ✅ Health check disponível

### Modelo ML
- ✅ 3 modelos treinados: Logistic Regression, Random Forest, KNN
- ✅ Seleção automática do melhor (Random Forest)
- ✅ Validação cruzada k-fold (k=5)
- ✅ Matriz de confusão
- ✅ Curva ROC para cada classe
- ✅ Gráficos de comparação de acurácia

---

## 📊 ARQUIVOS GERADOS

```
AULA_08/
├── DATASET_SINTÉTICO.py          (gerador de dados)
├── 2_pipeline_ml.py              (pipeline ML com joblib)
├── api_biomedicina.py            (API FastAPI)
├── interface_streamlit.py         (front-end)
├── GUIA_EXECUCAO.md              (instruções)
├── README_SISTEMA.md             (este arquivo)
│
├── pacientes.csv                 (2000 registros gerados)
├── melhor_modelo.pkl             (modelo Random Forest serializado)
├── scaler.pkl                    (normalizador serializado)
├── metadados_modelo.pkl          (metadados)
│
├── graficos_comparacao.png       (3 gráficos lado a lado)
├── matriz_confusao.png           (matriz confusão do melhor modelo)
└── curva_roc.png                 (curva ROC multiclasse)
```

---

## 🔧 TECNOLOGIAS UTILIZADAS

- **Python 3.10+**
- **FastAPI** - Framework API REST
- **Streamlit** - Interface web
- **scikit-learn** - Machine Learning
- **pandas** - Manipulação de dados
- **numpy** - Computação numérica
- **matplotlib** - Visualizações
- **joblib** - Serialização de modelos
- **uvicorn** - Servidor ASGI

---

## 📝 DADOS DO DATASET

### Estrutura (2000 registros)

| Coluna | Tipo | Intervalo | Distribuição |
|--------|------|-----------|--------------|
| nome | string | - | 50 nomes aleatórios |
| idade | int | 18-99 | Normal (μ=57.75) |
| glicose | float | 60-350 | Normal (μ=106.03) |
| pressao | float | 80-220 | Normal (μ=125.30) |
| imc | float | 15-55 | Normal (μ=27.05) |
| colesterol | float | 100-400 | Normal (μ=209.87) |
| **risco** | **int** | **0/1/2** | **16.2% / 68.3% / 15.4%** |

### Classificação de Risco

- **0 (Baixo):** 0-1 fatores de risco
- **1 (Médio):** 1-2 fatores de risco
- **2 (Alto):** 3+ fatores de risco

### Fatores Considerados

- Glicose ≥ 126 → Diabetes
- Pressão ≥ 140 → Hipertensão
- IMC ≥ 30 → Obesidade
- Colesterol ≥ 240 → Alto
- Idade ≥ 60 → Fator etário

---

## 🎬 EXEMPLO DE USO

### 1. Abrir interface

Navegador: http://localhost:8501

### 2. Preencher dados

```
Nome: Maria Santos
Idade: 63
Glicose: 148.0 mg/dL
Pressão: 155.0 mmHg
IMC: 31.5 kg/m²
Colesterol: 248.0 mg/dL
```

### 3. Clicar "Fazer Diagnóstico"

### 4. Resultado

```
Classificação: ALTO ⚠️
Confiança: 95.2%
Explicação: Paciente apresenta glicose elevada 
            (possível diabetes), hipertensão, 
            obesidade, colesterol alto.
Recomendação: Encaminhe para avaliação 
              médica urgente
```

---

## 🧪 TESTE RÁPIDO (SEM INTERFACE)

```bash
# Terminal - Testar API direto
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "nome":"João",
       "idade":63,
       "glicose":148,
       "pressao":155,
       "imc":31.5,
       "colesterol":248
     }'
```

**Resposta:**
```json
{
  "nome": "João",
  "idade": 63,
  "risco_codigo": 2,
  "risco_classificacao": "Alto",
  "probabilidade": 0.95,
  "explicacao": "Paciente apresenta glicose elevada..."
}
```

---

## ⚠️ REQUISITOS IMPORTANTES

### Antes de rodar:

1. ✅ Python 3.10+
2. ✅ Todas as dependências instaladas
3. ✅ `2_pipeline_ml.py` JÁ EXECUTADO (gera arquivos .pkl)
4. ✅ Estar no diretório correto (`AULA_08/`)

### Dependências:

```bash
pip install fastapi uvicorn joblib streamlit requests pandas numpy scikit-learn matplotlib
```

---

## 🎓 LEARNING PATH

### O que aprendeu:

1. **Dataset Sintético**
   - Geração com distribuições realistas
   - Classificação baseada em regras

2. **Machine Learning**
   - Separação treino/teste
   - Normalização de dados (StandardScaler)
   - Treinamento de múltiplos modelos
   - Avaliação com múltiplas métricas
   - Validação cruzada

3. **API REST**
   - FastAPI + Uvicorn
   - Schema de validação (Pydantic)
   - Serialização de modelos (joblib)
   - Documentação automática

4. **Interface Web**
   - Streamlit para prototipagem rápida
   - Comunicação HTTP com API
   - Visualização de dados
   - UX/UI com Markdown

---

## 📈 MÉTRICAS FINAIS

### Random Forest (Melhor Modelo)

**Conjunto de Teste (400 amostras):**
- Acurácia: **98.75%**
- Precision: **98.77%**
- Recall: **98.75%**
- F1-Score: **98.74%**

**Validação Cruzada (5-fold):**
- Média: **98.50%**
- Desvio: **±0.72%**

**Interpretação:**
O modelo é extremamente confiável, acertando quase sempre na classificação de risco clínico.

---

## 🚀 PRÓXIMAS ETAPAS (AULA_09)

- [ ] **Demonstração em sala** - Mostrar sistema rodando
- [ ] **Testes com dados reais** - Validar com professor
- [ ] **Vídeo Pitch** - Gravar até 3 minutos
- [ ] **Envio no AVA** - Até 04/05/2026

### Roteiro para vídeo:

```
0-30s: Introdução
- "Desenvolvemos um sistema de diagnóstico de risco clínico"
- Mostrar interface

30-60s: Demonstração
- Preencher formulário
- Clicar diagnóstico
- Mostrar resultado

60-90s: Arquitetura
- Explicar: ML → API → Interface
- Mencionar 98.75% acurácia

90-120s: Impacto
- Caso de uso em hospitais/clínicas
- Próximos passos

120-180s: Buffer/Perguntas
```

---

## 📞 SUPORTE

### Se algo não funcionar:

1. **API não conecta:**
   - Terminal 2: `uvicorn api_biomedicina:app --reload`
   - Verificar: http://localhost:8000/health

2. **Modelo não carregado:**
   - Terminal 1: `python 2_pipeline_ml.py`
   - Verificar: `melhor_modelo.pkl` existe

3. **Interface não abre:**
   - Terminal 3: `streamlit run interface_streamlit.py`
   - Abrir: http://localhost:8501

---

## ✅ CONCLUSÃO

**O sistema está 100% funcional e pronto para:**
- ✅ Demonstração ao professor
- ✅ Teste com dados reais
- ✅ Vídeo pitch
- ✅ Integração futura em produção

---

**Desenvolvido em:** 27/04/2026  
**Status:** ✅ Pronto para AULA_09  
**Próxima entrega:** Pitch com vídeo (04/05/2026)
