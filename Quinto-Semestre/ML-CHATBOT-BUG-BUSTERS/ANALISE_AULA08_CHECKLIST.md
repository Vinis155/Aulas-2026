# 📋 ANÁLISE COMPLETA - AULA 08 (27/04/2026)
## Sprint-03 (AC-3) - 3ª ETAPA - Valor: 0,5 ponto

---

## 🎓 CONTEXTO DE APRENDIZADO (Aulas 2-8)

A disciplina segue uma progressão estruturada em Machine Learning e Chatbot:

| Aula | Período | Foco | Sprint | Status |
|------|---------|------|--------|--------|
| 02 | Fevereiro | Setup inicial (Git, venv, dependências) | Sprint-01 | ✅ Concluído |
| 03-04 | Março | Métricas ML, estatística (MAE, RMSE) | Sprint-02 | ✅ Concluído |
| 05 | Março | NLP: vetorização, frequência, limpeza texto | Sprint-02 | ✅ Concluído |
| 06 | Março | Chatbot Naive Bayes + Clusterização | Sprint-02 | ✅ Concluído |
| 07 | 06/04 | Documento Técnico + Arquitetura + UML | Sprint-03 (1ª) | ⏳ Pendente validação |
| 08 | 27/04 | **API ML + Dataset Biomedicina + Pipeline** | **Sprint-03 (3ª)** | **❌ INCOMPLETO** |
| 09 | Maio | Projeto Final Biomedicina | Sprint-03 (Entrega) | 📅 Próximo |

---

## 📊 ANÁLISE DETALHADA - O QUE DEVERIA TER SIDO FEITO

### **PARTE 1: DOCUMENTAÇÃO TÉCNICA DO PROJETO TECH** 
**Valor: 0,25 pontos**

#### 📋 Requerimentos:
- ✅ Arquivo em formato DOC ou Google Docs
- ✅ Contém:
  - Título do Projeto
  - Descrição do que está sendo construído (App/Game)
  - **Especificação Técnica Detalhada:**
    - Linguagem e versão (Python 3.10+)
    - Bibliotecas (pandas, scikit-learn, fastapi, etc.)
    - APIs utilizadas (ngrok, etc.)
    - Outros detalhes técnicos
- ✅ Enviado por email: `flavio.santarelli@pro.fecaf.com.br`

#### ❌ **FALTA COMPLETAMENTE**
- Nenhum arquivo encontrado
- Recomendação: **Criar imediatamente documento com especificação técnica do projeto**

---

### **PARTE 2 - SPRINT-03 (AC-3) - ATIVIDADE 1: API para ML**
**Valor: 0,15 pontos**

#### 📋 Requerimentos:
1. Executar arquivo `ml_api.txt` no Google Colab
2. Seguir passos para:
   - Treinar modelo simples (Pipeline TF-IDF + Logistic Regression)
   - Serializar com Joblib
   - Criar API FastAPI
   - Expor via ngrok
3. Documentar resultados na SPRINT-3 (GitHub Projects)

#### ✅ **ARQUIVO DISPONÍVEL:**
- `ml_api.txt` - Tutorial COMPLETO com todas as instruções

#### ❌ **FALTANDO:**
- Código Python gerado (api_chatbot.py ou similar)
- Evidência de execução no Colab
- Resultado/screenshot da API funcionando
- Documentação na SPRINT-3

#### 🔧 Próximos Passos:
```
1. Abrir Google Colab
2. Executar bloco a bloco do ml_api.txt
3. Gerar arquivo api_chatbot.py com código funcional
4. Testar API localmente ou via ngrok
5. Colocar evidência na SPRINT-3
```

---

### **PARTE 2 - SPRINT-03 (AC-3) - ATIVIDADE 2: Dataset + Algoritmo Biomedicina**
**Valor: 0,35 pontos** ⭐ **PRINCIPAL**

#### 📋 Requerimentos Detalhados:

**Etapa 1: Preparação**
- [ ] Baixar PDF do documento técnico criado na AULA_07
- [ ] Ter acesso a Claude.IA com conta Google

**Etapa 2: Configurar Claude como Especialista**
- [ ] Criar nova Skill "ASSISTENTE-ML" (seguir skill_claude.txt)
- [ ] Descrição: "Especialista em ML e Chatbots"
- [ ] Instruções: "Ajude a criar projetos de ML e Ciência de Dados"

**Etapa 3: Gerar Código via IA**
- [ ] Colocar prompt_biomedicina.txt na Skill do Claude
- [ ] Inserir arquivo PDF da especificação técnica
- [ ] IA vai gerar 3 códigos completos:
  1. Gerador de Dataset (2000 registros)
  2. Pipeline ML completo (treino, validação, métricas)
  3. Visualizações (gráficos comparativos)

**Etapa 4: Executar Gerador de Dataset**
- [ ] Rodar: `DATASET_SINTÉTICO.py`
- [ ] Saída esperada: `pacientes.csv` (2000 linhas)
- [ ] Arquivo CSV vai para o GitHub do grupo

**Etapa 5: Treinar Modelos**
- [ ] Rodar: `2_pipeline_ml.py`
- [ ] Entrada: `pacientes.csv`
- [ ] Saídas esperadas:
  - `graficos_comparacao.png` (acurácia 3 modelos)
  - `matriz_confusao.png` (melhor modelo)
  - `curva_roc.png` (curva ROC multiclasse)
  - Print em console com métricas

**Etapa 6: Documentar Resultados**
- [ ] Colocar CSV no GitHub do grupo
- [ ] Colocar códigos Python no repositório
- [ ] Colocar RESULTADOS (print console + gráficos) na SPRINT-3

**Etapa 7: Validação**
- [ ] Chamar professor para validar tudo em sala

#### ✅ **ARQUIVOS JÁ DISPONÍVEIS:**
```
✅ ml_api.txt                    → Tutorial API
✅ skill_claude.txt              → Instruções Skill
✅ prompt_biomedicina.txt        → Prompt completo (prompt excelente)
✅ DATASET_SINTÉTICO.py          → Gerador dataset (pronto para usar)
✅ 2_pipeline_ml.py              → Pipeline ML (pronto para usar)
```

#### ❌ **FALTANDO EXECUTAR / GERAR:**
```
❌ pacientes.csv                 → Não foi gerado ainda
❌ 1_gerador_dataset.py          → (IA vai gerar - cópia melhorada)
❌ 3_algoritmo_biomedicina.py    → (IA vai gerar - código final)
❌ graficos_comparacao.png       → Não foi gerado
❌ matriz_confusao.png           → Não foi gerado
❌ curva_roc.png                 → Não foi gerado
❌ api_biomedicina.py            → Não foi implementado
❌ documento_resultados.txt      → Não foi criado
```

#### ⚠️ **Variáveis do Dataset a Gerar:**
```
✅ Nome (fictícios)
✅ Idade (18-99 anos)
✅ Glicose (mg/dL)
✅ Pressão arterial (mmHg)
✅ IMC (kg/m²)
✅ Colesterol (mg/dL)
✅ Risco (0=baixo, 1=médio, 2=alto)
```

#### ⚙️ **Modelos a Treinar:**
```
✅ Regressão Logística
✅ Random Forest
✅ KNN (K-Nearest Neighbors)
```

#### 📈 **Métricas Esperadas:**
```
✅ Acurácia
✅ Precision
✅ Recall
✅ F1-score
✅ Validação Cruzada (K-fold, k=5)
✅ Matriz de Confusão
✅ Curva ROC
```

---

## 🎯 CHECKLIST DE COMPLETUDE

### ✅ Entregáveis Concluídos:
- [x] Arquivo ml_api.txt com tutorial completo
- [x] Arquivo skill_claude.txt com instruções
- [x] Arquivo prompt_biomedicina.txt com prompt detalhado
- [x] DATASET_SINTÉTICO.py pronto para execução
- [x] 2_pipeline_ml.py pronto para execução

### ❌ Entregáveis Pendentes:

#### **CRÍTICO (0-48h):**
1. [ ] **Documentação Técnica TECH** - DOC com especificação (PARTE 1)
   - Status: ❌ NÃO INICIADO
   - Prazo: URGENTE
   
2. [ ] **Executar DATASET_SINTÉTICO.py**
   - Status: ❌ NÃO EXECUTADO
   - Esperado: pacientes.csv (2000 linhas)
   - Tempo: ~2 min
   
3. [ ] **Executar 2_pipeline_ml.py**
   - Status: ❌ NÃO EXECUTADO
   - Esperado: 3 gráficos PNG + console metrics
   - Tempo: ~5-10 min

#### **IMPORTANTE (dentro de 1 semana):**
4. [ ] **API com FastAPI** - Implementar código da atividade 1
   - Status: ❌ NÃO INICIADO
   - Arquivo esperado: api_chatbot.py
   
5. [ ] **Documentar Resultados** - Arquivo markdown com print/gráficos
   - Status: ❌ NÃO INICIADO
   - Arquivo esperado: RESULTADOS_AULA08.md

6. [ ] **Validação com Professor** - Chamar prof em sala para validar
   - Status: ❌ NÃO FEITO

---

## 📁 ESTRUTURA ESPERADA FINAL

```
ML-CHATBOT-BUG-BUSTERS/
├── AULA_08/
│   ├── 📄 Roteiro_Aula08
│   ├── 📝 ml_api.txt                    ✅
│   ├── 📝 skill_claude.txt              ✅
│   ├── 📝 prompt_biomedicina.txt        ✅
│   ├── 🐍 DATASET_SINTÉTICO.py          ✅
│   ├── 🐍 2_pipeline_ml.py              ✅
│   ├── 🐍 api_biomedicina.py            ❌ (gerar)
│   ├── 📊 pacientes.csv                 ❌ (gerar)
│   ├── 📊 graficos_comparacao.png       ❌ (gerar)
│   ├── 📊 matriz_confusao.png           ❌ (gerar)
│   ├── 📊 curva_roc.png                 ❌ (gerar)
│   └── 📄 RESULTADOS_AULA08.md          ❌ (criar)
│
├── GitHub (grupo):
│   ├── pacientes.csv                    ❌ (enviar)
│   ├── 2_pipeline_ml.py                 ❌ (enviar)
│   └── api_biomedicina.py               ❌ (enviar)
│
└── Email professor:
    └── TECH_SPEC_[PROJETO].docx         ❌ (enviar)
```

---

## 🚀 PLANO DE AÇÃO RECOMENDADO

### **Fase 1: Executar Scripts Existentes (30 min)**
```python
# 1. Gerar dataset
python DATASET_SINTÉTICO.py
# → Cria: pacientes.csv

# 2. Treinar modelos
python 2_pipeline_ml.py
# → Cria: PNG com gráficos + print métricas
```

### **Fase 2: Documentar (20 min)**
```markdown
# Criar arquivo: RESULTADOS_AULA08.md
- Copiar print da execução do 2_pipeline_ml.py
- Descrever os 3 modelos treinados
- Inserir print das métricas
- Inserir as 3 imagens PNG geradas
- Análise: qual modelo foi melhor?
```

### **Fase 3: Implementar API (1-2 horas)**
```python
# Criar: api_biomedicina.py
# Baseado em ml_api.txt
# - Treinar modelo em pacientes.csv
# - Serializar com Joblib
# - Criar API FastAPI com endpoint /predict
# - Expor via ngrok
# - Testar com curl ou Postman
```

### **Fase 4: Documentação Técnica (30 min)**
```
Criar DOC com:
- Título: "Sistema de Previsão de Risco Clínico - Biomedicina"
- Descrição: App/Game que usa IA para prever risco clínico
- Tech Spec:
  - Linguagem: Python 3.10+
  - Bibliotecas: pandas, scikit-learn, fastapi, joblib
  - APIs: ngrok (exposição de API)
  - Arquitetura: dataset → pipeline ML → modelo → API
```

### **Fase 5: Envios e Validação (15 min)**
```
1. GitHub: enviar CSV e código Python
2. Email: enviar DOC técnico ao professor
3. SPRINT-3: adicionar resultados/gráficos
4. Classe: avisar professor para validar
```

---

## ⏱️ CRONOGRAMA SUGERIDO

| Fase | Atividade | Tempo | Prazo |
|------|-----------|-------|-------|
| 1 | Executar scripts Python | 30 min | HOJE |
| 2 | Documentar resultados | 20 min | HOJE |
| 3 | Implementar API | 1-2 h | Amanhã |
| 4 | Doc Técnica | 30 min | Amanhã |
| 5 | Envios e validação | 15 min | Esta semana |

---

## 📌 NOTAS IMPORTANTES

### ⚠️ Alertas:
1. **AULA_07 NÃO VALIDADA**: Documento técnico da AULA_07 (especificação do projeto Biomedicina) foi enviado mas não foi retornado pelo professor com nota. **Verificar se foi aprovado.**

2. **Dependência**: A AULA_08 PARTE 2 depende que o professor já tenha aprovado a especificação da AULA_07.

3. **Skill Claude.IA**: Não há evidência de que a Skill "ASSISTENTE-ML" foi criada. Pode ser necessário criá-la ou adaptá-la.

### 💡 Recomendações:
1. Começar pelos scripts Python executáveis (mais fácil)
2. Documentar resultados enquanto executa
3. Criar API como extensão final (não é crítico para a nota 0,5)
4. Enviar DOC técnico assim que estiver pronto (pode ganhar nota da PARTE 1)

### 🎯 Valor Total Potencial:
- PARTE 1 (Tech Spec): 0,25 pontos
- PARTE 2, Ativ 1 (API): 0,15 pontos  
- PARTE 2, Ativ 2 (Dataset + ML): 0,35 pontos
- **TOTAL: 0,75 pontos** ⭐ (se completar tudo) ou **0,5 pontos** (mínimo esperado)

---

## 📞 Contatos Importantes

- **Professor**: flavio.santarelli@pro.fecaf.com.br
- **GitHub**: Repositório do grupo
- **SPRINT-3**: GitHub Projects

---

**Última Atualização**: 27/04/2026  
**Status**: ANÁLISE COMPLETA - PRONTO PARA AÇÃO
