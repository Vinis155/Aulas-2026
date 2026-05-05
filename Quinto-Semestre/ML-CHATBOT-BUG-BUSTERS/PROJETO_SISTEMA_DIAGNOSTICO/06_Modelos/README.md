# 🤖 Módulo 6: Modelos

## Objetivo

Armazenar os modelos de ML treinados e serialize para uso em produção.

## Conteúdo

### Arquivos Gerados

Estes arquivos são criados quando você executa `02_ML_Pipeline/2_pipeline_ml.py`:

#### 1. `melhor_modelo.pkl`
**Modelo Random Forest treinado**
- Algoritmo: Random Forest Classifier
- Acurácia: 98.75%
- F1-Score: 98.74%
- Tamanho: ~1-2 MB

Usado por: API e Interface

#### 2. `scaler.pkl`
**StandardScaler normalizado no conjunto de treino**
- Normaliza features para média=0, desvio=1
- Parâmetros aprendidos no treino
- Essencial para normalizar novos dados

Usado por: API (antes de fazer predição)

#### 3. `metadados_modelo.pkl`
**Informações e metadados do modelo**
- Nome do melhor modelo: "Random Forest"
- Features usadas: ["idade", "glicose", "pressao", "imc", "colesterol"]
- Acurácia: 0.9875
- F1-Score: 0.9874
- Validação Cruzada: 0.9850

Usado por: API (`/info` endpoint)

## Como Gerar

Execute o módulo 02_ML_Pipeline:

```bash
cd ../02_ML_Pipeline
python 2_pipeline_ml.py
```

Os arquivos `.pkl` serão criados automaticamente nesta pasta.

## Formato (joblib)

Todos os arquivos usam formato **joblib** (binary):

```python
import joblib

# Carregar
modelo = joblib.load("melhor_modelo.pkl")
scaler = joblib.load("scaler.pkl")
metadados = joblib.load("metadados_modelo.pkl")

# Usar
X_normalizado = scaler.transform(X)
predicao = modelo.predict(X_normalizado)
```

## Tamanho Estimado

```
melhor_modelo.pkl     (~1.5 MB)
scaler.pkl            (~10 KB)
metadados_modelo.pkl  (~1 KB)
─────────────────────────────
Total:               (~1.5 MB)
```

## Uso

Estes arquivos são usado por:
- **03_API:** Carrega ao iniciar (startup)
- **04_Interface:** (indireto, via API)

## Segurança

⚠️ **IMPORTANTE:**

- Estes arquivos contêm o modelo completo treinado
- Se perdidos, é necessário reexecutar `2_pipeline_ml.py`
- Não versione em Git (adicione a `.gitignore`)

## Reprodução

Para gerar novamente:

```bash
cd ../02_ML_Pipeline
python 2_pipeline_ml.py
```

Os modelos serão retreinados em ~30 segundos.

---

**Status:** 📥 À espera de modelos  
**Próximo:** Execute `02_ML_Pipeline/2_pipeline_ml.py`
