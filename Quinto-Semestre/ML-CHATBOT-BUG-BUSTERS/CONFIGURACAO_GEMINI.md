# ⚙️ CONFIGURAÇÃO DA CHAVE GEMINI API

## 🔑 Como Obter a Chave API do Google Gemini

### Passo 1: Acessar o Google AI Studio

1. Acesse: https://aistudio.google.com/app/apikey
2. Faça login com sua conta Google (crie uma se não tiver)
3. Clique em **"Create API Key"** ou **"Get API Key"**

### Passo 2: Copiar a Chave

1. A chave será gerada automaticamente
2. Clique em **"Copy"** para copiar
3. Guarde a chave em lugar seguro (nunca compartilhe!)

---

## 📝 Como Configurar no Projeto

### Opção 1: Arquivo .env (Recomendado)

#### Windows:
1. Na pasta raiz do projeto, crie arquivo chamado `.env`
2. Abra em um editor de texto (Bloco de Notas, VS Code, etc)
3. Cole exatamente isto:
```
GEMINI_API_KEY=sua_chave_aqui
```
4. Substitua `sua_chave_aqui` pela chave copiada
5. **Salve o arquivo**

Exemplo:
```
GEMINI_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
```

#### Localização do arquivo .env:
```
ML-CHATBOT-BUG-BUSTERS/
├── .env                           ← Criar aqui
├── PROJETO_SISTEMA_DIAGNOSTICO/
├── AULA_02/
└── ... (outros arquivos)
```

### Opção 2: Variável de Ambiente do Windows

#### Via PowerShell (Admin):
```powershell
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'sua_chave_aqui', 'User')
```

#### Via CMD (Admin):
```batch
setx GEMINI_API_KEY "sua_chave_aqui"
```

---

## 🚀 Instalação de Dependências

```bash
# Instalar Google Generative AI
pip install google-generativeai

# Ou instale todas de uma vez
pip install streamlit requests pandas python-dotenv google-generativeai
```

---

## ✅ Verificar Configuração

Execute este comando para testar:

```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('Chave configurada!' if os.getenv('GEMINI_API_KEY') else 'Erro: Chave não encontrada!')"
```

---

## 🧪 Testar o Chatbot Gemini

```bash
cd PROJETO_SISTEMA_DIAGNOSTICO/04_Interface
streamlit run chatbot_clinica_gemini.py
```

Acesse: http://localhost:8501

---

## 📋 Checklist de Configuração

- [ ] Criar arquivo `.env` na raiz do projeto
- [ ] Obter chave em https://aistudio.google.com/app/apikey
- [ ] Adicionar chave no arquivo `.env`
- [ ] Instalar `pip install google-generativeai`
- [ ] Testar com comando Python
- [ ] Executar chatbot Gemini

---

## 🔐 Segurança

### ⚠️ IMPORTANTE - Nunca faça isto:
- ❌ Não commit do arquivo `.env` no Git
- ❌ Não compartilhe sua chave em redes sociais
- ❌ Não coloque chave no código Python
- ❌ Não envie arquivo `.env` por email

### ✅ Arquivo .gitignore (já deve estar configurado):
```
.env
.env.local
*.pyc
__pycache__/
```

---

## ⏱️ Limite de Uso Gratuito

A API Gemini do Google oferece:
- ✅ **Gratuito:** 60 requisições por minuto
- ✅ **Sem cartão de crédito obrigatório**
- ✅ Suficiente para desenvolvimento

Se precisar de mais, acesse Google Cloud Console para ativar plano pago

---

## 🐛 Troubleshooting

### Erro: "GEMINI_API_KEY not found"

**Solução:**
1. Verifique se arquivo `.env` existe na raiz
2. Verifique se está escrito correto: `GEMINI_API_KEY=...`
3. Reinicie o terminal/IDE

### Erro: "401 Unauthorized"

**Solução:**
1. Verifique se copiou chave corretamente
2. Teste a chave em: https://aistudio.google.com/
3. Gere nova chave se necessário

### Erro: "module 'google.generativeai' not found"

**Solução:**
```bash
pip install google-generativeai --upgrade
```

---

## 📞 Suporte

- **Documentação Gemini:** https://ai.google.dev/tutorials
- **Google Cloud Console:** https://console.cloud.google.com
- **Comunidade:** https://groups.google.com/forum/#!forum/google-generative-ai-discuss

---

**Versão:** 1.0.0
**Data:** Maio 2026
**Projeto:** ML-CHATBOT-BUG-BUSTERS
