# 🤖 GUIA COMPLETO - CHATBOT CLÍNICA BIOMEDICINA

## 📑 Índice

1. [Visão Geral](#-visão-geral)
2. [Instalação](#-instalação)
3. [Como Usar](#-como-usar)
4. [Exemplos de Conversa](#-exemplos-de-conversa)
5. [Recursos Avançados](#-recursos-avançados)
6. [Troubleshooting](#-troubleshooting)

---

## 🎯 Visão Geral

O **Chatbot Clínica Biomedicina** é um sistema inteligente de atendimento que:

- 🗣️ Conversa naturalmente com pacientes
- 🩺 Coleta dados de saúde de forma intuitiva
- 🤖 Realiza diagnósticos com Machine Learning
- 💊 Fornece recomendações personalizadas
- 📅 Agenda consultas automáticas
- 📊 Mantém histórico de pacientes

---

## 💻 Instalação

### Pré-requisitos
```
✅ Python 3.8+
✅ Virtual Environment configurado
✅ Dependências instaladas
```

### Passo 1: Ativar Virtual Environment
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### Passo 2: Instalar Dependências
```bash
pip install streamlit requests pandas python-dotenv
```

### Passo 3: Executar Sistema Completo

**Opção A - Script Automático (Recomendado)**
```bash
cd PROJETO_SISTEMA_DIAGNOSTICO/09_Scripts_Uteis
./run_chatbot.bat
```

**Opção B - Manualmente (3 terminais)**

Terminal 1 - API:
```bash
cd PROJETO_SISTEMA_DIAGNOSTICO/03_API
python -m uvicorn api_biomedicina:app --port 8000 --reload
```

Terminal 2 - Chatbot:
```bash
cd PROJETO_SISTEMA_DIAGNOSTICO/04_Interface
streamlit run chatbot_clinica.py
```

Terminal 3 (Opcional) - Chatbot PRO com análise:
```bash
cd PROJETO_SISTEMA_DIAGNOSTICO/04_Interface
streamlit run chatbot_clinica_pro.py
```

### Passo 4: Acessar

| Serviço | URL | Descrição |
|---------|-----|-----------|
| Chatbot Básico | http://localhost:8501 | Interface conversacional |
| Chatbot PRO | http://localhost:8502 | Com análise avançada |
| API Docs | http://localhost:8000/docs | Documentação interativa |

---

## 📖 Como Usar

### Fluxo Básico do Chatbot

```
┌─────────────────────────────────────┐
│  1️⃣ SAUDAÇÃO                         │
│  Bot: "Bem-vindo! Qual seu nome?"   │
│  User: "João Silva"                 │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  2️⃣ COLETA DE DADOS                  │
│  Bot: "Qual sua idade?"             │
│  User: "45 anos"                    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  3️⃣ SINTOMAS                         │
│  Bot: "Algum sintoma?"              │
│  User: "Cansaço e dor de cabeça"   │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  4️⃣ VITAIS (Glicose, Pressão, etc)  │
│  User: "105 125 26.5 210"          │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  5️⃣ ANÁLISE                          │
│  User: "Analisar"                   │
│  Bot: 🟡 RISCO MÉDIO - Detalhes...  │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  6️⃣ RECOMENDAÇÕES                    │
│  Bot: Dicas de saúde personalizadas │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  7️⃣ AGENDAMENTO                      │
│  User: "Agendar consulta"           │
│  Bot: Confirma data/hora            │
└─────────────────────────────────────┘
```

### Interações Principais

#### Saudação
```
User: Oi
Bot: 👋 Bem-vindo à Clínica de Biomedicina! 
     Qual é o seu nome?
```

#### Dados Pessoais
```
User: João Silva
Bot: Prazer, João! Qual sua idade?

User: 45
Bot: Ótimo! Algum sintoma específico?
```

#### Sintomas
```
User: Tenho fadiga, dor de cabeça e febre
Bot: Entendi. Vou anotar esses sintomas.
     Agora vamos aos dados vitais...
```

#### Vitais
```
User: 105 125 26.5 210
Bot: ✅ Dados coletados!
     Digite "fazer diagnóstico" para continuar
```

#### Diagnóstico
```
User: Fazer diagnóstico
Bot: 🟡 RESULTADO: RISCO MÉDIO
     Probabilidade: 75%
     Análise: Você apresenta...
```

#### Recomendações
```
Bot: 💊 RECOMENDAÇÕES:
     ✅ Monitorar sinais vitais regularmente
     ✅ Aumentar consumo de fibras
     ✅ Fazer atividade física com moderação
     ✅ Agende consulta em breve
```

#### Agendamento
```
User: Agendar
Bot: 📅 Qual especialista?
     1. Clínico Geral
     2. Cardiologista
     3. Endocrinologista

User: 1
Bot: ✅ Agendado com Clínico Geral em 05/06/2026!
```

---

## 🗨️ Exemplos de Conversa

### Exemplo 1: Paciente com Risco Baixo

```
Bot: Bem-vindo! Qual é o seu nome?
User: Maria Santos

Bot: Prazer, Maria! Qual sua idade?
User: 32

Bot: Algum sintoma específico?
User: Nenhum, só vim fazer check-up

Bot: Ótimo! Digite seus vitais:
User: 85 115 22 180

Bot: ✅ Dados coletados! Digite "fazer diagnóstico"
User: Fazer diagnóstico

Bot: 🟢 RISCO BAIXO
     Probabilidade: 95%
     Você está bem! Mantenha os hábitos saudáveis.
     
💊 RECOMENDAÇÕES:
   ✅ Continue com dieta balanceada
   ✅ Manter atividade física (150 min/semana)
   ✅ Dormir 7-8 horas por noite
   ✅ Fazer check-up anual

Deseja agendar consulta de rotina?
```

### Exemplo 2: Paciente com Risco Médio

```
Bot: Bem-vindo! Qual seu nome?
User: Carlos Alberto

Bot: Qual sua idade?
User: 58 anos

Bot: Algum sintoma?
User: Tenho cansaço constante e às vezes falta de ar

Bot: Entendi. Digite seus vitais:
User: 145 140 29.5 245

Bot: ✅ Dados coletados!
User: Fazer diagnóstico

Bot: 🟡 RESULTADO: RISCO MÉDIO
     Probabilidade: 68%
     Análise: Você apresenta:
     - Glicose elevada (pré-diabetes)
     - Hipertensão estágio 1
     - Sobrepeso
     - Colesterol elevado
     - Faixa etária de risco

💊 RECOMENDAÇÕES:
   ⚠️ Agende consulta com clínico geral em breve
   🏃 Aumentar atividade física (30 min/dia)
   🥗 Reduzir sódio e gorduras
   🚫 Deixar de fumar (se aplicável)
   📊 Fazer exames a cada 6 meses

Deseja agendar consulta?
```

### Exemplo 3: Paciente com Risco Alto

```
Bot: Qual seu nome?
User: Pedro Silva

Bot: Qual sua idade?
User: 72

Bot: Algum sintoma?
User: Dor no peito, falta de ar severa, suor frio

Bot: Digite seus vitais:
User: 285 175 35.2 310

Bot: Fazer diagnóstico
User: Fazendo...

Bot: 🔴 RESULTADO: RISCO ALTO
     Probabilidade: 98%
     
🚨 SITUAÇÃO CRÍTICA!
   - Glicose muito elevada (diabetes descontrolado)
   - Hipertensão severa
   - Obesidade
   - Colesterol muito elevado
   - Sintomas alarmantes reportados

⚠️ AÇÕES IMEDIATAS:
   🚨 PROCURE ATENDIMENTO MÉDICO URGENTE
   📞 Ligue para SAMU: 192
   🏥 Internação pode ser necessária
   💊 Medicação contínua recomendada
   ❌ Evite atividade física
   📊 Monitoramento diário obrigatório

Posso ajudar a chamar assistência?
```

---

## 🚀 Recursos Avançados

### Chatbot PRO (chatbot_clinica_pro.py)

Acesse funcionalidades extras:

#### 1. 💬 Chatbot Tab
- Conversa inteligente
- Extração de dados automática

#### 2. 📊 Histórico Tab
- Visualizar consultas anteriores
- Filtrar por paciente
- Gráficos de evolução

#### 3. 🔍 Análise Tab
- Calculadora de risco avançado
- Pontuação personalizada
- Detalhamento de fatores de risco

#### 4. 📋 Relatórios Tab
- Gerar relatórios completos
- Exportar em JSON
- Análise comparativa

### Dados Persistentes

Os dados de pacientes são salvos em `dados_pacientes/historico_consultas.json`

```json
{
  "nome": "João Silva",
  "idade": 45,
  "glicose": 120,
  "pressao": 140,
  "imc": 26.5,
  "colesterol": 220,
  "risco": "Médio",
  "timestamp": "2026-05-25T20:30:00"
}
```

### Exportar Relatório

1. Ir para aba **📋 Relatórios**
2. Selecionar paciente
3. Clicar **"Gerar Relatório"**
4. Clicar **"Baixar JSON"**

---

## 🔧 Troubleshooting

### ❌ "API não está respondendo"

**Solução:**
```bash
# Terminal 1
cd PROJETO_SISTEMA_DIAGNOSTICO/03_API
python -m uvicorn api_biomedicina:app --port 8000 --reload
```

Verifique: http://localhost:8000/docs

### ❌ "Não consegui extrair os valores"

**Solução:**
Digite números separados por espaço:
```
✅ Correto: 105 125 26.5 210
❌ Errado: glicose 105
```

### ❌ "Erro de conexão"

**Solução:**
1. Verifique internet
2. Feche e reabra terminais
3. Limpe cache Streamlit:
```bash
streamlit cache clear
```

### ❌ "Sintomas não reconhecidos"

**Solução:**
Use palavras-chave conhecidas:
- Fadiga / Cansaço
- Dor
- Febre
- Tosse
- Garganta
- Cabeça
- Náusea
- Respiração / Falta de ar

### ❌ "Porta 8501 já em uso"

**Solução:**
```bash
# Rodar em porta diferente
streamlit run chatbot_clinica.py --server.port 8502
```

### ❌ "Erro ao salvar paciente"

**Solução:**
1. Crie pasta `dados_pacientes/`
2. Verifique permissões de escrita
3. Reinicie aplicação

---

## 📞 Suporte

- **Documentação:** Ver README_CHATBOT.md
- **Clínica:** (11) 1234-5678
- **Email:** suporte@clinica-biomedicina.com
- **Emergência:** 192 (SAMU)

---

## ✅ Checklist de Configuração

- [ ] Python 3.8+ instalado
- [ ] Virtual environment criado e ativado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] API rodando na porta 8000
- [ ] Chatbot rodando na porta 8501
- [ ] Acesso em http://localhost:8501
- [ ] Teste com paciente fictício

---

## 🎓 Dicas e Boas Práticas

### ✅ Faça
- Sempre comece com saudação ("Oi" ou "Olá")
- Forneça dados vitais completos
- Clique em "Analisar" após coletar dados
- Agende consulta quando recomendado

### ❌ Evite
- Misturar dados (use formato: `105 125 26.5 210`)
- Fechar abruptamente os terminais
- Compartilhar dados sem consentimento
- Usar para emergências médicas (ligue 192)

---

**Versão:** 1.0.0
**Data:** Maio 2026
**Desenvolvido para:** Clínica de Biomedicina
