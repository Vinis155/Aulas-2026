"""
=============================================================================
API REST — SISTEMA DE DIAGNÓSTICO DE RISCO CLÍNICO
=============================================================================
Projeto  : Diagnóstico de Risco Clínico com ML
Arquivo  : api_biomedicina.py
Função   : Expor o modelo ML treinado via API REST usando FastAPI

Requisitos:
    pip install fastapi uvicorn joblib

Como rodar:
    uvicorn api_biomedicina:app --reload --port 8000

Documentação automática:
    http://localhost:8000/docs (Swagger UI)
    http://localhost:8000/redoc (ReDoc)
=============================================================================
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import joblib
import numpy as np
import logging
import os

# ── CONFIGURACAO DE LOGGING ────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── INICIALIZACAO DA API ───────────────────────────────────────────────────────
app = FastAPI(
    title="API de Diagnóstico de Risco Clínico",
    description="Sistema de previsão de risco clínico usando Machine Learning (Random Forest)",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# ── SCHEMA DO REQUEST (Input) ──────────────────────────────────────────────────
class PacienteInput(BaseModel):
    """Dados de um paciente para diagnóstico de risco clínico"""
    nome: str = Field(..., description="Nome do paciente", example="João Silva")
    idade: int = Field(..., ge=18, le=120, description="Idade em anos", example=45)
    glicose: float = Field(..., ge=60, le=350, description="Glicose em mg/dL", example=120.0)
    pressao: float = Field(..., ge=80, le=220, description="Pressão arterial em mmHg", example=130.0)
    imc: float = Field(..., ge=15, le=55, description="IMC em kg/m²", example=25.0)
    colesterol: float = Field(..., ge=100, le=400, description="Colesterol em mg/dL", example=200.0)

    class Config:
        schema_extra = {
            "example": {
                "nome": "Maria Santos",
                "idade": 63,
                "glicose": 148.0,
                "pressao": 155.0,
                "imc": 31.5,
                "colesterol": 248.0
            }
        }

# ── SCHEMA DO RESPONSE (Output) ────────────────────────────────────────────────
class PacienteOutput(BaseModel):
    """Resultado do diagnóstico para um paciente"""
    nome: str
    idade: int
    risco_codigo: int
    risco_classificacao: str
    probabilidade: float
    explicacao: str

# ── VARIÁVEIS GLOBAIS PARA CARREGAR MODELO ────────────────────────────────────
modelo = None
scaler = None
metadados = None
FEATURES = ["idade", "glicose", "pressao", "imc", "colesterol"]
LABELS_RISCO = {0: "Baixo", 1: "Médio", 2: "Alto"}

# ── STARTUP: Carregar modelo ao iniciar a API ──────────────────────────────────
@app.on_event("startup")
async def carregar_modelo():
    """Carrega o modelo, scaler e metadados ao iniciar a API."""
    global modelo, scaler, metadados
    
    try:
        # Caminhos relativos para os arquivos
        base_dir = os.path.dirname(__file__)
        modelo_path = os.path.join(base_dir, "..", "06_Modelos", "melhor_modelo.pkl")
        scaler_path = os.path.join(base_dir, "..", "06_Modelos", "scaler.pkl")
        metadados_path = os.path.join(base_dir, "..", "06_Modelos", "metadados_modelo.pkl")
        
        logger.info("Carregando modelo treinado...")
        modelo = joblib.load(modelo_path)
        logger.info("✅ Modelo carregado com sucesso")
        
        logger.info("Carregando scaler (normalizador)...")
        scaler = joblib.load(scaler_path)
        logger.info("✅ Scaler carregado com sucesso")
        
        logger.info("Carregando metadados...")
        metadados = joblib.load(metadados_path)
        logger.info(f"✅ Metadados carregados: {metadados['melhor_modelo']}")
        logger.info(f"   Acurácia: {metadados['acuracia']:.4f}")
        logger.info(f"   F1-Score: {metadados['f1_score']:.4f}")
        
    except FileNotFoundError as e:
        logger.error(f"❌ Erro ao carregar arquivos: {e}")
        logger.error("Certifique-se de que os arquivos foram gerados por 2_pipeline_ml.py")
        raise RuntimeError("Falha ao carregar modelo") from e
    except Exception as e:
        logger.error(f"❌ Erro inesperado: {e}")
        raise

# ── ENDPOINT: Verificar status da API ──────────────────────────────────────────
@app.get("/")
async def root():
    """Endpoint raiz: verifica se a API está funcionando."""
    if modelo is None:
        return JSONResponse(
            status_code=503,
            content={"status": "erro", "mensagem": "Modelo não carregado"}
        )
    
    return {
        "status": "ok",
        "mensagem": "API de Diagnóstico de Risco Clínico está operacional",
        "modelo": metadados.get("melhor_modelo"),
        "acuracia": metadados.get("acuracia"),
    }

# ── ENDPOINT: Health check ─────────────────────────────────────────────────────
@app.get("/health")
async def health_check():
    """Verifica a saúde da API e dos recursos carregados."""
    return {
        "status": "healthy" if modelo is not None else "unhealthy",
        "modelo_carregado": modelo is not None,
        "scaler_carregado": scaler is not None,
    }

# ── ENDPOINT PRINCIPAL: Fazer diagnóstico ──────────────────────────────────────
@app.post("/predict", response_model=PacienteOutput)
async def predict(paciente: PacienteInput):
    """Faz o diagnóstico de risco para um paciente."""
    
    if modelo is None:
        logger.error("Modelo não carregado")
        raise HTTPException(status_code=503, detail="Modelo de ML não foi carregado")
    
    try:
        # Extrair dados na ordem correta
        features_valores = [
            paciente.idade,
            paciente.glicose,
            paciente.pressao,
            paciente.imc,
            paciente.colesterol
        ]
        
        # Converter e normalizar
        X = np.array([features_valores])
        X_normalizado = scaler.transform(X)
        
        # Fazer predição
        classe_predita = modelo.predict(X_normalizado)[0]
        probabilidades = modelo.predict_proba(X_normalizado)[0]
        probabilidade_max = float(probabilidades[int(classe_predita)])
        
        # Mapear para rótulo
        risco_classificacao = LABELS_RISCO[int(classe_predita)]
        
        # Gerar explicação
        fatores_risco = []
        if paciente.glicose >= 126:
            fatores_risco.append("glicose elevada (possível diabetes)")
        if paciente.pressao >= 140:
            fatores_risco.append("hipertensão")
        if paciente.imc >= 30:
            fatores_risco.append("obesidade")
        if paciente.colesterol >= 240:
            fatores_risco.append("colesterol alto")
        if paciente.idade >= 60:
            fatores_risco.append("idade avançada")
        
        if fatores_risco:
            explicacao = f"Paciente apresenta {', '.join(fatores_risco)}."
        else:
            explicacao = "Paciente não apresenta fatores de risco críticos."
        
        resposta = PacienteOutput(
            nome=paciente.nome,
            idade=paciente.idade,
            risco_codigo=int(classe_predita),
            risco_classificacao=risco_classificacao,
            probabilidade=probabilidade_max,
            explicacao=explicacao
        )
        
        logger.info(f"Predição realizada: {paciente.nome} -> Risco {risco_classificacao}")
        return resposta
        
    except ValueError as e:
        logger.error(f"Erro de validação: {e}")
        raise HTTPException(status_code=422, detail=f"Erro ao processar dados: {str(e)}")
    except Exception as e:
        logger.error(f"Erro ao fazer predição: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# ── ENDPOINT: Informações do modelo ────────────────────────────────────────────
@app.get("/info")
async def model_info():
    """Retorna informações sobre o modelo de ML carregado."""
    if modelo is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")
    
    return {
        "nome": metadados.get("melhor_modelo"),
        "acuracia": f"{metadados.get('acuracia'):.4f}",
        "f1_score": f"{metadados.get('f1_score'):.4f}",
        "validacao_cruzada": f"{metadados.get('cv_media'):.4f}",
        "features": metadados.get("features"),
        "classes": list(LABELS_RISCO.values()),
    }

# ── EXECUTAR API (se rodado diretamente) ───────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 60)
    print("🏥 API de Diagnóstico de Risco Clínico")
    print("=" * 60)
    print("\n📍 URL Local: http://localhost:8000")
    print("📖 Swagger UI: http://localhost:8000/docs")
    print("📖 ReDoc: http://localhost:8000/redoc")
    print("\n✅ Iniciando servidor...\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
