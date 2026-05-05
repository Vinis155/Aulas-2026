"""
=============================================================================
INTERFACE STREAMLIT — SISTEMA DE DIAGNÓSTICO DE RISCO CLÍNICO
=============================================================================
Projeto  : Diagnóstico de Risco Clínico com ML
Arquivo  : interface_streamlit.py
Função   : Interface web para diagnóstico usando Streamlit

Requisitos:
    pip install streamlit requests

Como rodar:
    streamlit run interface_streamlit.py

Acesso:
    http://localhost:8501

Nota:
    Certifique-se de que a API está rodando em outro terminal:
    uvicorn api_biomedicina:app --reload --port 8000

=============================================================================
"""

import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd

# ── CONFIGURAÇÃO DA PÁGINA ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Diagnóstico de Risco Clínico",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── ESTILO CUSTOMIZADO ────────────────────────────────────────────────────────
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stTitle {
            color: #1f77b4;
            font-size: 2.5rem;
        }
        .subtitle {
            color: #666;
            font-size: 1rem;
            margin: 1rem 0;
        }
        .resultado-baixo {
            background-color: #d4edda;
            border-left: 5px solid #28a745;
            padding: 1rem;
            border-radius: 0.5rem;
        }
        .resultado-medio {
            background-color: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 1rem;
            border-radius: 0.5rem;
        }
        .resultado-alto {
            background-color: #f8d7da;
            border-left: 5px solid #dc3545;
            padding: 1rem;
            border-radius: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# ── TÍTULO E DESCRIÇÃO ────────────────────────────────────────────────────────
st.title("🏥 Sistema de Diagnóstico de Risco Clínico")
st.markdown("### Análise inteligente de risco de saúde com Machine Learning")
st.markdown("---")

# ── BARRA LATERAL ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configurações")
    
    # URL da API
    api_url = st.text_input(
        "URL da API",
        value="http://localhost:8000",
        help="Endereço base da API FastAPI"
    )
    
    # Status da API
    try:
        response = requests.get(f"{api_url}/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ API conectada", icon="✅")
        else:
            st.error("❌ API desconectada", icon="❌")
    except:
        st.error("❌ Não conseguiu conectar à API", icon="❌")
    
    st.divider()
    
    # Informações do modelo
    st.subheader("ℹ️ Sobre o Modelo")
    try:
        info = requests.get(f"{api_url}/info", timeout=5).json()
        st.write(f"**Modelo:** {info['nome']}")
        st.write(f"**Acurácia:** {info['acuracia']}")
        st.write(f"**F1-Score:** {info['f1_score']}")
        st.write(f"**Validação CV:** {info['validacao_cruzada']}")
    except:
        st.warning("Não foi possível carregar informações do modelo")
    
    st.divider()
    
    # Referência de valores
    st.subheader("📋 Referência de Valores")
    referencia = """
    **Glicose (mg/dL):**
    - Normal: < 100
    - Pré-diabetes: 100-125
    - Diabetes: ≥ 126
    
    **Pressão (mmHg):**
    - Ótima: < 120
    - Normal: 120-129
    - Hipertensão: ≥ 140
    
    **IMC (kg/m²):**
    - Normal: 18.5-24.9
    - Sobrepeso: 25-29.9
    - Obesidade: ≥ 30
    
    **Colesterol (mg/dL):**
    - Desejável: < 200
    - Limítrofe: 200-239
    - Alto: ≥ 240
    """
    st.info(referencia)

# ── CONTEÚDO PRINCIPAL ────────────────────────────────────────────────────────
# Dividir em 2 colunas
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("👤 Dados do Paciente")
    
    # Linha 1: Nome e Idade
    col_nome, col_idade = st.columns(2)
    with col_nome:
        nome = st.text_input(
            "Nome do Paciente",
            placeholder="Ex: João Silva",
            help="Digite o nome completo do paciente"
        )
    with col_idade:
        idade = st.number_input(
            "Idade (anos)",
            min_value=18,
            max_value=120,
            value=45,
            step=1,
            help="Idade em anos (18-120)"
        )
    
    st.divider()
    
    # Linha 2: Glicose, Pressão, IMC
    col_glicose, col_pressao, col_imc = st.columns(3)
    
    with col_glicose:
        glicose = st.number_input(
            "Glicose (mg/dL)",
            min_value=60,
            max_value=350,
            value=100.0,
            step=0.5,
            help="Glicose em mg/dL (60-350)"
        )
    
    with col_pressao:
        pressao = st.number_input(
            "Pressão (mmHg)",
            min_value=80,
            max_value=220,
            value=120.0,
            step=0.5,
            help="Pressão arterial sistólica em mmHg (80-220)"
        )
    
    with col_imc:
        imc = st.number_input(
            "IMC (kg/m²)",
            min_value=15.0,
            max_value=55.0,
            value=25.0,
            step=0.1,
            help="Índice de Massa Corporal em kg/m² (15-55)"
        )
    
    st.divider()
    
    # Linha 3: Colesterol
    colesterol = st.number_input(
        "Colesterol (mg/dL)",
        min_value=100,
        max_value=400,
        value=200.0,
        step=0.5,
        help="Colesterol total em mg/dL (100-400)"
    )

with col2:
    st.subheader("🎯 Indicadores Rápidos")
    
    # Indicadores do paciente
    st.metric(
        label="Categoria Glicose",
        value="Alta" if glicose >= 126 else "Normal" if glicose < 100 else "Pré-diabetes",
        delta="⚠️ Risco" if glicose >= 126 else "✅ OK"
    )
    
    st.metric(
        label="Categoria PA",
        value="Alta" if pressao >= 140 else "Normal",
        delta="⚠️ Risco" if pressao >= 140 else "✅ OK"
    )
    
    st.metric(
        label="Categoria IMC",
        value="Obesidade" if imc >= 30 else "Sobrepeso" if imc >= 25 else "Normal",
        delta="⚠️ Risco" if imc >= 30 else "✅ OK"
    )
    
    st.metric(
        label="Categoria Colesterol",
        value="Alto" if colesterol >= 240 else "Normal",
        delta="⚠️ Risco" if colesterol >= 240 else "✅ OK"
    )

# ── SEÇÃO DE AÇÃO ─────────────────────────────────────────────────────────────
st.divider()

col_btn1, col_btn2 = st.columns([1, 4])

with col_btn1:
    botao_diagnostico = st.button(
        "🔍 Fazer Diagnóstico",
        key="btn_diagnostico",
        use_container_width=True,
        type="primary"
    )

with col_btn2:
    st.info("💡 Clique no botão ao lado para processar o diagnóstico com IA")

# ── PROCESSAMENTO DO DIAGNÓSTICO ──────────────────────────────────────────────
if botao_diagnostico:
    # Validações básicas
    if not nome:
        st.error("❌ Por favor, preencha o nome do paciente")
    else:
        # Mostrar status de processamento
        with st.spinner("⏳ Processando diagnóstico... Aguarde"):
            try:
                # Preparar dados para enviar à API
                dados_paciente = {
                    "nome": nome,
                    "idade": int(idade),
                    "glicose": float(glicose),
                    "pressao": float(pressao),
                    "imc": float(imc),
                    "colesterol": float(colesterol)
                }
                
                # Fazer requisição à API
                response = requests.post(
                    f"{api_url}/predict",
                    json=dados_paciente,
                    timeout=10
                )
                
                # Processar resposta
                if response.status_code == 200:
                    resultado = response.json()
                    
                    # Guardar resultado na sessão para manter na tela
                    st.session_state.ultimo_resultado = resultado
                    st.success("✅ Diagnóstico concluído com sucesso!")
                    
                else:
                    st.error(f"❌ Erro na API: {response.status_code}")
                    st.error(f"Detalhes: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Não foi possível conectar à API")
                st.error("Certifique-se de que a API está rodando em http://localhost:8000")
                st.error("Terminal de comando: `uvicorn api_biomedicina:app --reload`")
            except requests.exceptions.Timeout:
                st.error("❌ Timeout ao conectar à API")
            except Exception as e:
                st.error(f"❌ Erro ao fazer diagnóstico: {str(e)}")

# ── EXIBIÇÃO DOS RESULTADOS ──────────────────────────────────────────────────
if "ultimo_resultado" in st.session_state:
    resultado = st.session_state.ultimo_resultado
    
    st.divider()
    st.subheader("📊 Resultado do Diagnóstico")
    
    # Determinar a cor e o ícone baseado no risco
    risco_codigo = resultado["risco_codigo"]
    risco_class = resultado["risco_classificacao"]
    probabilidade = resultado["probabilidade"]
    
    if risco_codigo == 0:
        cor = "green"
        icone = "✅"
        classe_css = "resultado-baixo"
        msg_recomendacao = "Manter acompanhamento regular e estilo de vida saudável."
    elif risco_codigo == 1:
        cor = "orange"
        icone = "⚠️"
        classe_css = "resultado-medio"
        msg_recomendacao = "Recomenda-se acompanhamento médico para monitoramento."
    else:  # risco_codigo == 2
        cor = "red"
        icone = "🚨"
        classe_css = "resultado-alto"
        msg_recomendacao = "Encaminhe para avaliação médica urgente e considere intervenções preventivas."
    
    # Exibir resultado
    col_resultado1, col_resultado2, col_resultado3 = st.columns(3)
    
    with col_resultado1:
        st.metric(
            label="Classificação de Risco",
            value=risco_class,
            delta=icone
        )
    
    with col_resultado2:
        st.metric(
            label="Confiança (Probabilidade)",
            value=f"{probabilidade*100:.1f}%",
            delta="Alta" if probabilidade > 0.8 else "Moderada"
        )
    
    with col_resultado3:
        st.metric(
            label="Código de Risco",
            value=risco_codigo,
            delta="0=Baixo, 1=Médio, 2=Alto"
        )
    
    # Explicação dos fatores de risco
    st.markdown(f"""
    <div class="{classe_css}">
        <h4>{icone} Análise de Fatores de Risco</h4>
        <p><strong>Explicação:</strong> {resultado['explicacao']}</p>
        <p><strong>Recomendação:</strong> {msg_recomendacao}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Detalhes adicionais
    with st.expander("📋 Detalhes Adicionais", expanded=False):
        
        # Dados do paciente
        st.write("**Dados do Paciente:**")
        dados_df = pd.DataFrame({
            "Campo": ["Nome", "Idade", "Glicose", "Pressão", "IMC", "Colesterol"],
            "Valor": [
                resultado["nome"],
                resultado["idade"],
                f"{glicose:.1f} mg/dL",
                f"{pressao:.1f} mmHg",
                f"{imc:.1f} kg/m²",
                f"{colesterol:.1f} mg/dL"
            ]
        })
        st.dataframe(dados_df, use_container_width=True, hide_index=True)
        
        # Resultado estruturado
        st.write("**Resultado Estruturado (JSON):**")
        st.json(resultado)
    
    # Opções adicionais
    col_acao1, col_acao2, col_acao3 = st.columns(3)
    
    with col_acao1:
        if st.button("📥 Exportar Resultado (JSON)", use_container_width=True):
            json_str = json.dumps(resultado, indent=2, ensure_ascii=False)
            st.download_button(
                label="⬇️ Baixar JSON",
                data=json_str,
                file_name=f"diagnostico_{resultado['nome']}__{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col_acao2:
        if st.button("🔄 Novo Diagnóstico", use_container_width=True):
            st.session_state.ultimo_resultado = None
            st.rerun()
    
    with col_acao3:
        if st.button("📋 Limpar Formulário", use_container_width=True):
            st.session_state.ultimo_resultado = None
            st.rerun()

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.divider()
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.caption("🏥 Sistema de Diagnóstico de Risco Clínico")

with col_footer2:
    st.caption("💻 Desenvolvido com Streamlit + FastAPI + Machine Learning")

with col_footer3:
    st.caption(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
