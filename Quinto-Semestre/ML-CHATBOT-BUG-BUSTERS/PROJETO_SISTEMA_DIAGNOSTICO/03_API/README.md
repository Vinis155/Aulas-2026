# 🌐 Módulo 3: API REST

## Objetivo

Expor o modelo de ML treinado via uma API REST para que outras aplicações possam fazer diagnósticos.

## Arquivo

- **`api_biomedicina.py`** - API FastAPI

## Como Usar

### 1. Instalar Dependências

```bash
pip install fastapi uvicorn joblib
```

### 2. Rodar a API

```bash
cd 03_API
uvicorn api_biomedicina:app --reload --port 8000
```

**Esperado:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Carregando modelo treinado...
INFO:     ✅ Modelo carregado com sucesso
```

## Endpoints Disponíveis

### ✅ GET `/`
Status da API

**Resposta:**
```json
{
  "status": "ok",
  "mensagem": "API de Diagnóstico de Risco Clínico está operacional",
  "modelo": "Random Forest",
  "acuracia": 0.9875
}
```

### ✅ GET `/health`
Health check da API

**Resposta:**
```json
{
  "status": "healthy",
  "modelo_carregado": true,
  "scaler_carregado": true
}
```

### ✅ POST `/predict`
Fazer diagnóstico de risco

**Request:**
```json
{
  "nome": "João Silva",
  "idade": 63,
  "glicose": 148.0,
  "pressao": 155.0,
  "imc": 31.5,
  "colesterol": 248.0
}
```

**Response:**
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

### ✅ GET `/info`
Informações do modelo

**Resposta:**
```json
{
  "nome": "Random Forest",
  "acuracia": "0.9875",
  "f1_score": "0.9874",
  "validacao_cruzada": "0.9850",
  "features": ["idade", "glicose", "pressao", "imc", "colesterol"],
  "classes": ["Baixo", "Médio", "Alto"]
}
```

## Testar com curl

```bash
# Test health check
curl http://localhost:8000/health

# Fazer diagnóstico
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "nome":"Maria",
       "idade":63,
       "glicose":148,
       "pressao":155,
       "imc":31.5,
       "colesterol":248
     }'
```

## Documentação Interativa

Após rodar a API, acesse:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Lá você pode testar os endpoints diretamente no navegador!

## Validações

A API valida automaticamente:

- **Idade:** 18-120 anos
- **Glicose:** 60-350 mg/dL
- **Pressão:** 80-220 mmHg
- **IMC:** 15-55 kg/m²
- **Colesterol:** 100-400 mg/dL

Valores fora desses intervalos retornam erro 422.

## Pré-requisitos

- ✅ Arquivos `.pkl` gerados (execute `02_ML_Pipeline/2_pipeline_ml.py`)
- ✅ FastAPI e Uvicorn instalados
- ✅ Porta 8000 disponível (ou mudar em `--port 8001`)

## Próximo Passo

Após a API estar rodando, execute o módulo **04_Interface** para usar o Streamlit.

---

**Status:** ✅ Pronto para usar  
**Data:** 27/04/2026  
**Modelo:** Random Forest (98.75% acurácia)
