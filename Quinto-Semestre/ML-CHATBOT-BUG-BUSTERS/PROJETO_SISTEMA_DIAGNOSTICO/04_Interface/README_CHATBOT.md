# 🤖 Chatbot Clínica de Biomedicina

## 📋 Visão Geral

Um **chatbot inteligente e conversacional** projetado para atendimento em clínica de biomedicina. Combina **processamento de linguagem natural** com **machine learning** para fornecer diagnósticos de risco clínico personalizados.

## ✨ Características Principais

### 🎯 Conversação Natural
- Interface conversacional intuitiva
- Compreensão de linguagem natural
- Histórico de conversa persistente
- Sugestões contextuais

### 🏥 Diagnóstico Inteligente
- Extração automática de sintomas
- Coleta estruturada de dados vitais
- Integração com modelo ML de diagnóstico
- Classificação de risco (Baixo/Médio/Alto)

### 💊 Recomendações Personalizadas
- Recomendações baseadas no nível de risco
- Dicas de saúde preventiva
- Alerta de urgência para risco alto
- Sugestões de especialistas

### 📅 Agendamento de Consultas
- Agendamento automático com especialistas
- Seleção de especialidade
- Confirmação de data e horário
- Histórico de consultas

### 📊 Monitoramento de Saúde
- Rastreamento de vitais
- Análise comparativa de métricas
- Avisos de valores fora da normalidade
- Recomendações de acompanhamento

## 🚀 Como Executar

### Opção 1: Script Automático (Recomendado)
```bash
# Windows
.\run_chatbot.bat

# Linux/Mac
bash run_chatbot.sh
```

### Opção 2: Manualmente
```bash
# Terminal 1 - API
cd PROJETO_SISTEMA_DIAGNOSTICO/03_API
python -m uvicorn api_biomedicina:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Chatbot
cd PROJETO_SISTEMA_DIAGNOSTICO/04_Interface
streamlit run chatbot_clinica.py
```

## 📖 Fluxo de Conversa

```
1. Saudação
   └─ Bot: "Bem-vindo! Qual é o seu nome?"

2. Coleta de Dados
   ├─ Nome do paciente
   ├─ Idade
   ├─ Sintomas (linguagem natural)
   └─ Dados vitais (glicose, pressão, IMC, colesterol)

3. Análise
   └─ Bot faz diagnóstico via ML
   └─ Retorna classificação de risco

4. Recomendações
   ├─ Dicas de saúde personalizadas
   ├─ Alerta de urgência (se necessário)
   └─ Sugestões de especialista

5. Agendamento
   ├─ Seleção de especialidade
   ├─ Confirmação de data/horário
   └─ Opções de próximas ações
```

## 🎨 Interface

### Painel Lateral
- Status do paciente
- Valores inseridos
- Classificação de risco (com emoji)
- Botão de limpeza de conversa

### Área de Chat
- Histórico completo de mensagens
- Timestamps de interações
- Exibição clara de dados

### Input
- Campo de texto para mensagens
- Botão de envio
- Processamento em tempo real

## 🧠 Extração de Dados Inteligente

### Reconhecimento de Sintomas
O chatbot reconhece automaticamente sintomas como:
- Fadiga / Cansaço
- Dor (geral ou específica)
- Febre
- Tosse
- Dor de garganta
- Dor de cabeça
- Náusea
- Falta de ar

### Extração de Números
Aceita dados em vários formatos:
```
Exemplos:
- "105 125 26.5 210"
- "glicose 105, pressão 125, imc 26.5, colesterol 210"
- Digitação de um por um
```

## 🔐 Segurança & Privacidade

- Dados armazenados localmente
- Histórico de consultas privado
- Sem envio de dados sensíveis (exceto para API)
- Avisos sobre situações críticas

## 📊 Categorias de Risco

### 🟢 Risco Baixo
- Recomendações: Atividades preventivas
- Acompanhamento: Anual
- Ações: Consulta de rotina

### 🟡 Risco Médio
- Recomendações: Monitoramento aumentado
- Acompanhamento: Semestral
- Ações: Consulta em breve

### 🔴 Risco Alto
- Recomendações: Atenção médica urgente
- Acompanhamento: Mensal
- Ações: Consulta urgente ou emergência

## 🎯 Casos de Uso

### Triagem Inicial
O chatbot realiza uma triagem inicial antes de consulta presencial

### Monitoramento Remoto
Pacientes podem fazer check-ups do próprio domicílio

### Educação em Saúde
Fornece dicas e recomendações preventivas

### Agendamento 24/7
Possibilita agendamento em qualquer hora

### Histórico de Pacientes
Mantém registro de todos os atendimentos

## 🛠️ Requisitos

```
streamlit>=1.0.0
requests>=2.26.0
pandas>=1.3.0
python>=3.8
```

## 🚨 Troubleshooting

### Erro: "API não está respondendo"
- Verifique se API está rodando na porta 8000
- Execute: `uvicorn 03_API/api_biomedicina:app --port 8000`

### Erro: "Não consegui extrair os valores"
- Digite números separados por espaços
- Exemplo: `105 125 26.5 210`

### Chat lento
- Verifique conexão de internet
- Reinicie os terminais
- Limpe o cache do Streamlit

## 📞 Contato & Suporte

- **Clínica:** 📞 (11) 1234-5678
- **Email:** contato@clinica-biomedicina.com
- **Emergência:** 192 (SAMU)

## 📝 Exemplos de Conversa

### Exemplo 1: Paciente com Risco Médio
```
Usuario: Oi
Bot: Bem-vindo! Qual é o seu nome?

Usuario: Maria Silva
Bot: Prazer, Maria! Qual é sua idade?

Usuario: 45 anos
Bot: Ótimo! Algum sintoma?

Usuario: Cansaço e dor de cabeça
Bot: Entendi. Digite seus vitais: glicose pressão imc colesterol

Usuario: 120 140 28 220
Bot: ✅ Dados coletados! Digite "analisar"

Usuario: analisar
Bot: 🟡 RISCO MÉDIO - Recomendações: [...]
```

## 🔮 Futuras Melhorias

- [ ] Integração com chatGPT para respostas mais naturais
- [ ] Suporte a múltiplos idiomas
- [ ] Notificações por SMS/Email
- [ ] Dashboard de dashboard para profissionais
- [ ] Integração com prontuário eletrônico
- [ ] Telemedicina com vídeo
- [ ] IA mais avançada com LLM

---

**Desenvolvido para:** Clínica de Biomedicina
**Versão:** 1.0.0
**Data:** Maio 2026
