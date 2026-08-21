# 🤖 CHATBOT COM IA GEMINI - CLÍNICA BIOMEDICINA

## 📋 Visão Geral

**Chatbot inteligente de atendimento clínico** que usa a **IA Google Gemini** para conversas naturais e compreensão contextual de sintomas.

Combina:
- 🤖 **IA Gemini** para respostas naturais
- 🧠 **ML Random Forest** para diagnóstico de risco (98.75% acurácia)
- 💬 **Processamento de Linguagem Natural** para extração de dados
- 📊 **Análise contextual** de sintomas e sinais vitais

---

## 🚀 Início Rápido

### Opção 1: Automática (Recomendado)
```bash
# Execute o script que faz tudo
PROJETO_SISTEMA_DIAGNOSTICO/09_Scripts_Uteis/run_chatbot_gemini.bat
```

### Opção 2: Manual

**Terminal 1 - API:**
```bash
cd PROJETO_SISTEMA_DIAGNOSTICO/03_API
python -m uvicorn api_biomedicina:app --port 8000
```

**Terminal 2 - Chatbot Gemini:**
```bash
cd PROJETO_SISTEMA_DIAGNOSTICO/04_Interface
streamlit run chatbot_clinica_gemini.py
```

---

## 🔧 Configuração Chave Gemini

### Passo 1: Obter Chave
1. Acesse: https://aistudio.google.com/app/apikey
2. Faça login com Google
3. Click "Create API Key"
4. Copie a chave

### Passo 2: Criar Arquivo `.env`

Na **raiz do projeto** (ML-CHATBOT-BUG-BUSTERS/), crie arquivo `.env`:

```bash
GEMINI_API_KEY=sua_chave_aqui
```

**Exemplo:**
```
GEMINI_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
```

**Localização:**
```
ML-CHATBOT-BUG-BUSTERS/
├── .env                    ← COLOCAR AQUI ✅
├── CONFIGURACAO_GEMINI.md  ← Guia detalhado
├── INICIO_RAPIDO_GEMINI.md ← Guia rápido
├── PROJETO_SISTEMA_DIAGNOSTICO/
└── ...
```

### Passo 3: Instalar Dependências

```bash
pip install google-generativeai python-dotenv streamlit requests
```

Ou se estiver usando o arquivo requirements.txt:
```bash
pip install -r requirements.txt
```

---

## 💬 Como Usar

### Fluxo de Conversa

```
1. Bot: "Olá! Bem-vindo à Clínica."
   User: "Oi"

2. Bot: "Qual é o seu nome?"
   User: "João Silva"

3. Bot: "Prazer João! Qual sua idade?"
   User: "45 anos"

4. Bot: "Qual é o problema? Descreva seus sintomas."
   User: "Tenho fadiga, dor de cabeça e febre"

5. Bot: "Entendi. Digite seus dados vitais:
          glicose pressão imc colesterol"
   User: "105 125 26.5 210"

6. Bot: "Obrigado! Gostaria de fazer um diagnóstico agora?"
   User: "Sim, fazer diagnóstico"

7. Bot: "🟡 RESULTADO: RISCO MÉDIO
          Recomendações: [...]"
```

### Exemplo de Conversa Completa

#### Cenário 1: Risco Baixo ✅

```
User: Oi
Bot: Bem-vindo à Clínica de Biomedicina! Sou seu assistente de saúde com IA.
     Como posso ajudá-lo hoje?

User: Quero fazer um check-up
Bot: Ótimo! Vamos fazer uma avaliação rápida.
     Qual é o seu nome?

User: Maria Santos
Bot: Prazer Maria! Qual sua idade?

User: 32 anos
Bot: E como se sente? Algum sintoma específico?

User: Nenhum, só quero verificar minha saúde
Bot: Perfeito! Vamos aos dados vitais então.
     Digite: glicose, pressão arterial, IMC, colesterol
     Ex: 85 115 22 180

User: 85 115 22 180
Bot: Excelente! Vou fazer a análise agora.

User: Fazer diagnóstico
Bot: 🟢 RESULTADO: RISCO BAIXO
     Probabilidade: 95%
     
     Você está bem! Mantenha seus hábitos saudáveis.
     
     💊 RECOMENDAÇÕES:
        ✅ Continue com dieta balanceada
        ✅ Manter 150 min de atividade física por semana
        ✅ Dormir 7-8 horas por noite
        ✅ Fazer check-up anual
     
     Gostaria de agendar uma consulta de rotina?
```

#### Cenário 2: Risco Alto 🚨

```
User: Oi, não estou bem
Bot: Desculpe ouvir isso. Qual é seu nome?

User: Pedro Silva
Bot: Qual sua idade, Pedro?

User: 72 anos
Bot: E o que está sentindo?

User: Dor no peito, falta de ar, suor frio
Bot: 🚨 ALERTA!
     Você relatou sintomas graves!
     
     PROCURE EMERGÊNCIA IMEDIATAMENTE!
     📞 Ligue para 192 (SAMU)
     🏥 Vá ao pronto-socorro mais próximo
     
     Sua vida pode estar em risco!
     
     Precisa de ajuda para chamar a ambulância?
```

---

## 🧠 Recursos da IA

### Compreensão Natural

O Gemini entende automaticamente:
- 🎯 **Intenção do paciente** - Triagem, check-up, emergência
- 📝 **Sintomas em linguagem natural** - "Cansaço extremo", "Falta de ar", etc
- 🔢 **Dados em vários formatos** - "105 mmHg", "glicose 105", "105,125,26.5,210"
- 🚨 **Situações críticas** - Dor no peito, desmaio, etc

### Respostas Contextualizadas

O Gemini adapta respostas baseado em:
- 👤 **Dados do paciente** - Idade, sintomas, histórico
- 📊 **Etapa da conversa** - Coleta, análise, recomendação
- ⚠️ **Nível de risco** - Urgência da situação

### Processamento Inteligente

- 🧬 **Extração automática** de dados (nome, idade, vitais)
- 🔍 **Validação de entrada** - Rejeita dados inválidos
- 📋 **Sumarização** de informações
- 🎯 **Sugestões** contextualizadas

---

## 📊 Integração com ML

O chatbot combina IA com Machine Learning:

```
Entrada do Usuário
       ↓
   [Gemini]
   Compreensão Natural
       ↓
Extração de Dados
   (nome, idade, sintomas, vitais)
       ↓
   [API ML]
   Random Forest Classifier
   Acurácia: 98.75%
       ↓
Classificação de Risco
(Baixo/Médio/Alto)
       ↓
   [Gemini]
   Gera Recomendações
       ↓
Resposta para Paciente
```

---

## 💾 Persistência de Dados

Todas as consultas são salvas em:
```
PROJETO_SISTEMA_DIAGNOSTICO/dados_pacientes/historico_consultas.json
```

**Exemplo de registro:**
```json
{
  "nome": "João Silva",
  "idade": 45,
  "glicose": 120,
  "pressao": 140,
  "imc": 26.5,
  "colesterol": 220,
  "risco": "Médio",
  "sintomas": ["fadiga", "dor de cabeça"],
  "timestamp": "2026-05-25T20:30:00"
}
```

---

## 🎯 Casos de Uso

### 1. Triagem Inicial
Paciente novo faz primeira avaliação através do chatbot

### 2. Check-up Remoto
Paciente faz acompanhamento do próprio domicílio

### 3. Monitoramento Contínuo
Rastreia evolução de pacientes com risco médio

### 4. Educação em Saúde
Fornece dicas e recomendações preventivas

### 5. Detecção de Emergência
Identifica situações críticas que requerem SAMU

---

## 🔐 Segurança

### Dados Locais
- 📂 Arquivo JSON guardado no computador
- 🔒 Sem envio para nuvem (exceto para Gemini API)
- 🔐 Sem compartilhamento com terceiros

### Chave API
- ⚠️ **NUNCA** compartilhe sua chave
- ⚠️ **NUNCA** commit `.env` no Git
- ✅ Use `git ignore` para `.env`

### Avisos Legais
- ⚖️ Não substitui consulta médica profissional
- 🚨 Em emergência, ligue 192 (SAMU)
- 📋 Use apenas para triagem

---

## 🆘 Troubleshooting

### Erro: "GEMINI_API_KEY not found"

**Causa:** Arquivo `.env` não existe ou chave está vazia

**Solução:**
1. Verifique se `.env` está na raiz: `ML-CHATBOT-BUG-BUSTERS/.env`
2. Verifique conteúdo: `GEMINI_API_KEY=sua_chave_aqui`
3. Reinicie o terminal

### Erro: "401 Unauthorized"

**Causa:** Chave inválida ou expirada

**Solução:**
1. Gere nova chave em https://aistudio.google.com/app/apikey
2. Atualize arquivo `.env`
3. Reinicie chatbot

### Erro: "API não conecta"

**Causa:** Servidor não está rodando

**Solução:**
```bash
# Terminal 1
cd PROJETO_SISTEMA_DIAGNOSTICO/03_API
python -m uvicorn api_biomedicina:app --port 8000
```

### Erro: "module google.generativeai not found"

**Causa:** Dependência não instalada

**Solução:**
```bash
pip install google-generativeai python-dotenv
```

### Chat lento

**Causa:** Conexão internet lenta ou API sobrecarregada

**Solução:**
1. Verifique conexão internet
2. Aguarde alguns segundos
3. Feche e reabra o chatbot

---

## 📊 Estatísticas

| Métrica | Valor |
|---------|-------|
| Modelo ML | Random Forest |
| Acurácia | 98.75% ✅ |
| F1-Score | 98.74% ✅ |
| IA Conversacional | Google Gemini |
| Requisições/minuto | 60 (limite gratuito) |
| Limite de tokens | ~2000 por mensagem |

---

## 📚 Documentação Relacionada

| Arquivo | Descrição |
|---------|-----------|
| [../../CONFIGURACAO_GEMINI.md](../../CONFIGURACAO_GEMINI.md) | Guia completo de configuração |
| [../../INICIO_RAPIDO_GEMINI.md](../../INICIO_RAPIDO_GEMINI.md) | Início rápido em 3 passos |
| [README_CHATBOT.md](README_CHATBOT.md) | Chatbot sem Gemini |
| [../../PROJETO_SISTEMA_DIAGNOSTICO/README.md](../../README.md) | README do projeto |

---

## 🔗 Links Úteis

- **API Gemini:** https://ai.google.dev/
- **Console Google:** https://aistudio.google.com/app/apikey
- **Documentação:** https://ai.google.dev/tutorials
- **Comunidade:** https://groups.google.com/forum/#!forum/google-generative-ai-discuss

---

## 💡 Dicas Profissionais

### ✅ Faça
- Sempre pergunte nome do paciente no início
- Colete todos os dados vitais
- Alerte para situações críticas
- Recomende acompanhamento profissional

### ❌ Evite
- Não faça diagnósticos definitivos
- Não receite medicamentos
- Não ignore sintomas graves
- Não salve dados sensíveis em nuvem

---

## 🎓 Próximos Passos

1. ✅ Configurar chave Gemini
2. ✅ Executar script `run_chatbot_gemini.bat`
3. ✅ Acessar http://localhost:8501
4. ✅ Fazer teste com paciente fictício
5. ✅ Integrar em sistema clínico real
6. ✅ Treinar staff da clínica

---

**Versão:** 1.0.0
**Data:** Maio 2026
**Desenvolvido para:** Clínica de Biomedicina
**IA:** Google Gemini Pro
