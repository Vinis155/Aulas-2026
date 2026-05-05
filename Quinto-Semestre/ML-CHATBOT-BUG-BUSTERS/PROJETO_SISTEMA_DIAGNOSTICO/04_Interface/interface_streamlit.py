"""
=============================================================================
INTERFACE WEB — SISTEMA DE DIAGNÓSTICO DE RISCO CLÍNICO
=============================================================================
Projeto  : Diagnóstico de Risco Clínico com ML
Arquivo  : interface_streamlit.py
Função   : Fornecer interface web para interação com a API

Requisitos:
    pip install streamlit requests pandas

Como rodar:
    streamlit run interface_streamlit.py

Acesso:
    http://localhost:8501

Pré-requisito:
    A API FastAPI deve estar rodando em http://localhost:8000
=============================================================================
"""

import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime

# ── CONFIGURACAO DA PAGINA ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Diagnóstico de Risco Clínico",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── URL DA API ─────────────────────────────────────────────────────────────────
API_URL = "http://localhost:8000"

# ── TITULO PRINCIPAL ───────────────────────────────────────────────────────────
st.title("🏥 Sistema de Diagnóstico de Risco Clínico")
st.write("Utilize este sistema para fazer o diagnóstico de risco clínico de pacientes baseado em Machine Learning.")

# ── BARRA LATERAL ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📋 Informações")
    
    # Health check da API
    try:
        health_response = requests.get(f"{API_URL}/health", timeout=5)
        if health_response.status_code == 200:
            st.success("✅ API conectada e funcionando")
        else:
            st.error("❌ API não respondendo corretamente")
    except requests.exceptions.ConnectionError:
        st.error("❌ Erro: Não foi possível conectar à API. Certifique-se que ela está rodando em http://localhost:8000")
        st.info("Execute em outro terminal: `uvicorn 03_API/api_biomedicina:app --port 8000`")
    except Exception as e:
        st.error(f"❌ Erro ao conectar à API: {str(e)}")
    
    st.divider()
    
    # Informações do modelo
    st.subheader("🤖 Informações do Modelo")
    try:
        info_response = requests.get(f"{API_URL}/info", timeout=5)
        if info_response.status_code == 200:
            info_data = info_response.json()
            st.write(f"**Modelo:** {info_data.get('nome', 'N/A')}")
            st.write(f"**Acurácia:** {info_data.get('acuracia', 'N/A')}")
            st.write(f"**F1-Score:** {info_data.get('f1_score', 'N/A')}")
            st.write(f"**Val. Cruzada:** {info_data.get('validacao_cruzada', 'N/A')}")
        else:
            st.warning("Não foi possível carregar informações do modelo")
    except:
        st.warning("Não foi possível acessar informações do modelo")
    
    st.divider()
    
    # Valores de referência
    st.subheader("📊 Valores de Referência")
    
    referencia_df = pd.DataFrame({
        "Medida": ["Glicose", "Pressão", "IMC", "Colesterol"],
        "Normal": ["< 100", "< 120", "18-25", "< 200"],
        "Alerta": ["100-125", "120-140", "25-30", "200-240"],
        "Crítico": ["≥ 126", "≥ 140", "≥ 30", "≥ 240"]
    })
    
    st.table(referencia_df)

# ── FORMULARIO PRINCIPAL ───────────────────────────────────────────────────────
st.header("📝 Dados do Paciente")

col1, col2 = st.columns(2)

with col1:
    nome = st.text_input(
        "Nome do paciente",
        value="",
        placeholder="Ex: João Silva"
    )
    idade = st.number_input(
        "Idade (anos)",
        min_value=18,
        max_value=120,
        value=45,
        step=1
    )
    glicose = st.number_input(
        "Glicose (mg/dL)",
        min_value=60.0,
        max_value=350.0,
        value=100.0,
        step=1.0,
        help="Normal: < 100 mg/dL"
    )

with col2:
    pressao = st.number_input(
        "Pressão Arterial Sistólica (mmHg)",
        min_value=80.0,
        max_value=220.0,
        value=120.0,
        step=1.0,
        help="Normal: < 120 mmHg"
    )
    imc = st.number_input(
        "IMC (kg/m²)",
        min_value=15.0,
        max_value=55.0,
        value=25.0,
        step=0.1,
        help="Normal: 18.5-24.9 kg/m²"
    )
    colesterol = st.number_input(
        "Colesterol Total (mg/dL)",
        min_value=100.0,
        max_value=400.0,
        value=200.0,
        step=1.0,
        help="Normal: < 200 mg/dL"
    )

# ── INDICADORES RAPIDOS ────────────────────────────────────────────────────────
st.header("🎯 Indicadores Rápidos")

col_ind1, col_ind2, col_ind3, col_ind4, col_ind5 = st.columns(5)

with col_ind1:
    if glicose < 100:
        st.success(f"✅ Glicose: {glicose:.1f}\n(Normal)")
    elif glicose < 126:
        st.warning(f"⚠️ Glicose: {glicose:.1f}\n(Alerta)")
    else:
        st.error(f"❌ Glicose: {glicose:.1f}\n(Crítico)")

with col_ind2:
    if pressao < 120:
        st.success(f"✅ Pressão: {pressao:.1f}\n(Normal)")
    elif pressao < 140:
        st.warning(f"⚠️ Pressão: {pressao:.1f}\n(Alerta)")
    else:
        st.error(f"❌ Pressão: {pressao:.1f}\n(Crítico)")

with col_ind3:
    if 18.5 <= imc < 25:
        st.success(f"✅ IMC: {imc:.1f}\n(Normal)")
    elif imc < 30:
        st.warning(f"⚠️ IMC: {imc:.1f}\n(Alerta)")
    else:
        st.error(f"❌ IMC: {imc:.1f}\n(Crítico)")

with col_ind4:
    if colesterol < 200:
        st.success(f"✅ Colesterol: {colesterol:.1f}\n(Normal)")
    elif colesterol < 240:
        st.warning(f"⚠️ Colesterol: {colesterol:.1f}\n(Alerta)")
    else:
        st.error(f"❌ Colesterol: {colesterol:.1f}\n(Crítico)")

with col_ind5:
    if idade < 60:
        st.success(f"✅ Idade: {idade}\n(Normal)")
    else:
        st.warning(f"⚠️ Idade: {idade}\n(Fator)")

# ── BOTAO ENVIAR ──────────────────────────────────────────────────────────────
st.divider()

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn2:
    botao_diagnosticar = st.button(
        "🔍 Fazer Diagnóstico",
        use_container_width=True,
        type="primary"
    )

# ── FAZER PREDICAO ─────────────────────────────────────────────────────────────
if botao_diagnosticar:
    # Validações
    if not nome.strip():
        st.error("❌ Por favor, insira o nome do paciente")
    else:
        # Preparar dados
        paciente_dados = {
            "nome": nome,
            "idade": int(idade),
            "glicose": float(glicose),
            "pressao": float(pressao),
            "imc": float(imc),
            "colesterol": float(colesterol)
        }
        
        # Spinner enquanto faz a requisição
        with st.spinner("⏳ Processando diagnóstico..."):
            try:
                response = requests.post(
                    f"{API_URL}/predict",
                    json=paciente_dados,
                    timeout=10
                )
                
                if response.status_code == 200:
                    resultado = response.json()
                    
                    # Armazenar em session state para mostrar
                    st.session_state.ultimo_resultado = resultado
                    st.session_state.timestamp = datetime.now().strftime("%H:%M:%S")
                    
                    # Cores por nível de risco
                    cores_risco = {
                        0: ("green", "Risco Baixo", "✅"),
                        1: ("orange", "Risco Médio", "⚠️"),
                        2: ("red", "Risco Alto", "❌")
                    }
                    
                    risco_code = resultado.get("risco_codigo", -1)
                    cor, label, emoji = cores_risco.get(risco_code, ("gray", "Desconhecido", "❓"))
                    
                    # Mostrar resultado em caixa destacada
                    st.divider()
                    st.header("📊 RESULTADO DO DIAGNÓSTICO")
                    
                    # Container com cor
                    resultado_html = f"""
                    <div style="padding: 20px; border-radius: 10px; 
                                background-color: {'#d4edda' if cor == 'green' else '#fff3cd' if cor == 'orange' else '#f8d7da'};
                                border-left: 5px solid {cor};
                                margin: 20px 0;">
                        <h2 style="color: {cor}; margin: 0;">
                            {emoji} {resultado.get('risco_classificacao', 'N/A')}
                        </h2>
                        <p style="margin: 10px 0; font-size: 14px; color: #333;">
                            Paciente: <strong>{resultado.get('nome', 'N/A')}</strong> ({resultado.get('idade', 'N/A')} anos)
                        </p>
                    </div>
                    """
                    st.markdown(resultado_html, unsafe_allow_html=True)
                    
                    # Probabilidades
                    st.subheader("📈 Probabilidades por Classe")
                    
                    col_prob1, col_prob2, col_prob3 = st.columns(3)
                    
                    # Simular probabilidades por classe (em caso real viria da API)
                    prob_base = resultado.get("probabilidade", 0)
                    
                    with col_prob1:
                        if risco_code == 0:
                            st.metric("Risco Baixo", f"{prob_base*100:.1f}%")
                        else:
                            st.metric("Risco Baixo", "10-20%", delta="-")
                    
                    with col_prob2:
                        if risco_code == 1:
                            st.metric("Risco Médio", f"{prob_base*100:.1f}%")
                        else:
                            st.metric("Risco Médio", "20-40%", delta="-")
                    
                    with col_prob3:
                        if risco_code == 2:
                            st.metric("Risco Alto", f"{prob_base*100:.1f}%")
                        else:
                            st.metric("Risco Alto", "30-50%", delta="-")
                    
                    # Explicação
                    st.subheader("💡 Explicação")
                    st.info(resultado.get("explicacao", "Sem informações adicionais"))
                    
                    # JSON completo
                    st.subheader("📋 Dados Brutos (JSON)")
                    st.json(resultado)
                    
                    # Download dos resultados
                    resultado_json = json.dumps(resultado, indent=2, ensure_ascii=False)
                    st.download_button(
                        label="📥 Baixar resultado (JSON)",
                        data=resultado_json,
                        file_name=f"diagnostico_{resultado.get('nome')}_{st.session_state.timestamp}.json",
                        mime="application/json"
                    )
                
                else:
                    st.error(f"❌ Erro na API: {response.status_code}")
                    st.text(response.text)
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Erro: Não foi possível conectar à API")
                st.warning("Certifique-se que a API está rodando em http://localhost:8000")
            except requests.exceptions.Timeout:
                st.error("❌ Erro: Requisição excedeu o tempo limite")
            except Exception as e:
                st.error(f"❌ Erro inesperado: {str(e)}")

# ── MOSTRAR ULTIMO RESULTADO (se houver) ────────────────────────────────────────
if "ultimo_resultado" in st.session_state:
    # Apenas mostrado se foi processado nesta sessão
    pass  # Já mostrado acima

# ── RODAPE ────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "🏥 Sistema de Diagnóstico de Risco Clínico | "
    "Desenvolvido com Streamlit + FastAPI + Machine Learning | "
    "AULA_08 & AULA_09"
)
