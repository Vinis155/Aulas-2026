# 📚 ÍNDICE - CHATBOT COM GEMINI

## 🎯 COMECE AQUI!

### ⚡ Seu Primeiro Acesso (3 minutos)

1. **Leia:** [COLOQUE_CHAVE_AQUI.md](COLOQUE_CHAVE_AQUI.md) ← COMECE POR AQUI!
2. **Configure:** Criar arquivo `.env` com chave
3. **Execute:** `PROJETO_SISTEMA_DIAGNOSTICO/09_Scripts_Uteis/run_chatbot_gemini.bat`
4. **Acesse:** http://localhost:8501

---

## 📖 Documentação Completa

### Guias de Configuração

| Arquivo | Quando Usar |
|---------|------------|
| [**COLOQUE_CHAVE_AQUI.md**](COLOQUE_CHAVE_AQUI.md) | 📌 **COMECE AQUI!** Visual e fácil |
| [INICIO_RAPIDO_GEMINI.md](INICIO_RAPIDO_GEMINI.md) | ⚡ Início rápido em 3 passos |
| [CONFIGURACAO_GEMINI.md](CONFIGURACAO_GEMINI.md) | 📖 Guia detalhado e completo |
| [.env.example](.env.example) | 📝 Modelo de arquivo |

### Documentação do Chatbot

| Arquivo | Descrição |
|---------|-----------|
| [PROJETO_SISTEMA_DIAGNOSTICO/04_Interface/README_GEMINI.md](PROJETO_SISTEMA_DIAGNOSTICO/04_Interface/README_GEMINI.md) | 📚 Documentação completa do chatbot |
| [PROJETO_SISTEMA_DIAGNOSTICO/04_Interface/README_CHATBOT.md](PROJETO_SISTEMA_DIAGNOSTICO/04_Interface/README_CHATBOT.md) | 📚 Chatbot sem Gemini (versão básica) |
| [PROJETO_SISTEMA_DIAGNOSTICO/04_Interface/chatbot_clinica_gemini.py](PROJETO_SISTEMA_DIAGNOSTICO/04_Interface/chatbot_clinica_gemini.py) | 🐍 Código do chatbot Gemini |

### Outras Documentações

| Arquivo | Descrição |
|---------|-----------|
| [PROJETO_SISTEMA_DIAGNOSTICO/README.md](PROJETO_SISTEMA_DIAGNOSTICO/README.md) | 📋 README do projeto |
| [PROJETO_SISTEMA_DIAGNOSTICO/08_Documentacao/GUIA_CHATBOT.md](PROJETO_SISTEMA_DIAGNOSTICO/08_Documentacao/GUIA_CHATBOT.md) | 📖 Guia completo do chatbot |

---

## 🗺️ Estrutura de Pastas

```
ML-CHATBOT-BUG-BUSTERS/
│
├── 📌 COLOQUE_CHAVE_AQUI.md                  ← LEIA PRIMEIRO!
├── ⚡ INICIO_RAPIDO_GEMINI.md                ← Início rápido
├── 📖 CONFIGURACAO_GEMINI.md                 ← Guia completo
├── 📝 .env.example                           ← Modelo
├── 📄 .env                                   ← CRIAR AQUI! ✅
│
├── 📁 PROJETO_SISTEMA_DIAGNOSTICO/
│   │
│   ├── 🤖 04_Interface/
│   │   ├── README_GEMINI.md                  ← Docs Gemini
│   │   ├── README_CHATBOT.md                 ← Docs Chatbot
│   │   ├── chatbot_clinica_gemini.py         ← 🆕 COM GEMINI!
│   │   ├── chatbot_clinica.py                ← Versão básica
│   │   └── chatbot_clinica_pro.py            ← Versão PRO
│   │
│   ├── 📡 03_API/
│   │   └── api_biomedicina.py                ← API ML
│   │
│   ├── 🎯 09_Scripts_Uteis/
│   │   ├── run_chatbot_gemini.bat            ← 🆕 EXECUTE ISTO!
│   │   ├── run_chatbot.bat                   ← Versão básica
│   │   └── ...
│   │
│   ├── 📚 08_Documentacao/
│   │   ├── GUIA_CHATBOT.md
│   │   ├── README_SISTEMA.md
│   │   └── ...
│   │
│   ├── requirements.txt
│   └── README.md
│
└── 📄 README.md
```

---

## ⚙️ Configuração Rápida

### Passo 1: Obter Chave
```
https://aistudio.google.com/app/apikey
→ Login Google
→ "Create API Key"
→ Copiar
```

### Passo 2: Criar `.env`

**Local correto:**
```
ML-CHATBOT-BUG-BUSTERS/.env  ← AQUI!
```

**Conteúdo:**
```env
GEMINI_API_KEY=sua_chave_aqui
```

### Passo 3: Executar
```bash
PROJETO_SISTEMA_DIAGNOSTICO/09_Scripts_Uteis/run_chatbot_gemini.bat
```

---

## 🎯 Acessar Serviços

| Serviço | URL |
|---------|-----|
| 🤖 **Chatbot Gemini** | http://localhost:8501 |
| 📡 **API Docs** | http://localhost:8000/docs |
| 📊 **Swagger UI** | http://localhost:8000/swagger |

---

## 📋 Checklist de Instalação

- [ ] Li `COLOQUE_CHAVE_AQUI.md`
- [ ] Obtive chave em https://aistudio.google.com/app/apikey
- [ ] Criei arquivo `.env` na raiz
- [ ] Adicionar `GEMINI_API_KEY=...` no `.env`
- [ ] Instalei: `pip install google-generativeai python-dotenv`
- [ ] Executei: `run_chatbot_gemini.bat`
- [ ] Acessei: http://localhost:8501
- [ ] Testei conversa com o chatbot

---

## 🆘 Problemas?

### "Não consigo criar o arquivo `.env`"
→ Veja [COLOQUE_CHAVE_AQUI.md](COLOQUE_CHAVE_AQUI.md) - seção "Passo a Passo no Windows"

### "API não conecta"
→ Veja [CONFIGURACAO_GEMINI.md](CONFIGURACAO_GEMINI.md) - seção "Troubleshooting"

### "Chave não funciona"
→ Veja [INICIO_RAPIDO_GEMINI.md](INICIO_RAPIDO_GEMINI.md) - seção "Verificar Configuração"

---

## 💡 Dicas

✅ **Comece por:** [COLOQUE_CHAVE_AQUI.md](COLOQUE_CHAVE_AQUI.md)
✅ **Se tiver dúvidas:** [CONFIGURACAO_GEMINI.md](CONFIGURACAO_GEMINI.md)
✅ **Para aprender:** [PROJETO_SISTEMA_DIAGNOSTICO/04_Interface/README_GEMINI.md](PROJETO_SISTEMA_DIAGNOSTICO/04_Interface/README_GEMINI.md)
✅ **Para troubleshoot:** Procure "Troubleshooting" em qualquer doc

---

## 🎓 Próximas Ações

1. ✅ Abrir [COLOQUE_CHAVE_AQUI.md](COLOQUE_CHAVE_AQUI.md)
2. ✅ Configurar chave Gemini
3. ✅ Executar chatbot
4. ✅ Testar com pacientes fictícios
5. ✅ Integrar em sistema real
6. ✅ Treinar staff da clínica

---

## 📊 Versões Disponíveis

| Versão | Arquivo | Tipo |
|--------|---------|------|
| **Básica** | `interface_streamlit.py` | Formulário |
| **Chatbot** | `chatbot_clinica.py` | Conversa |
| **Chatbot PRO** | `chatbot_clinica_pro.py` | Conversa + Análise |
| **Chatbot Gemini** ⭐ | `chatbot_clinica_gemini.py` | **IA GEMINI** |

---

**Última atualização:** Maio 2026
**Projeto:** ML-CHATBOT-BUG-BUSTERS
**IA:** Google Gemini Pro
