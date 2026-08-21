"""
=============================================================================
CHATBOT COM IA GEMINI — CLÍNICA DE BIOMEDICINA
=============================================================================
Projeto  : Chatbot para Diagnóstico e Atendimento Clínico com IA Gemini
Arquivo  : chatbot_clinica_gemini.py
Função   : Chatbot conversacional com IA Google Gemini para diálogos naturais

Requisitos:
    pip install streamlit requests pandas python-dotenv google-generativeai

Como rodar:
    streamlit run chatbot_clinica_gemini.py

Acesso:
    http://localhost:8501

Características:
    ✅ Conversa natural com IA Gemini
    ✅ Extração inteligente de dados do paciente
    ✅ Análise contextual de sintomas
    ✅ Integração com modelo ML de diagnóstico
    ✅ Recomendações personalizadas baseadas em IA
    ✅ Histórico de conversa persistente
    ✅ Agendamento de consultas simulado
    ✅ Notificações de risco clínico
=============================================================================
"""

import streamlit as st
import requests
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Importar Google Gemini
try:
    import google.generativeai as genai
    GEMINI_DISPONIVEL = True
except ImportError:
    GEMINI_DISPONIVEL = False
    st.warning("⚠️ google-generativeai não instalado. Execute: pip install google-generativeai")

# ── CONFIGURACAO ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🤖 Chatbot Gemini - Clínica Biomedicina",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar variáveis de ambiente
load_dotenv()

API_URL = "http://localhost:8000"
DATA_DIR = Path("dados_pacientes")
DATA_DIR.mkdir(exist_ok=True)

RISK_LEVELS = {
    "Baixo": "🟢",
    "Médio": "🟡",
    "Alto": "🔴"
}

# ── CONFIGURAR GEMINI ──────────────────────────────────────────────────────

def configurar_gemini():
    """Configura a API do Gemini"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        return None, "Chave GEMINI_API_KEY não encontrada em variáveis de ambiente"
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        return model, None
    except Exception as e:
        return None, f"Erro ao configurar Gemini: {str(e)}"

# ── FUNÇÕES AUXILIARES ─────────────────────────────────────────────────────

def chamar_gemini(prompt, model):
    """Chama a API Gemini para gerar resposta"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Erro ao chamar Gemini: {str(e)}"

def gerar_prompt_chatbot(entrada_usuario, contexto_paciente, estado_conversa):
    """Gera prompt otimizado para o Gemini"""
    
    prompt = f"""Você é um assistente de saúde profissional em uma clínica de biomedicina.
Seu objetivo é fazer triagem de pacientes para diagnóstico de risco clínico.

CONTEXTO ATUAL:
- Paciente: {contexto_paciente.get('nome', 'Novo paciente')}
- Idade: {contexto_paciente.get('idade', 'Não informada')}
- Sintomas já informados: {', '.join(contexto_paciente.get('sintomas', [])) or 'Nenhum'}
- Dados vitais coletados: {contexto_paciente.get('vitais_coletados', False)}
- Etapa da conversa: {estado_conversa}

INSTRUÇÕES:
1. Seja empático e profissional
2. Faça perguntas claras e objetivas
3. Se o paciente relatar sintomas graves (dor no peito, falta de ar severa, etc), avise para procurar emergência
4. Colete informações de forma natural na conversa
5. Não faça diagnósticos, apenas triagem
6. Se tiver todos os dados (nome, idade, glicose, pressão, imc, colesterol), indique ao paciente)

ENTRADA DO PACIENTE: {entrada_usuario}

Responda de forma concisa (máximo 150 palavras), natural e conversacional.
Se for pedir informação, deixe claro o que precisa.
"""
    
    return prompt

def extrair_numero(texto, min_val=None, max_val=None):
    """Extrai número do texto"""
    try:
        numeros = re.findall(r'\d+\.?\d*', texto)
        if numeros:
            valor = float(numeros[0])
            if min_val and valor < min_val:
                return None
            if max_val and valor > max_val:
                return None
            return valor
    except:
        pass
    return None

def conectar_api():
    """Verifica conexão com API"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def chamar_api_diagnostico(dados_paciente):
    """Chama API para fazer diagnóstico"""
    try:
        response = requests.post(
            f"{API_URL}/diagnostico",
            json=dados_paciente,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"erro": f"Erro na API: {response.status_code}"}
    except Exception as e:
        return {"erro": f"Erro ao conectar com API: {str(e)}"}

def extrair_sintomas(texto):
    """Extrai sintomas do texto"""
    palavras_sintomas = {
        'fadiga': ['cansaço', 'fadiga', 'fraco', 'sem energia', 'exausto'],
        'dor': ['dor', 'dolorido', 'dói', 'dorem'],
        'febre': ['febre', 'quente', 'temperatura', 'com febre'],
        'tosse': ['tosse', 'tossindo', 'tosse seca', 'tosse com catarro'],
        'dor_garganta': ['garganta', 'dor garganta', 'garganta inflamada'],
        'dor_cabeca': ['cabeça', 'dor de cabeça', 'migranha', 'cefaleia'],
        'nausea': ['náusea', 'vontade de vomitar', 'ânsia', 'feeling'],
        'dispneia': ['falta de ar', 'respiração', 'ofegante', 'difícil respirar'],
        'dor_peito': ['peito', 'dor no peito', 'aperto no peito', 'angina'],
    }
    
    sintomas_encontrados = []
    texto_lower = texto.lower()
    
    for sintoma, keywords in palavras_sintomas.items():
        if any(keyword in texto_lower for keyword in keywords):
            sintomas_encontrados.append(sintoma.replace('_', ' '))
    
    return sintomas_encontrados

def gerar_recomendacoes(risco_nivel, sintomas):
    """Gera recomendações personalizadas"""
    recomendacoes = {
        "Baixo": [
            "✅ Mantenha uma dieta balanceada e equilibrada",
            "🏃 Faça 150 minutos de atividade física por semana",
            "💤 Durma de 7-8 horas por noite",
            "💧 Beba bastante água (2-3 litros por dia)",
            "🚫 Evite fumar e limitar álcool"
        ],
        "Médio": [
            "⚠️ Agendar consulta com clínico geral em breve",
            "🏥 Monitorar sinais vitais regularmente",
            "🥗 Aumentar consumo de fibras e frutas",
            "🏃 Realizar atividades físicas com moderação",
            "📊 Fazer exames periódicos (a cada 6 meses)"
        ],
        "Alto": [
            "🚨 PROCURAR ATENDIMENTO MÉDICO URGENTEMENTE",
            "📞 Contato de Emergência: 192 (SAMU)",
            "🏥 Internação recomendada para monitoramento",
            "💊 Pode ser necessário medicação contínua",
            "📋 Agendar consulta urgente com cardiologista/endocrinologista"
        ]
    }
    
    return recomendacoes.get(risco_nivel, recomendacoes["Médio"])

def salvar_consulta(dados_consulta):
    """Salva consulta em JSON"""
    arquivo = DATA_DIR / "historico_consultas.json"
    
    historico = []
    if arquivo.exists():
        with open(arquivo, 'r', encoding='utf-8') as f:
            historico = json.load(f)
    
    dados_consulta['timestamp'] = datetime.now().isoformat()
    historico.append(dados_consulta)
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

def inicializar_sessao():
    """Inicializa variáveis de sessão"""
    if "mensagens" not in st.session_state:
        st.session_state.mensagens = []
    if "paciente_dados" not in st.session_state:
        st.session_state.paciente_dados = {
            "nome": None,
            "idade": None,
            "glicose": None,
            "pressao": None,
            "imc": None,
            "colesterol": None,
            "sintomas": []
        }
    if "etapa" not in st.session_state:
        st.session_state.etapa = "inicial"
    if "diagnostico_feito" not in st.session_state:
        st.session_state.diagnostico_feito = False
    if "model_gemini" not in st.session_state:
        model, erro = configurar_gemini()
        st.session_state.model_gemini = model
        st.session_state.erro_gemini = erro

def adicionar_mensagem(role, conteudo):
    """Adiciona mensagem ao histórico"""
    st.session_state.mensagens.append({
        "role": role,
        "conteudo": conteudo,
        "timestamp": datetime.now()
    })

def exibir_mensagens():
    """Exibe histórico de mensagens"""
    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
            st.write(msg["conteudo"])

# ── LÓGICA DO CHATBOT COM GEMINI ───────────────────────────────────────────

def gerar_resposta_chatbot_gemini(entrada_usuario, model):
    """Gera resposta usando Gemini com contexto da triagem"""
    
    # Verificar sintomas graves
    if any(grave in entrada_usuario.lower() for grave in ['dor no peito', 'falta de ar', 'suor frio', 'desmaio']):
        return "🚨 **ALERTA!** Você relatou sintomas graves. **PROCURE EMERGÊNCIA IMEDIATAMENTE!** Ligue para 192 (SAMU) ou vá ao pronto-socorro mais próximo. Sua vida pode estar em risco."
    
    # Gerar prompt contextualizado
    prompt = gerar_prompt_chatbot(
        entrada_usuario,
        st.session_state.paciente_dados,
        st.session_state.etapa
    )
    
    # Chamar Gemini
    resposta = chamar_gemini(prompt, model)
    
    # Extrair dados da resposta (parsing inteligente)
    if st.session_state.paciente_dados["nome"] is None and len(entrada_usuario) > 2:
        # Tenta extrair nome
        if not any(char.isdigit() for char in entrada_usuario):
            st.session_state.paciente_dados["nome"] = entrada_usuario.strip()
    
    # Extrair idade
    idade = extrair_numero(entrada_usuario, 18, 120)
    if idade and st.session_state.paciente_dados["idade"] is None:
        st.session_state.paciente_dados["idade"] = int(idade)
    
    # Extrair sintomas
    sintomas = extrair_sintomas(entrada_usuario)
    if sintomas:
        st.session_state.paciente_dados["sintomas"].extend(sintomas)
        st.session_state.paciente_dados["sintomas"] = list(set(st.session_state.paciente_dados["sintomas"]))
    
    # Extrair vitais (glicose pressao imc colesterol)
    if any(op in entrada_usuario.lower() for op in ['vitais', 'dados']):
        numeros = re.findall(r'\d+\.?\d*', entrada_usuario)
        if len(numeros) >= 4:
            st.session_state.paciente_dados["glicose"] = float(numeros[0])
            st.session_state.paciente_dados["pressao"] = float(numeros[1])
            st.session_state.paciente_dados["imc"] = float(numeros[2])
            st.session_state.paciente_dados["colesterol"] = float(numeros[3])
    
    # Atualizar etapa
    if st.session_state.paciente_dados["nome"]:
        st.session_state.etapa = "coletando_dados"
    
    # Se tem todos dados, permitir diagnóstico
    if all([st.session_state.paciente_dados["glicose"],
            st.session_state.paciente_dados["pressao"],
            st.session_state.paciente_dados["imc"],
            st.session_state.paciente_dados["colesterol"]]):
        st.session_state.etapa = "pronto_diagnostico"
    
    return resposta

def fazer_diagnostico_ml():
    """Faz diagnóstico com ML e retorna resultado"""
    resultado = chamar_api_diagnostico(st.session_state.paciente_dados)
    
    if "erro" not in resultado:
        st.session_state.diagnostico_feito = True
        return resultado
    else:
        return None

# ── INTERFACE PRINCIPAL ────────────────────────────────────────────────────

def main():
    inicializar_sessao()
    
    # VERIFICAR GEMINI
    if not GEMINI_DISPONIVEL or st.session_state.model_gemini is None:
        st.error("❌ **Erro:** Gemini não disponível!")
        if st.session_state.erro_gemini:
            st.error(st.session_state.erro_gemini)
        st.info("📝 Instruções de instalação:")
        st.code("pip install google-generativeai", language="bash")
        return
    
    # HEADER
    st.title("🏥 Chatbot com IA Gemini - Clínica Biomedicina")
    st.markdown("### Seu assistente de saúde 24/7 com Inteligência Artificial 🤖")
    
    # VERIFICAR CONEXÃO API
    if not conectar_api():
        st.error("❌ **Erro:** API não está respondendo!")
        st.warning("Certifique-se de que a API FastAPI está rodando na porta 8000:")
        st.code("cd PROJETO_SISTEMA_DIAGNOSTICO/03_API\npython -m uvicorn api_biomedicina:app --port 8000", language="bash")
        return
    
    # SIDEBAR
    with st.sidebar:
        st.header("ℹ️ Informações do Paciente")
        
        if st.session_state.paciente_dados["nome"]:
            st.success(f"👤 **Paciente:** {st.session_state.paciente_dados['nome']}")
            
            if st.session_state.diagnostico_feito:
                st.info(f"✅ Diagnóstico realizado com sucesso")
        
        st.divider()
        
        st.subheader("📊 Dados Coletados")
        
        cols = st.columns(2)
        with cols[0]:
            if st.session_state.paciente_dados["idade"]:
                st.write(f"**Idade:** {st.session_state.paciente_dados['idade']} anos")
            if st.session_state.paciente_dados["glicose"]:
                st.write(f"**Glicose:** {st.session_state.paciente_dados['glicose']} mg/dL")
            if st.session_state.paciente_dados["imc"]:
                st.write(f"**IMC:** {st.session_state.paciente_dados['imc']} kg/m²")
        
        with cols[1]:
            if st.session_state.paciente_dados["pressao"]:
                st.write(f"**Pressão:** {st.session_state.paciente_dados['pressao']} mmHg")
            if st.session_state.paciente_dados["colesterol"]:
                st.write(f"**Colesterol:** {st.session_state.paciente_dados['colesterol']} mg/dL")
        
        if st.session_state.paciente_dados["sintomas"]:
            st.write(f"**Sintomas:** {', '.join(st.session_state.paciente_dados['sintomas'])}")
        
        st.divider()
        
        if st.button("🔄 Nova Conversa", key="nova"):
            st.session_state.mensagens = []
            st.session_state.paciente_dados = {
                "nome": None, "idade": None, "glicose": None,
                "pressao": None, "imc": None, "colesterol": None,
                "sintomas": []
            }
            st.session_state.etapa = "inicial"
            st.session_state.diagnostico_feito = False
            st.rerun()
    
    # AREA DE CHAT
    st.subheader("💬 Conversa")
    
    # Exibir mensagens anteriores
    exibir_mensagens()
    
    # Se não há mensagens, mandar saudação inicial
    if not st.session_state.mensagens:
        saudacao = "Olá! 👋 Bem-vindo à Clínica de Biomedicina! Sou seu assistente de saúde com IA. Como posso ajudá-lo hoje?"
        adicionar_mensagem("assistant", saudacao)
        st.rerun()
    
    # INPUT DO USUARIO
    st.divider()
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        entrada_usuario = st.chat_input("Digite sua mensagem...", key="user_input")
    
    # PROCESSAR ENTRADA
    if entrada_usuario:
        # Adicionar mensagem do usuário
        adicionar_mensagem("user", entrada_usuario)
        
        # Gerar resposta com Gemini
        resposta = gerar_resposta_chatbot_gemini(entrada_usuario, st.session_state.model_gemini)
        adicionar_mensagem("assistant", resposta)
        
        # Se temos todos os dados e usuário pediu diagnóstico
        if "diagnóstico" in entrada_usuario.lower() or "diagnostico" in entrada_usuario.lower():
            if all([st.session_state.paciente_dados["glicose"],
                    st.session_state.paciente_dados["pressao"],
                    st.session_state.paciente_dados["imc"],
                    st.session_state.paciente_dados["colesterol"]]):
                
                with st.spinner("Analisando dados com ML..."):
                    resultado = fazer_diagnostico_ml()
                    
                    if resultado:
                        risco = resultado.get("risco_classificacao", "Desconhecido")
                        emoji = RISK_LEVELS.get(risco, "❓")
                        prob = resultado.get("probabilidade", 0) * 100
                        
                        msg_diagnostico = f"""
{emoji} **RESULTADO DA ANÁLISE**

**Classificação de Risco:** {risco}
**Probabilidade:** {prob:.1f}%

**Análise:** {resultado.get('explicacao', 'Análise realizada')}

💊 **RECOMENDAÇÕES PERSONALIZADAS:**
"""
                        recomendacoes = gerar_recomendacoes(risco, st.session_state.paciente_dados["sintomas"])
                        for rec in recomendacoes:
                            msg_diagnostico += f"\n{rec}"
                        
                        adicionar_mensagem("assistant", msg_diagnostico)
                        
                        # Salvar consulta
                        salvar_consulta({
                            "nome": st.session_state.paciente_dados["nome"],
                            "idade": st.session_state.paciente_dados["idade"],
                            "glicose": st.session_state.paciente_dados["glicose"],
                            "pressao": st.session_state.paciente_dados["pressao"],
                            "imc": st.session_state.paciente_dados["imc"],
                            "colesterol": st.session_state.paciente_dados["colesterol"],
                            "risco": risco,
                            "sintomas": st.session_state.paciente_dados["sintomas"]
                        })
        
        st.rerun()
    
    # INFO DE SEGURANÇA
    st.info(
        "⚠️ **DISCLAIMER:** Este chatbot é para triagem apenas. "
        "Não substitui consulta médica profissional. Em caso de emergência, ligue 192 (SAMU)."
    )

if __name__ == "__main__":
    main()
