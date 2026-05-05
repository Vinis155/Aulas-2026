# 🚀 GUIA DE EXECUÇÃO — Sistema de Diagnóstico de Risco Clínico

## 📋 Resumo do que foi criado

```
AULA_08/
├── 2_pipeline_ml.py              ✅ Pipeline ML (MODIFICADO + joblib.dump)
├── DATASET_SINTÉTICO.py          ✅ Gerador de dataset
├── api_biomedicina.py            ✅ NOVO - API FastAPI
├── interface_streamlit.py         ✅ NOVO - Front-end Streamlit
└── [Arquivos gerados após rodar]
    ├── pacientes.csv             (2000 registros)
    ├── melhor_modelo.pkl         (modelo Random Forest)
    ├── scaler.pkl                (normalizador)
    ├── metadados_modelo.pkl      (informações)
    ├── graficos_comparacao.png
    ├── matriz_confusao.png
    └── curva_roc.png
```

---

## ⚙️ PRÉ-REQUISITOS

### 1. Instalar dependências Python

```bash
pip install fastapi uvicorn joblib streamlit requests pandas numpy scikit-learn matplotlib
```

Ou use o arquivo `requirements.txt`:

```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

### 2. Verificar Python

```bash
python --version
# Esperado: Python 3.10 ou superior
```

---

## 🎯 EXECUÇÃO PASSO A PASSO

### **PASSO 1: Gerar Dataset (1 terminal)**

```bash
cd AULA_08
python DATASET_SINTÉTICO.py
```

**Esperado:**
```
GERADOR DE DATASET — RISCO CLINICO
====================================================
Registros gerados : 2000
Distribuicao das classes de risco:
    Classe 0 (Baixo): xxxxx  16.2%  ...
    Classe 1 (Medio): xxxxx  68.3%  ...
    Classe 2 (Alto ):  xxxxx  15.4%  ...

Arquivo 'pacientes.csv' salvo com sucesso.
```

✅ **Arquivo criado:** `pacientes.csv`

---

### **PASSO 2: Treinar Modelos e Salvar (mesmo terminal)**

```bash
python 2_pipeline_ml.py
```

**Esperado (resumido):**
```
SISTEMA DE PREVISAO DE RISCO CLINICO — PIPELINE ML
====================================================

[ETAPA 1] Lendo 'pacientes.csv'...
[ETAPA 2] Separando features (X) e target (y)...
...
[ETAPA 8] Comparacao e selecao do melhor modelo...
>>> MELHOR MODELO: Random Forest <<<

[ETAPA 9] Gerando visualizacoes...
[OK] 'graficos_comparacao.png' salvo.
[OK] 'matriz_confusao.png' salvo.
[OK] 'curva_roc.png' salvo.

[ETAPA 11] Salvando modelo e scaler para producao...
[OK] Modelo 'Random Forest' salvo como 'melhor_modelo.pkl'
[OK] StandardScaler salvo como 'scaler.pkl'
[OK] Metadados salvos como 'metadados_modelo.pkl'

✅ Pronto para usar na API e Interface!
```

✅ **Arquivos criados:**
- `melhor_modelo.pkl`
- `scaler.pkl`
- `metadados_modelo.pkl`
- `graficos_comparacao.png`
- `matriz_confusao.png`
- `curva_roc.png`

---

### **PASSO 3: Rodar a API FastAPI (novo terminal)**

```bash
# Terminal 2
cd AULA_08
uvicorn api_biomedicina:app --reload --port 8000
```

**Esperado:**
```
============================================================
🏥 API de Diagnóstico de Risco Clínico
============================================================

📍 URL Local: http://localhost:8000
📖 Swagger UI: http://localhost:8000/docs
📖 ReDoc: http://localhost:8000/redoc

✅ Iniciando servidor...

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Carregando modelo treinado...
INFO:     ✅ Modelo carregado com sucesso
INFO:     ✅ Scaler carregado com sucesso
INFO:     ✅ Metadados carregados: Random Forest
```

✅ **API rodando em:** `http://localhost:8000`

**Testar no navegador:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

---

### **PASSO 4: Rodar o Front-end Streamlit (novo terminal)**

```bash
# Terminal 3
cd AULA_08
streamlit run interface_streamlit.py
```

**Esperado:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://YOUR_IP:8501

For debugging and remote access, visit http://localhost:8501/?embed=true
```

✅ **Interface rodando em:** `http://localhost:8501`

---

## 📝 COMO USAR

### Via Interface Streamlit (Recomendado)

1. Abra: http://localhost:8501
2. Preencha os dados do paciente:
   - Nome
   - Idade (18-120)
   - Glicose (60-350)
   - Pressão (80-220)
   - IMC (15-55)
   - Colesterol (100-400)
3. Clique em **"🔍 Fazer Diagnóstico"**
4. Veja o resultado com:
   - Classificação (Baixo/Médio/Alto)
   - Probabilidade
   - Explicação dos fatores de risco

---

### Via API (Avançado)

#### **Teste com curl:**

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "nome": "João Silva",
       "idade": 63,
       "glicose": 148.0,
       "pressao": 155.0,
       "imc": 31.5,
       "colesterol": 248.0
     }'
```

**Resposta esperada:**
```json
{
  "nome": "João Silva",
  "idade": 63,
  "risco_codigo": 2,
  "risco_classificacao": "Alto",
  "probabilidade": 0.95,
  "explicacao": "Paciente apresenta glicose elevada (possível diabetes), hipertensão, obesidade, colesterol alto."
}
```

#### **Endpoints disponíveis:**

| Método | Endpoint | Função |
|--------|----------|--------|
| GET | `/` | Status da API |
| GET | `/health` | Health check |
| GET | `/info` | Informações do modelo |
| POST | `/predict` | Fazer diagnóstico |

---

## 🎬 EXEMPLO COMPLETO DE USO

### Terminal 1: Preparar dados e treinar modelo

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

### Acessar no navegador

```
- Interface: http://localhost:8501
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
```

### Preencher formulário e clicar em "Fazer Diagnóstico"

✅ **Sistema rodando completo!**

---

## 🧪 TESTE RÁPIDO

### Dados de teste inclusos no código:

**Paciente: Fernanda**
- Idade: 63
- Glicose: 148.0
- Pressão: 155.0
- IMC: 31.5
- Colesterol: 248.0

**Resultado esperado:**
- Risco: **Alto**
- Probabilidade: **100%** (muito confiável)
- Razão: Múltiplos fatores de risco críticos

---

## ⚠️ TROUBLESHOOTING

### Erro: "Modelo não carregado"
```
Solução: Rodar 2_pipeline_ml.py para gerar melhor_modelo.pkl e scaler.pkl
```

### Erro: "Não conseguiu conectar à API"
```
Solução: 
1. Verificar se a API está rodando no Terminal 2
2. Confirmação: http://localhost:8000/health retorna 200
3. Usar URL correta na interface: http://localhost:8000
```

### Erro: "TimeoutError"
```
Solução:
1. API pode estar lenta no primeiro carregamento
2. Aumentar timeout na interface_streamlit.py (linha ~200)
3. Ou executar novamente
```

### API reclama "Address already in use"
```
Solução: Trocar porta
uvicorn api_biomedicina:app --port 8001 (ou outra porta disponível)
Depois mudar interface_streamlit.py para http://localhost:8001
```

### Streamlit não inicia
```
Solução: Instalar explicitamente
pip install --upgrade streamlit
streamlit run interface_streamlit.py --logger.level=debug
```

---

## 📊 ARQUITETURA DO SISTEMA

```
┌─────────────────────────────────────────────────────────────┐
│                 Front-end (Streamlit)                       │
│  http://localhost:8501                                      │
│  - Formulário com 6 inputs                                   │
│  - Exibe resultados com gráficos                             │
└────────────────────────────┬────────────────────────────────┘
                              │ HTTP POST
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              API REST (FastAPI)                              │
│  http://localhost:8000                                      │
│  - Endpoint /predict                                         │
│  - Valida dados                                              │
│  - Normaliza com scaler                                      │
└────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│           Modelo ML Serializado                              │
│  - melhor_modelo.pkl (Random Forest)                         │
│  - scaler.pkl (StandardScaler)                               │
│  - Acurácia: 98.75%                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Dataset Sintético                               │
│  pacientes.csv (2000 registros)                              │
│  - Features: idade, glicose, pressão, IMC, colesterol       │
│  - Target: risco (0/1/2)                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📈 PRÓXIMOS PASSOS (AULA_09)

1. ✅ Sistema rodando localmente
2. ✅ Teste funcional com dados reais
3. ➡️ **Demonstrar para o professor em sala**
4. ➡️ Gravar vídeo pitch (até 3 minutos)
5. ➡️ Enviar vídeo no AVA até 04/05/2026

---

## 📞 CONTATOS E REFERÊNCIAS

- **Professor:** flavio.santarelli@pro.fecaf.com.br
- **API FastAPI:** https://fastapi.tiangolo.com/
- **Streamlit:** https://streamlit.io/
- **scikit-learn:** https://scikit-learn.org/

---

## ✅ CHECKLIST DE EXECUÇÃO

- [ ] Instalar dependências: `pip install fastapi uvicorn joblib streamlit requests`
- [ ] Executar DATASET_SINTÉTICO.py
- [ ] Executar 2_pipeline_ml.py
- [ ] Rodar API: `uvicorn api_biomedicina:app --reload`
- [ ] Rodar Interface: `streamlit run interface_streamlit.py`
- [ ] Acessar http://localhost:8501
- [ ] Testar com dados de "Fernanda"
- [ ] Verificar resultado esperado (Risco Alto)
- [ ] Testar outros pacientes
- [ ] Pronto para demonstrar ao professor!

---

**Data:** 27/04/2026  
**Status:** ✅ Sistema pronto para uso  
**Próximo:** 04/05/2026 - Pitch com vídeo
