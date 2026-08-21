# 🤖 INÍCIO RÁPIDO - CHATBOT COM GEMINI IA

## ⚡ 3 Passos para Começar

### Passo 1️⃣: Obter Chave Gemini (2 minutos)

```
1. Abra: https://aistudio.google.com/app/apikey
2. Faça login com Google
3. Clique "Create API Key"
4. Copie a chave (exemplo: AIzaSyD...)
```

### Passo 2️⃣: Configurar Chave (1 minuto)

**Opção A - Arquivo .env (Recomendado):**

1. Crie arquivo `.env` na raiz do projeto:
   ```
   ML-CHATBOT-BUG-BUSTERS/
   └── .env  ← Criar aqui
   ```

2. Cole isto dentro do arquivo:
   ```
   GEMINI_API_KEY=sua_chave_aqui
   ```

3. Substitua `sua_chave_aqui` pela chave copiada

**Exemplo completo:**
```
GEMINI_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
```

**Opção B - Variável de Ambiente (Windows):**
```powershell
# Abra PowerShell como ADMIN e execute:
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'sua_chave_aqui', 'User')
```

### Passo 3️⃣: Executar (1 minuto)

**Opção A - Script Automático:**
```bash
PROJETO_SISTEMA_DIAGNOSTICO\09_Scripts_Uteis\run_chatbot_gemini.bat
```

**Opção B - Manual:**

Terminal 1:
```bash
cd PROJETO_SISTEMA_DIAGNOSTICO/03_API
python -m uvicorn api_biomedicina:app --port 8000
```

Terminal 2:
```bash
pip install google-generativeai python-dotenv
cd PROJETO_SISTEMA_DIAGNOSTICO/04_Interface
streamlit run chatbot_clinica_gemini.py
```

---

## 🎯 Usar o Chatbot

### Exemplo de Conversa:

```
Bot: Olá! Bem-vindo à Clínica. Como posso ajudá-lo?

User: Oi, estou me sentindo mal

Bot: Sinto que não está bem. Qual é o seu nome?

User: João Silva

Bot: Prazer, João. Qual é sua idade?

User: 45 anos

Bot: Qual é o seu problema? Descreva seus sintomas.

User: Tenho fadiga, dor de cabeça e febre

Bot: Entendo. Vamos coletar seus dados vitais...
     Digite seus valores: glicose, pressão, imc, colesterol
     Exemplo: 105 125 26.5 210

User: 105 125 26.5 210

Bot: Ótimo! Posso fazer um diagnóstico agora?

User: Sim, fazer diagnóstico

Bot: 🟡 RESULTADO: RISCO MÉDIO
     Recomendações: [...]
```

---

## 📂 Onde Colocar a Chave

```
ML-CHATBOT-BUG-BUSTERS/              ← Raiz do Projeto
│
├── .env                             ← COLOCAR CHAVE AQUI! ✅
├── CONFIGURACAO_GEMINI.md           ← Guia detalhado
├── .env.example                     ← Modelo (não edite)
├── PROJETO_SISTEMA_DIAGNOSTICO/
│   ├── 04_Interface/
│   │   ├── chatbot_clinica_gemini.py  ← Novo arquivo ✨
│   │   ├── chatbot_clinica.py
│   │   └── chatbot_clinica_pro.py
│   ├── 03_API/
│   └── 09_Scripts_Uteis/
│       ├── run_chatbot_gemini.bat    ← Novo script ✨
│       └── run_chatbot.bat
│
└── README.md
```

---

## 🔑 Exemplos de Chaves Gemini

```
AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
AIzaSyDf5e1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
AIzaSyDabcdefghijklmnopqrstuvwxyz1234567890
```

**⚠️ Formato:** Começa com `AIzaSy` seguido de ~36 caracteres

---

## ✅ Verificar se Está Funcionando

```bash
# Terminal
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ OK!' if os.getenv('GEMINI_API_KEY') else '❌ Erro!')"
```

---

## 🆘 Erros Comuns

### ❌ "GEMINI_API_KEY not found"
**Solução:** Criou arquivo `.env`? Está na raiz? Tem a chave?

### ❌ "401 Unauthorized"
**Solução:** Chave está errada? Copie novamente de https://aistudio.google.com/app/apikey

### ❌ "module google.generativeai not found"
**Solução:** 
```bash
pip install google-generativeai python-dotenv
```

---

## 📞 Links Rápidos

| Link | Descrição |
|------|-----------|
| https://aistudio.google.com/app/apikey | 🔑 Obter Chave |
| http://localhost:8501 | 🤖 Chatbot Gemini |
| http://localhost:8000/docs | 📚 API Docs |
| ../CONFIGURACAO_GEMINI.md | 📖 Guia Completo |

---

## 🎓 Próximos Passos

1. ✅ Criar arquivo `.env` na raiz
2. ✅ Obter chave em https://aistudio.google.com/app/apikey
3. ✅ Adicionar chave no `.env`
4. ✅ Instalar: `pip install google-generativeai python-dotenv`
5. ✅ Rodar: `run_chatbot_gemini.bat`
6. ✅ Acessar: http://localhost:8501
7. ✅ Conversar com IA! 🎉

---

**💡 Dica:** Salve este arquivo! Você pode precisar consultar depois.

**📅 Data:** Maio 2026
**🏥 Projeto:** ML-CHATBOT-BUG-BUSTERS
