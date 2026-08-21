"""
=============================================================================
CHATBOT INTELIGENTE — CLÍNICA DE BIOMEDICINA
=============================================================================
Projeto  : Chatbot para Diagnóstico e Atendimento Clínico
Arquivo  : chatbot_clinica.py
Função   : Chatbot conversacional com IA para diagnóstico de risco clínico

Requisitos:
    pip install streamlit requests pandas python-dotenv

Como rodar:
    streamlit run chatbot_clinica.py

Acesso:
    http://localhost:8501

Características:
    ✅ Conversa natural sobre sintomas
    ✅ Extração inteligente de dados do paciente
    ✅ Integração com modelo ML de diagnóstico
    ✅ Histórico de conversa persistente
    ✅ Recomendações de saúde personalizadas
    ✅ Agendamento de consultas simulado
    ✅ Notificações de risco clínico
=============================================================================
"""

import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import re
from enum import Enum

# ── CONFIGURACAO DA PAGINA ────────────────────────────────────────────────────
st.set_page_config(
    page_title="🤖 Chatbot Clínica Biomedicina",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CONSTANTES ─────────────────────────────────────────────────────────────────
API_URL = "http://localhost:8000"
RISK_LEVELS = {
    "Baixo": "🟢",
    "Médio": "🟡", 
    "Alto": "🔴"
}

# ── CLASSE DE ESTADOS DO CHATBOT ───────────────────────────────────────────────
class ChatState(Enum):
    GREETING = "greeting"
    COLLECTING_SYMPTOMS = "collecting_symptoms"
    COLLECTING_VITALS = "collecting_vitals"
    ANALYSIS = "analysis"
    RECOMMENDATION = "recommendation"
    SCHEDULING = "scheduling"

# ── FUNCOES AUXILIARES ─────────────────────────────────────────────────────────

def extrair_numero(texto, min_val=None, max_val=None):
    """Extrai número do texto do usuário"""
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
    """Extrai palavras-chave de sintomas do texto"""
    palavras_sintomas = {
        'fadiga': ['cansaço', 'fadiga', 'fraco', 'sem energia'],
        'dor': ['dor', 'dolorido', 'dói'],
        'febre': ['febre', 'quente', 'temperatura'],
        'tosse': ['tosse', 'tossindo'],
        'dor_garganta': ['garganta', 'dor garganta'],
        'dor_cabeca': ['cabeça', 'dor de cabeça', 'migranha'],
        'nausea': ['náusea', 'vontade de vomitar'],
        'dispneia': ['falta de ar', 'respiração', 'ofegante'],
    }
    
    sintomas_encontrados = []
    texto_lower = texto.lower()
    
    for sintoma, keywords in palavras_sintomas.items():
        if any(keyword in texto_lower for keyword in keywords):
            sintomas_encontrados.append(sintoma)
    
    return sintomas_encontrados

def gerar_recomendacoes(risco_nivel, sintomas):
    """Gera recomendações personalizadas baseado no risco"""
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
        st.session_state.etapa = ChatState.GREETING.value
    if "diagnostico_feito" not in st.session_state:
        st.session_state.diagnostico_feito = False
    if "historico_consultas" not in st.session_state:
        st.session_state.historico_consultas = []

def adicionar_mensagem(role, conteudo, tipo="texto"):
    """Adiciona mensagem ao histórico"""
    st.session_state.mensagens.append({
        "role": role,
        "conteudo": conteudo,
        "tipo": tipo,
        "timestamp": datetime.now()
    })

def exibir_mensagens():
    """Exibe histórico de mensagens"""
    for msg in st.session_state.mensagens:
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
            if msg["tipo"] == "texto":
                st.write(msg["conteudo"])
            elif msg["tipo"] == "dados":
                st.json(msg["conteudo"])
            elif msg["tipo"] == "alerta":
                st.warning(msg["conteudo"])

# ── LOGICA DO CHATBOT ──────────────────────────────────────────────────────────

def gerar_resposta_chatbot(entrada_usuario):
    """Gera resposta do chatbot baseada no estado e entrada"""
    
    etapa = st.session_state.etapa
    
    # ETAPA 1: SAUDAÇÃO INICIAL
    if etapa == ChatState.GREETING.value:
        if any(palavra in entrada_usuario.lower() for palavra in ['oi', 'olá', 'opa', 'tudo bem']):
            st.session_state.etapa = ChatState.COLLECTING_SYMPTOMS.value
            return """
            👋 Bem-vindo à Clínica de Biomedicina! Sou seu assistente de diagnóstico.

            Vou coletar algumas informações para fazer uma análise preliminar de sua saúde.

            **Primeiro, qual é o seu nome?**
            """
        else:
            return "Olá! Para começar, poderia me cumprimentar dizendo 'Oi' ou 'Olá'?"
    
    # ETAPA 2: COLETA DE INFORMAÇÕES
    elif etapa == ChatState.COLLECTING_SYMPTOMS.value:
        
        # Extrai nome se não tiver
        if not st.session_state.paciente_dados["nome"]:
            # Verifica se é um nome (palavras com capitais ou comprimento razoável)
            palavras = entrada_usuario.split()
            if len(entrada_usuario) > 2 and not re.search(r'\d', entrada_usuario):
                st.session_state.paciente_dados["nome"] = entrada_usuario.strip()
                return f"""
                Prazer em conhecê-lo, **{entrada_usuario}**! 🎉
                
                Agora, por favor, responda:
                
                **Qual é a sua idade?** (em anos)
                """
            else:
                return "Desculpe, não compreendi. Qual é o seu nome?"
        
        # Extrai idade
        elif not st.session_state.paciente_dados["idade"]:
            idade = extrair_numero(entrada_usuario, 18, 120)
            if idade:
                st.session_state.paciente_dados["idade"] = int(idade)
                return f"""
                Ótimo! Você tem {int(idade)} anos.
                
                **Algum sintoma específico que está sentindo?**
                
                (Exemplos: fadiga, dor, febre, tosse, falta de ar, etc.)
                """
            else:
                return "Por favor, digite uma idade válida (entre 18 e 120 anos)."
        
        # Coleta sintomas
        elif not st.session_state.paciente_dados["sintomas"] or "próximo" in entrada_usuario.lower():
            if entrada_usuario.lower() not in ["nenhum", "nada", "não"]:
                sintomas = extrair_sintomas(entrada_usuario)
                st.session_state.paciente_dados["sintomas"].extend(sintomas)
                
                if sintomas:
                    resp = f"Entendi. Você está com: {', '.join(sintomas)}.\n\n"
                else:
                    resp = "Anotado. Vamos coletar seus dados vitais.\n\n"
            else:
                resp = "Tudo bem. Vamos prosseguir com os dados vitais.\n\n"
            
            st.session_state.etapa = ChatState.COLLECTING_VITALS.value
            resp += """
            **Agora preciso de seus dados vitais:**
            
            Por favor, digite ou diga seus valores na ordem:
            - Glicose (mg/dL): ex: 120
            - Pressão Arterial (mmHg): ex: 130
            - IMC (kg/m²): ex: 25.5
            - Colesterol (mg/dL): ex: 200
            """
            return resp
    
    # ETAPA 3: COLETA DE VITAIS
    elif etapa == ChatState.COLLECTING_VITALS.value:
        
        # Tenta extrair números do usuário
        numeros = re.findall(r'\d+\.?\d*', entrada_usuario)
        
        if len(numeros) >= 4:
            st.session_state.paciente_dados["glicose"] = float(numeros[0])
            st.session_state.paciente_dados["pressao"] = float(numeros[1])
            st.session_state.paciente_dados["imc"] = float(numeros[2])
            st.session_state.paciente_dados["colesterol"] = float(numeros[3])
            
            st.session_state.etapa = ChatState.ANALYSIS.value
            
            return """
            ✅ **Dados coletados com sucesso!**
            
            Analisando seus dados... 
            
            Digite **"analisar"** ou **"fazer diagnóstico"** para prosseguir com a análise.
            """
        else:
            return """
            Parece que não consegui extrair todos os 4 valores. 
            
            Por favor, digite em formato: `glicose pressao imc colesterol`
            
            Exemplo: `105 125 26.5 210`
            """
    
    # ETAPA 4: ANÁLISE
    elif etapa == ChatState.ANALYSIS.value:
        
        if any(palavra in entrada_usuario.lower() for palavra in ['analisar', 'diagnóstico', 'fazer', 'começar']):
            
            # Validar dados
            if not all([
                st.session_state.paciente_dados["glicose"],
                st.session_state.paciente_dados["pressao"],
                st.session_state.paciente_dados["imc"],
                st.session_state.paciente_dados["colesterol"]
            ]):
                return "⚠️ Faltam dados! Por favor, complete todos os valores."
            
            # Chamar API
            resultado = chamar_api_diagnostico(st.session_state.paciente_dados)
            
            if "erro" not in resultado:
                st.session_state.diagnostico = resultado
                st.session_state.diagnostico_feito = True
                st.session_state.etapa = ChatState.RECOMMENDATION.value
                
                risco = resultado.get("risco_classificacao", "Desconhecido")
                emoji = RISK_LEVELS.get(risco, "❓")
                
                resposta = f"""
                {emoji} **RESULTADO DA ANÁLISE**
                
                **Classificação de Risco:** {risco}
                
                **Probabilidade:** {resultado.get('probabilidade', 0)*100:.1f}%
                
                **Análise:**
                {resultado.get('explicacao', 'Análise realizada')}
                
                Vou agora fornecer recomendações personalizadas...
                """
                
                if risco == "Alto":
                    resposta = f"🚨 {resposta}"
                
                return resposta
            else:
                return f"❌ Erro ao fazer diagnóstico: {resultado.get('erro')}"
        else:
            return "Digite **'fazer diagnóstico'** para prosseguir com a análise."
    
    # ETAPA 5: RECOMENDAÇÕES
    elif etapa == ChatState.RECOMMENDATION.value:
        
        risco = st.session_state.diagnostico.get("risco_classificacao", "Médio")
        sintomas = st.session_state.paciente_dados["sintomas"]
        
        recomendacoes = gerar_recomendacoes(risco, sintomas)
        
        resp = f"""
        💊 **RECOMENDAÇÕES PERSONALIZADAS**
        
        Baseado na análise de risco {risco.lower()}:
        
        """
        
        for rec in recomendacoes:
            resp += f"\n{rec}"
        
        resp += """
        
        ---
        
        **Próximas ações:**
        
        1. Digite **"agendar"** para marcar uma consulta
        2. Digite **"novo"** para fazer outro diagnóstico
        3. Digite **"histórico"** para ver suas consultas anteriores
        4. Digite **"sair"** para encerrar
        """
        
        st.session_state.etapa = ChatState.SCHEDULING.value
        return resp
    
    # ETAPA 6: AGENDAMENTO
    elif etapa == ChatState.SCHEDULING.value:
        
        if "agendar" in entrada_usuario.lower():
            return """
            📅 **AGENDAMENTO DE CONSULTA**
            
            Ótimo! Vou agendar uma consulta para você.
            
            **Qual especialista você gostaria de consultar?**
            
            1. 👨‍⚕️ Clínico Geral
            2. 💓 Cardiologista
            3. 🩺 Endocrinologista
            4. 🧬 Biomedicina especializada
            
            Digite o número da opção.
            """
        
        elif any(op in entrada_usuario.lower() for op in ['1', 'clínico', 'geral', '2', 'cardio', '3', 'endocr', '4', 'biom']):
            
            especialista_map = {
                '1': 'Clínico Geral',
                '2': 'Cardiologista',
                '3': 'Endocrinologista',
                '4': 'Biomedicina Especializada'
            }
            
            # Encontra a especialidade
            especialista = None
            for num, espec in especialista_map.items():
                if num in entrada_usuario or espec.lower() in entrada_usuario.lower():
                    especialista = espec
                    break
            
            if especialista:
                data_consulta = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")
                horario = "14:30"
                
                consulta = {
                    "paciente": st.session_state.paciente_dados["nome"],
                    "especialista": especialista,
                    "data": data_consulta,
                    "horario": horario,
                    "risco": st.session_state.diagnostico.get("risco_classificacao")
                }
                
                st.session_state.historico_consultas.append(consulta)
                
                return f"""
                ✅ **CONSULTA AGENDADA COM SUCESSO!**
                
                📋 **Detalhes:**
                - **Paciente:** {consulta['paciente']}
                - **Especialista:** {consulta['especialista']}
                - **Data:** {consulta['data']}
                - **Horário:** {consulta['horario']}
                - **Local:** Clínica de Biomedicina
                
                📞 **Confirmação será enviada por SMS**
                
                Qualquer dúvida, entre em contato!
                """
            else:
                return "Por favor, escolha uma especialidade válida (1, 2, 3 ou 4)."
        
        elif "histórico" in entrada_usuario.lower():
            if st.session_state.historico_consultas:
                resp = "📋 **HISTÓRICO DE CONSULTAS**\n\n"
                for i, cons in enumerate(st.session_state.historico_consultas, 1):
                    resp += f"{i}. {cons['paciente']} - {cons['especialista']} ({cons['data']})\n"
                return resp
            else:
                return "Nenhuma consulta agendada ainda."
        
        elif "novo" in entrada_usuario.lower():
            st.session_state.etapa = ChatState.GREETING.value
            st.session_state.paciente_dados = {
                "nome": None,
                "idade": None,
                "glicose": None,
                "pressao": None,
                "imc": None,
                "colesterol": None,
                "sintomas": []
            }
            st.session_state.diagnostico_feito = False
            return "🔄 Novo atendimento iniciado. Digite **'oi'** para começar!"
        
        elif "sair" in entrada_usuario.lower():
            return "Obrigado por usar o Chatbot da Clínica de Biomedicina! Até logo! 👋"
    
    return "Desculpe, não compreendi. Poderia repetir?"

# ── INTERFACE PRINCIPAL ────────────────────────────────────────────────────────

def main():
    inicializar_sessao()
    
    # HEADER
    st.title("🏥 Chatbot Clínica de Biomedicina")
    st.markdown("### Seu assistente de saúde 24/7")
    
    # VERIFICAR CONEXÃO API
    if not conectar_api():
        st.error("❌ **Erro:** API não está respondendo!")
        st.warning("Certifique-se de que a API FastAPI está rodando na porta 8000:")
        st.code("uvicorn 03_API/api_biomedicina:app --port 8000", language="bash")
        return
    
    # SIDEBAR COM INFORMAÇÕES
    with st.sidebar:
        st.header("ℹ️ Informações")
        
        if st.session_state.paciente_dados["nome"]:
            st.success(f"👤 **Paciente:** {st.session_state.paciente_dados['nome']}")
            
            if st.session_state.diagnostico_feito:
                risco = st.session_state.diagnostico.get("risco_classificacao", "?")
                emoji = RISK_LEVELS.get(risco, "❓")
                st.warning(f"{emoji} **Risco:** {risco}")
        
        st.divider()
        
        st.subheader("📊 Valores Inseridos")
        if st.session_state.paciente_dados["idade"]:
            st.write(f"**Idade:** {st.session_state.paciente_dados['idade']} anos")
        if st.session_state.paciente_dados["glicose"]:
            st.write(f"**Glicose:** {st.session_state.paciente_dados['glicose']} mg/dL")
        if st.session_state.paciente_dados["pressao"]:
            st.write(f"**Pressão:** {st.session_state.paciente_dados['pressao']} mmHg")
        if st.session_state.paciente_dados["imc"]:
            st.write(f"**IMC:** {st.session_state.paciente_dados['imc']} kg/m²")
        if st.session_state.paciente_dados["colesterol"]:
            st.write(f"**Colesterol:** {st.session_state.paciente_dados['colesterol']} mg/dL")
        
        st.divider()
        
        if st.button("🔄 Limpar Conversa", key="clear"):
            st.session_state.mensagens = []
            st.session_state.etapa = ChatState.GREETING.value
            st.session_state.paciente_dados = {
                "nome": None,
                "idade": None,
                "glicose": None,
                "pressao": None,
                "imc": None,
                "colesterol": None,
                "sintomas": []
            }
            st.session_state.diagnostico_feito = False
            st.rerun()
    
    # AREA DE CHAT
    container_chat = st.container()
    
    with container_chat:
        # Exibir mensagens anteriores
        exibir_mensagens()
        
        # Se não há mensagens, mandar saudação inicial
        if not st.session_state.mensagens:
            saudacao_inicial = "Bem-vindo à Clínica de Biomedicina! 👋 Como posso ajudá-lo hoje? (Digite 'Oi' para começar)"
            adicionar_mensagem("assistant", saudacao_inicial)
            st.rerun()
    
    # INPUT DO USUARIO
    st.divider()
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        entrada_usuario = st.chat_input("Digite sua mensagem aqui...", key="user_input")
    
    with col2:
        if st.button("📤 Enviar", key="send"):
            entrada_usuario = st.session_state.get("user_input_temp", "")
    
    # PROCESSAR ENTRADA
    if entrada_usuario:
        # Adicionar mensagem do usuário
        adicionar_mensagem("user", entrada_usuario)
        
        # Gerar resposta do chatbot
        resposta = gerar_resposta_chatbot(entrada_usuario)
        adicionar_mensagem("assistant", resposta)
        
        # Recarregar para exibir
        st.rerun()

if __name__ == "__main__":
    main()
