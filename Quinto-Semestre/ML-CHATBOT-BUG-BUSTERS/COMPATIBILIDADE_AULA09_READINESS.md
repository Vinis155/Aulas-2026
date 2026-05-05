# 🎯 ANÁLISE DE COMPATIBILIDADE - AULA_09 vs AULAS 2-8
## Verificação: Projeto está pronto para integração e interface?

---

## 📊 VISÃO GERAL DA AULA_09

### Objetivo Principal:
**Desenvolver sistema completo de diagnóstico de risco clínico com:**
- ✅ Banco de dados (dataset sintético + CSV)
- ✅ Algoritmo ML treinado (3 modelos)
- ✅ **API REST** (expor modelo para uso externo)
- ✅ **Front-end** (interface para capturar dados e mostrar resultados)
- ✅ **Demonstração ao professor** (rodando, cadastrando, predizendo)

### Prazo & Entrega:
- 📅 **Aula 09**: Demonstração ao professor (27/04 já passou, seria próxima aula)
- 📅 **04/05/2026**: Pitch com vídeo (até 3 minutos)
- 📹 **Formato**: Vídeo mostrando: cadastro → predição → resultado

---

## ✅❌ ANÁLISE DE READINESS - O Que Falta?

### **COMPONENTE 1: BANCO DE DADOS**
```
Requisito AULA_09: Criar banco de dados (Python) com estrutura definida
Status Atual:
  ✅ DATASET_SINTÉTICO.py - PRONTO (gera 2000 registros)
  ✅ Estrutura de dados CORRETA:
     - Nome, Idade, Glicose, PA, IMC, Colesterol, Risco
  ❌ pacientes.csv - NÃO FOI GERADO AINDA
  
Ação Necessária:
  1. Executar: python DATASET_SINTÉTICO.py
  2. Gerar: pacientes.csv (2000 linhas)
  3. Usar como base para tudo que vem depois
  
Complexidade: ⭐ MUITO FÁCIL (1 comando)
Tempo: ~2 minutos
```

---

### **COMPONENTE 2: ALGORITMO ML (Pipeline)**
```
Requisito AULA_09: Treinar múltiplos modelos com validação
Status Atual:
  ✅ 2_pipeline_ml.py - PRONTO
  ✅ Executa os 3 modelos obrigatórios:
     - Logistic Regression
     - Random Forest
     - KNN
  ✅ Calcula métricas: acurácia, precision, recall, F1-score
  ✅ Validação cruzada: k-fold (k=5)
  ✅ Gera gráficos: comparação, matriz confusão, curva ROC
  ❌ Pipeline NÃO FOI EXECUTADO AINDA
  ❌ Modelos NÃO FORAM SALVOS em .pkl (serialização)
  
Ação Necessária:
  1. Executar: python 2_pipeline_ml.py
  2. Capturar saída (métricas)
  3. Salvar melhor modelo com joblib:
     joblib.dump(best_model, 'melhor_modelo.pkl')
  
Complexidade: ⭐ MUITO FÁCIL (1 comando + 1 linha de código)
Tempo: ~5-10 minutos execução
```

---

### **COMPONENTE 3: API REST (FastAPI)**
```
Requisito AULA_09: API para integração com front-end
Status Atual:
  ✅ ml_api.txt - TUTORIAL COMPLETO disponível
  ❌ api_sistema.py - NÃO FOI IMPLEMENTADO
  ❌ Endpoint /predict - NÃO EXISTE
  ❌ API NÃO ESTÁ RODANDO
  
Requerimentos da API:
  - Tipo: REST com FastAPI + uvicorn
  - Endpoint: POST /predict
  - Input: { "nome": str, "idade": int, "glicose": float, ... }
  - Output: { "risco": 0|1|2, "probabilidade": float, "classificacao": str }
  - Exposição: ngrok (URL pública + token)
  
Ação Necessária:
  1. Criar arquivo: api_sistema.py
  2. Carregar melhor_modelo.pkl
  3. Implementar endpoint /predict
  4. Testar com curl ou Postman
  5. Expor via ngrok
  
Complexidade: ⭐⭐ FÁCIL (código template disponível em ml_api.txt)
Tempo: ~30-45 minutos (incluindo testes)
```

---

### **COMPONENTE 4: FRONT-END (Interface)**
```
Requisito AULA_09: Capturar dados do paciente e mostrar resultado
Status Atual:
  ❌ FRONT-END NÃO EXISTE
  ❌ Nenhuma interface implementada
  
Opções Recomendadas (em ordem de simplicidade):
  
  OPÇÃO 1 (⭐⭐⭐ RECOMENDADO): CLI Simples + Print
  - Modo: Linha de comando
  - Input: terminal com input()
  - Output: print formatado
  - Tempo: 15 minutos
  - Adequado para: Demonstração rápida ao professor
  
  OPÇÃO 2 (⭐⭐⭐⭐ MELHOR): Streamlit
  - Modo: Web interface
  - Input: campos interativos
  - Output: interface com gráficos
  - Tempo: 30-45 minutos
  - Instalação: pip install streamlit
  - Adequado para: Pitch profissional, vídeo
  
  OPÇÃO 3 (⭐⭐ MAIS SIMPLES): Tkinter
  - Modo: GUI Desktop
  - Input: formulário gráfico
  - Output: resultado em janela
  - Tempo: 45-60 minutos
  - Instalação: Built-in Python
  - Adequado para: Desktop puro
  
Ação Necessária:
  1. Escolher framework (recomendo: Streamlit)
  2. Criar arquivo: interface_streamlit.py
  3. Implementar:
     - Form com 6 inputs (Nome, Idade, Glicose, PA, IMC, Colesterol)
     - Botão "Fazer Diagnóstico"
     - Enviar à API /predict
     - Exibir: Classificação (Baixo/Médio/Alto) + Probabilidade
  4. Rodar: streamlit run interface_streamlit.py
  
Complexidade: ⭐⭐ FÁCIL (Streamlit faz 90% do trabalho)
Tempo: ~30-45 minutos
```

---

### **COMPONENTE 5: DOCUMENTAÇÃO TÉCNICA**
```
Requisito AULA_09: Document técnico conforme roteiro_final_ML-BIO.pdf
Status Atual:
  ❌ DOC TECH NÃO EXISTE (faz parte de AULA_08 PARTE 1 também)
  ❌ Especificação não foi enviada ao professor
  
Requerimentos:
  - Arquivo: Tech_Spec_Biomedicina.docx ou .pdf
  - Conteúdo:
    - Arquitetura do Sistema (dataset → ML → API → Front-end)
    - Componentes: Database, Pipeline, API, UI
    - Stack Técnico: Python 3.10, pandas, scikit-learn, fastapi, streamlit
    - Fluxo: Usuário cadastra → API prediz → Resultado mostrado
    - Modelos: LR, RF, KNN (métricas)
    - Especificação funcional: inputs/outputs
    - Modelo de dados: estrutura do CSV
  
Ação Necessária:
  1. Criar documento em Google Docs ou Word
  2. Preencher conforme acima
  3. Enviar para: flavio.santarelli@pro.fecaf.com.br
  
Complexidade: ⭐ MUITO FÁCIL (copiar estrutura)
Tempo: ~20 minutos
```

---

## 🚨 CHECKLIST CRÍTICO PARA AULA_09

### **Antes da Aula (O Que DEVE Estar Pronto):**

- [ ] **Banco de Dados**: 
  - [ ] Executar DATASET_SINTÉTICO.py
  - [ ] Arquivo pacientes.csv gerado (2000 registros)
  
- [ ] **Algoritmo ML**:
  - [ ] Executar 2_pipeline_ml.py
  - [ ] 3 modelos treinados
  - [ ] Melhor modelo salvo em .pkl
  - [ ] Métricas capturadas (acurácia, F1, etc.)
  
- [ ] **API REST**:
  - [ ] Arquivo api_sistema.py implementado
  - [ ] Endpoint /predict funcionando
  - [ ] Testado com pelo menos 1 exemplo
  - [ ] Rodando em localhost:8000
  
- [ ] **Front-end**:
  - [ ] Interface implementada (CLI ou Streamlit)
  - [ ] Formulário com 6 campos
  - [ ] Botão para fazer diagnóstico
  - [ ] Resultado exibindo classificação + probabilidade
  - [ ] Testado: cadastro de paciente → resposta
  
- [ ] **Documentação**:
  - [ ] Tech Spec completo
  - [ ] Diagrama da arquitetura (opcional)
  - [ ] Enviado ao professor

---

## 📋 PLANO DE AÇÃO RECOMENDADO

### **FASE 1: Database & ML (45 minutos)**

```bash
# 1. Gerar dataset (2 min)
cd AULA_08
python DATASET_SINTÉTICO.py
# → Cria: pacientes.csv

# 2. Treinar modelos (5-10 min)
python 2_pipeline_ml.py
# → Cria: gráficos PNG + métricas em console
# → Copiar melhor modelo para salvar em .pkl

# 3. Salvar modelo (modificar 2_pipeline_ml.py)
# Adicionar ao final:
# import joblib
# joblib.dump(best_model, 'melhor_modelo.pkl')
```

### **FASE 2: API REST (30-45 minutos)**

```python
# Arquivo: api_sistema.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = FastAPI()

class PacienteInput(BaseModel):
    nome: str
    idade: int
    glicose: float
    pressao: float  # PA
    imc: float
    colesterol: float

# Carregar modelo e scaler
model = joblib.load('melhor_modelo.pkl')
scaler = joblib.load('scaler.pkl')  # Salvar scaler também

@app.post("/predict")
async def predict(paciente: PacienteInput):
    # Preparar dados
    X = [[paciente.idade, paciente.glicose, paciente.pressao, 
          paciente.imc, paciente.colesterol]]
    X_scaled = scaler.transform(X)
    
    # Predizer
    risco = model.predict(X_scaled)[0]
    probabilidade = model.predict_proba(X_scaled).max()
    
    labels = {0: "Baixo", 1: "Médio", 2: "Alto"}
    
    return {
        "nome": paciente.nome,
        "risco": int(risco),
        "classificacao": labels[int(risco)],
        "probabilidade": float(probabilidade)
    }

# Rodar com: uvicorn api_sistema:app --reload
```

### **FASE 3: Front-end Streamlit (30-45 minutos)**

```python
# Arquivo: interface_streamlit.py
import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Diagnóstico de Risco Clínico", layout="wide")
st.title("🏥 Sistema de Diagnóstico de Risco Clínico")

# Formulário
col1, col2 = st.columns(2)

with col1:
    nome = st.text_input("Nome do Paciente")
    idade = st.number_input("Idade", min_value=18, max_value=99)
    glicose = st.number_input("Glicose (mg/dL)", min_value=60, max_value=350)

with col2:
    pressao = st.number_input("Pressão Arterial (mmHg)", min_value=80, max_value=220)
    imc = st.number_input("IMC (kg/m²)", min_value=15.0, max_value=55.0, step=0.1)
    colesterol = st.number_input("Colesterol (mg/dL)", min_value=100, max_value=400)

# Botão para fazer diagnóstico
if st.button("🔍 Fazer Diagnóstico"):
    # Enviar à API
    payload = {
        "nome": nome,
        "idade": int(idade),
        "glicose": float(glicose),
        "pressao": float(pressao),
        "imc": float(imc),
        "colesterol": float(colesterol)
    }
    
    try:
        response = requests.post("http://localhost:8000/predict", json=payload)
        resultado = response.json()
        
        # Exibir resultado
        st.success(f"✅ Diagnóstico Concluído")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Classificação de Risco", resultado['classificacao'])
        with col2:
            st.metric("Probabilidade", f"{resultado['probabilidade']*100:.1f}%")
        with col3:
            st.metric("Nível", resultado['risco'])
            
        # Mensagem personalisada
        if resultado['risco'] == 0:
            st.info("ℹ️ Paciente com BAIXO risco. Continue com acompanhamento regular.")
        elif resultado['risco'] == 1:
            st.warning("⚠️ Paciente com RISCO MÉDIO. Recomenda-se acompanhamento.")
        else:
            st.error("🚨 Paciente com ALTO risco. Encaminhe para avaliação urgente.")
            
    except Exception as e:
        st.error(f"Erro ao conectar à API: {e}")

# Rodar com: streamlit run interface_streamlit.py
```

### **FASE 4: Documentação (20 minutos)**

```markdown
Criar: Tech_Spec_Biomedicina.md ou .docx

# Especificação Técnica - Sistema de Diagnóstico de Risco Clínico

## 1. Arquitetura do Sistema
[Diagrama aqui ou descrição]

## 2. Stack Técnico
- Python 3.10+
- Pandas: manipulação de dados
- Scikit-learn: ML (LR, RF, KNN)
- FastAPI: API REST
- Streamlit: Interface web
- Joblib: Serialização de modelos

## 3. Componentes
1. Database: CSV com 2000 pacientes sintéticos
2. Pipeline ML: 3 modelos com validação k-fold
3. API: Endpoint /predict (POST)
4. UI: Streamlit web interface

## 4. Fluxo
Usuário → UI Streamlit → API FastAPI → ML Pipeline → Resultado

## 5. Modelos Treinados
- Logistic Regression: acurácia X%
- Random Forest: acurácia X%
- KNN: acurácia X%
Melhor: [modelo escolhido]

## 6. Formato de Dados
Features: Idade, Glicose, PA, IMC, Colesterol
Target: Risco (0=Baixo, 1=Médio, 2=Alto)
```

---

## ⏱️ CRONOGRAMA EXECUTIVO

| Fase | O Quê | Tempo | Prazo |
|------|-------|-------|-------|
| 1 | Database + ML | 45 min | **HOJE** |
| 2 | API REST | 30-45 min | Hoje/Amanhã |
| 3 | Front-end | 30-45 min | Amanhã |
| 4 | Documentação | 20 min | Amanhã |
| 5 | Vídeo/Pitch | 20 min | Até 04/05 |

**Total**: ~2,5 horas para tudo pronto

---

## 🎬 PARA O VÍDEO/PITCH (3 minutos - 04/05/2026)

**Roteiro Sugerido:**

```
00-30s: Introdução
- "Nosso sistema de diagnóstico de risco clínico usa Machine Learning"
- Apresentar o problema/contexto

30-60s: Demonstração
- Abrir interface Streamlit
- Preencher formulário com novo paciente
- Clicar "Fazer Diagnóstico"
- Mostrar resultado

60-90s: Arquitetura & Modelos
- Explicar: dataset → pipeline ML → API → resultado
- Mencionar 3 modelos treinados (LR, RF, KNN)
- Mostrar acurácia do melhor modelo

90-120s: Conclusão & Impacto
- Caso de uso real: hospitals/clínicas
- Próximos passos

120-180s: Buffer/Perguntas
```

---

## 🔴 RISCOS & MITIGAÇÕES

| Risco | Impacto | Mitigação |
|-------|--------|-----------|
| CSV não gerado | Bloqueia tudo | Executar DATASET_SINTÉTICO.py hoje |
| API não conecta com UI | Sistema não funciona | Testar com curl antes de UI |
| Streamlit não instala | Bloqueador | Usar CLI simples como fallback |
| Vídeo muito longo | Pontos perdidos | Editar com até 3 min |

---

## ✅ RECOMENDAÇÃO FINAL

**Status Atual**: ~60% pronto (database + ML scripts existem)

**Para estar 100% pronto para AULA_09:**
1. ✅ Executar scripts (30 min)
2. ✅ Criar API (45 min)
3. ✅ Criar UI Streamlit (45 min)
4. ✅ Documentar (20 min)

**Tempo Total**: ~2,5 horas

**Recomendação**: Fazer hoje (AULA_08 + prep AULA_09) para ganhar tempo antes do vídeo.

---

**Última Atualização**: 27/04/2026  
**Status**: READY - Todos os componentes têm templates/código disponível  
**Bloqueador**: Nenhum - Apenas precisa executar!
