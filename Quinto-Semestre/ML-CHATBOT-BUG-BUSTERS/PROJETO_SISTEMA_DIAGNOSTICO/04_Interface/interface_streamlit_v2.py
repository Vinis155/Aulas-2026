"""
=============================================================================
INTERFACE STREAMLIT v2 — SISTEMA DE DIAGNÓSTICO CLÍNICO COM BANCO DE DADOS
=============================================================================
Projeto  : Sistema de Diagnóstico de Risco Clínico v2.0
Arquivo  : interface_streamlit_v2.py
Função   : Interface completa com login, CRUD, integração com IA

Funcionalidades:
    1. Login (validação com banco SQL)
    2. Menu principal com navegação
    3. Gestão de Exames (CRUD)
    4. Cadastro de Pacientes (CRUD)
    5. Lançamento de Resultados (com IA)
    6. Dashboard com histórico

Como rodar:
    streamlit run 04_Interface/interface_streamlit_v2.py

Pré-requisitos:
    • clinica.db já criado (execute: python 10_Banco_Dados/criar_banco_dados.py)
    • Modelos .pkl já gerados (execute: python 02_ML_Pipeline/2_pipeline_ml.py)
=============================================================================
"""

import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
from typing import Optional, Tuple

# ── CONFIGURAÇÃO DA PÁGINA ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sistema Clínico v2.0",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CAMINHOS ──────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "clinica.db")
MODELO_PATH = os.path.join(BASE_DIR, "..", "06_Modelos", "melhor_modelo.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "..", "06_Modelos", "scaler.pkl")

# ── INICIALIZAÇÃO DE SESSION STATE ────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "usuario_id" not in st.session_state:
    st.session_state.usuario_id = None
if "username" not in st.session_state:
    st.session_state.username = None
if "pagina_atual" not in st.session_state:
    st.session_state.pagina_atual = "Dashboard"

# ── FUNÇÕES DE BANCO DE DADOS ─────────────────────────────────────────────────
def conectar_db():
    """Conecta ao banco de dados SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_senha(senha):
    """Gera hash SHA256 da senha"""
    return hashlib.sha256(senha.encode()).hexdigest()

def validar_login(username: str, senha: str) -> Optional[Tuple[int, str]]:
    """Valida credenciais do usuário. Retorna (id, username) ou None"""
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username FROM usuarios WHERE username = ? AND senha_hash = ? AND ativo = 1",
            (username, hash_senha(senha))
        )
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado:
            return (resultado[0], resultado[1])
        return None
    except Exception as e:
        st.error(f"Erro ao validar login: {str(e)}")
        return None

# ── FUNÇÕES DE PACIENTES ──────────────────────────────────────────────────────
def obter_pacientes():
    """Obtém lista de todos os pacientes"""
    conn = conectar_db()
    df = pd.read_sql_query("SELECT id, nome, idade FROM pacientes WHERE ativo = 1", conn)
    conn.close()
    return df

def adicionar_paciente(nome: str, idade: int):
    """Adiciona novo paciente ao banco"""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pacientes (nome, idade) VALUES (?, ?)",
        (nome, idade)
    )
    conn.commit()
    conn.close()
    return st.success("✅ Paciente adicionado com sucesso!")

def obter_paciente_por_id(paciente_id: int):
    """Obtém dados de um paciente específico"""
    # Garantir que o ID é inteiro
    paciente_id = int(paciente_id)
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, idade, data_cadastro FROM pacientes WHERE id = ?", (paciente_id,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return dict(resultado)
    return None

# ── FUNÇÕES DE EXAMES ─────────────────────────────────────────────────────────
def obter_tipos_exame():
    """Obtém lista de tipos de exame"""
    conn = conectar_db()
    df = pd.read_sql_query("SELECT id, nome, unidade FROM tipos_exame", conn)
    conn.close()
    return df

def obter_tipo_exame_por_id(tipo_exame_id: int):
    """Obtém informações de um tipo de exame"""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tipos_exame WHERE id = ?", (tipo_exame_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def adicionar_exame_paciente(paciente_id: int, tipo_exame_id: int, valor: float):
    """Registra um exame para um paciente"""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO exames_paciente (paciente_id, tipo_exame_id, valor) 
           VALUES (?, ?, ?)""",
        (paciente_id, tipo_exame_id, valor)
    )
    conn.commit()
    conn.close()

def obter_exames_paciente(paciente_id: int):
    """Obtém histórico de exames de um paciente"""
    conn = conectar_db()
    df = pd.read_sql_query("""
        SELECT e.id, te.nome, e.valor, te.unidade, e.data_exame
        FROM exames_paciente e
        JOIN tipos_exame te ON e.tipo_exame_id = te.id
        WHERE e.paciente_id = ?
        ORDER BY e.data_exame DESC
    """, (paciente_id,), conn)
    conn.close()
    return df

# ── FUNÇÕES DE RESULTADOS (IA) ────────────────────────────────────────────────
def carregar_modelo_ml():
    """Carrega o modelo .pkl e scaler"""
    try:
        modelo = joblib.load(MODELO_PATH)
        scaler = joblib.load(SCALER_PATH)
        return modelo, scaler
    except FileNotFoundError:
        st.error("❌ Modelos .pkl não encontrados! Execute 02_ML_Pipeline/2_pipeline_ml.py")
        return None, None

def fazer_predicao_ia(idade: float, glicose: float, pressao: float, imc: float, colesterol: float):
    """Faz predição com o modelo de IA"""
    modelo, scaler = carregar_modelo_ml()
    
    if modelo is None or scaler is None:
        return None
    
    try:
        X = np.array([[idade, glicose, pressao, imc, colesterol]])
        X_normalizado = scaler.transform(X)
        
        classe = modelo.predict(X_normalizado)[0]
        probabilidades = modelo.predict_proba(X_normalizado)[0]
        confianca = float(probabilidades[int(classe)])
        
        return {
            "classe": int(classe),
            "classificacao": ["Baixo", "Médio", "Alto"][int(classe)],
            "confianca": confianca,
            "probabilidades": probabilidades
        }
    except Exception as e:
        st.error(f"Erro ao fazer predição: {str(e)}")
        return None

def salvar_resultado(paciente_id: int, resultado: dict):
    """Salva resultado da análise no banco"""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO resultados (paciente_id, risco_codigo, risco_classificacao, probabilidade)
        VALUES (?, ?, ?, ?)
    """, (paciente_id, resultado["classe"], resultado["classificacao"], resultado["confianca"]))
    conn.commit()
    conn.close()

# ── PÁGINA DE LOGIN ───────────────────────────────────────────────────────────
def pagina_login():
    """Tela de login"""
    st.title("🏥 Sistema de Diagnóstico Clínico v2.0")
    st.subheader("Login")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("")
        st.write("")
        st.write("")
        username = st.text_input("Usuário:", key="login_user")
        senha = st.text_input("Senha:", type="password", key="login_pass")
        
        if st.button("🔐 Entrar", use_container_width=True, type="primary"):
            resultado = validar_login(username, senha)
            if resultado:
                st.session_state.logged_in = True
                st.session_state.usuario_id = resultado[0]
                st.session_state.username = resultado[1]
                st.rerun()
            else:
                st.error("❌ Usuário ou senha incorretos!")
    
    with col2:
        st.info("""
        ### 📋 Credenciais de Teste:
        
        **Admin:**
        - Usuário: admin
        - Senha: admin123
        
        **Médico:**
        - Usuário: medico
        - Senha: medico123
        """)

# ── PÁGINA DE DASHBOARD ───────────────────────────────────────────────────────
def pagina_dashboard():
    """Dashboard principal"""
    st.title("📊 Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    try:
        conn = conectar_db()
        
        with col1:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM pacientes WHERE ativo = 1")
            qtd_pacientes = cursor.fetchone()[0]
            st.metric("Total de Pacientes", qtd_pacientes)
        
        with col2:
            cursor.execute("SELECT COUNT(*) FROM exames_paciente")
            qtd_exames = cursor.fetchone()[0]
            st.metric("Total de Exames", qtd_exames)
        
        with col3:
            cursor.execute("SELECT COUNT(*) FROM resultados")
            qtd_analises = cursor.fetchone()[0]
            st.metric("Análises Realizadas", qtd_analises)
        
        conn.close()
    except Exception as e:
        st.error(f"Erro ao carregar dashboard: {str(e)}")
    
    st.divider()
    
    # Últimas análises
    st.subheader("📈 Últimas Análises")
    try:
        conn = conectar_db()
        df = pd.read_sql_query("""
            SELECT r.id, p.nome, r.risco_classificacao, r.probabilidade, r.data_analise
            FROM resultados r
            JOIN pacientes p ON r.paciente_id = p.id
            ORDER BY r.data_analise DESC
            LIMIT 10
        """, conn)
        conn.close()
        
        if len(df) > 0:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma análise realizada ainda.")
    except Exception as e:
        st.error(f"Erro ao carregar análises: {str(e)}")

# ── PÁGINA DE PACIENTES ───────────────────────────────────────────────────────
def pagina_pacientes():
    """Gestão de pacientes"""
    st.title("👥 Gestão de Pacientes")
    
    tab1, tab2 = st.tabs(["📋 Listar Pacientes", "➕ Novo Paciente"])
    
    with tab1:
        df = obter_pacientes()
        if len(df) > 0:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum paciente cadastrado.")
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome do Paciente:")
            idade = st.number_input("Idade:", min_value=0, max_value=150, value=30)
        
        if st.button("✅ Adicionar Paciente", use_container_width=True, type="primary"):
            if nome.strip():
                adicionar_paciente(nome, idade)
            else:
                st.error("Nome não pode estar vazio!")

# ── PÁGINA DE ANÁLISE COM IA ──────────────────────────────────────────────────
def pagina_analise_ia():
    """Lançamento de resultados com IA"""
    st.title("🤖 Análise de Risco (IA)")
    
    # Selecionar paciente
    df_pacientes = obter_pacientes()
    if len(df_pacientes) == 0:
        st.error("❌ Nenhum paciente cadastrado! Cadastre um paciente primeiro.")
        return
    
    paciente_nome = st.selectbox(
        "Selecione o Paciente:",
        options=df_pacientes["nome"].tolist(),
        key="select_paciente"
    )
    
    paciente_id = int(df_pacientes[df_pacientes["nome"] == paciente_nome]["id"].values[0])
    st.write(f"Debug: Buscando paciente ID {paciente_id}")
    paciente = obter_paciente_por_id(paciente_id)
    
    # Validar se paciente foi encontrado
    if paciente is None:
        st.error(f"❌ Paciente com ID {paciente_id} não encontrado no banco!")
        return
    
    st.divider()
    
    # Mostrar dados do paciente
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Nome:** {paciente['nome']}")
        st.write(f"**ID:** {paciente['id']}")
    with col2:
        st.write(f"**Idade:** {paciente['idade']} anos")
        st.write(f"**Data Cadastro:** {paciente['data_cadastro']}")
    
    st.divider()
    
    # Formulário de medições
    st.subheader("📊 Dados Biomédicos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Usar max_value dinâmico baseado na idade do paciente
        idade_max = max(120, int(paciente['idade']) + 10)
        idade = st.number_input("Idade (anos):", value=int(paciente['idade']), min_value=18, max_value=idade_max)
        glicose = st.number_input("Glicose (mg/dL):", min_value=60.0, max_value=350.0, value=105.0, step=0.1)
        pressao = st.number_input("Pressão Sistólica (mmHg):", min_value=80.0, max_value=220.0, value=120.0, step=0.1)
    
    with col2:
        imc = st.number_input("IMC (kg/m²):", min_value=15.0, max_value=55.0, value=25.0, step=0.1)
        colesterol = st.number_input("Colesterol (mg/dL):", min_value=100.0, max_value=400.0, value=200.0, step=0.1)
    
    st.divider()
    
    # Indicadores rápidos
    st.subheader("🎯 Indicadores de Status")
    
    col_ind1, col_ind2, col_ind3, col_ind4, col_ind5 = st.columns(5)
    
    with col_ind1:
        if glicose < 100:
            st.success(f"✅ Glicose\n{glicose:.1f}\n(Normal)")
        elif glicose < 126:
            st.warning(f"⚠️ Glicose\n{glicose:.1f}\n(Alerta)")
        else:
            st.error(f"❌ Glicose\n{glicose:.1f}\n(Crítico)")
    
    with col_ind2:
        if pressao < 120:
            st.success(f"✅ Pressão\n{pressao:.1f}\n(Normal)")
        elif pressao < 140:
            st.warning(f"⚠️ Pressão\n{pressao:.1f}\n(Alerta)")
        else:
            st.error(f"❌ Pressão\n{pressao:.1f}\n(Crítico)")
    
    with col_ind3:
        if 18.5 <= imc < 25:
            st.success(f"✅ IMC\n{imc:.1f}\n(Normal)")
        elif imc < 30:
            st.warning(f"⚠️ IMC\n{imc:.1f}\n(Alerta)")
        else:
            st.error(f"❌ IMC\n{imc:.1f}\n(Crítico)")
    
    with col_ind4:
        if colesterol < 200:
            st.success(f"✅ Colesterol\n{colesterol:.1f}\n(Normal)")
        elif colesterol < 240:
            st.warning(f"⚠️ Colesterol\n{colesterol:.1f}\n(Alerta)")
        else:
            st.error(f"❌ Colesterol\n{colesterol:.1f}\n(Crítico)")
    
    with col_ind5:
        if idade < 60:
            st.success(f"✅ Idade\n{idade}\n(Normal)")
        else:
            st.warning(f"⚠️ Idade\n{idade}\n(Fator)")
    
    st.divider()
    
    # Botão de análise
    if st.button("🔍 Analisar com IA", use_container_width=True, type="primary"):
        with st.spinner("Analisando dados..."):
            resultado = fazer_predicao_ia(idade, glicose, pressao, imc, colesterol)
        
        if resultado:
            # Salvar resultado
            salvar_resultado(paciente_id, resultado)
            
            # Mostrar resultado
            st.divider()
            
            cores_risco = {
                0: ("green", "Risco Baixo", "✅"),
                1: ("orange", "Risco Médio", "⚠️"),
                2: ("red", "Risco Alto", "❌")
            }
            
            cor, label, emoji = cores_risco[resultado["classe"]]
            
            resultado_html = f"""
            <div style="padding: 20px; border-radius: 10px; 
                        background-color: {'#d4edda' if cor == 'green' else '#fff3cd' if cor == 'orange' else '#f8d7da'};
                        border-left: 5px solid {cor};
                        margin: 20px 0;">
                <h2 style="color: {cor}; margin: 0;">
                    {emoji} {label}
                </h2>
                <p style="margin: 10px 0; font-size: 14px;">
                    Confiança: <strong>{resultado['confianca']*100:.1f}%</strong>
                </p>
            </div>
            """
            st.markdown(resultado_html, unsafe_allow_html=True)
            
            # Probabilidades por classe
            col_prob1, col_prob2, col_prob3 = st.columns(3)
            with col_prob1:
                st.metric("Risco Baixo", f"{resultado['probabilidades'][0]*100:.1f}%")
            with col_prob2:
                st.metric("Risco Médio", f"{resultado['probabilidades'][1]*100:.1f}%")
            with col_prob3:
                st.metric("Risco Alto", f"{resultado['probabilidades'][2]*100:.1f}%")

# ── PÁGINA PRINCIPAL ──────────────────────────────────────────────────────────
def main():
    """Aplicação principal"""
    
    # Se não está logado, mostrar login
    if not st.session_state.logged_in:
        pagina_login()
        return
    
    # Menu lateral
    with st.sidebar:
        st.title(f"👋 Bem-vindo, {st.session_state.username}!")
        st.divider()
        
        pagina = st.radio(
            "Navegação:",
            options=["Dashboard", "Pacientes", "Análise de Risco"],
            key="nav_menu"
        )
        
        st.divider()
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.usuario_id = None
            st.session_state.username = None
            st.rerun()
    
    # Renderizar página selecionada
    if pagina == "Dashboard":
        pagina_dashboard()
    elif pagina == "Pacientes":
        pagina_pacientes()
    elif pagina == "Análise de Risco":
        pagina_analise_ia()

if __name__ == "__main__":
    main()
