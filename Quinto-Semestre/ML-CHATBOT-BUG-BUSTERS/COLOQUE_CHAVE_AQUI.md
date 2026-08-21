# 🔑 ONDE COLOCAR A CHAVE GEMINI

## Visual da Localização

```
📁 ML-CHATBOT-BUG-BUSTERS/
│
├── 📄 .env  ← COLOCAR CHAVE AQUI! ✅✅✅
│
├── 📁 PROJETO_SISTEMA_DIAGNOSTICO/
│   ├── 📁 04_Interface/
│   │   └── 🤖 chatbot_clinica_gemini.py
│   ├── 📁 03_API/
│   └── 📁 09_Scripts_Uteis/
│       └── 🎯 run_chatbot_gemini.bat
│
├── 📄 CONFIGURACAO_GEMINI.md
├── 📄 INICIO_RAPIDO_GEMINI.md
├── 📄 .env.example
└── 📄 README.md
```

---

## 3️⃣ PASSOS SIMPLES

### 1️⃣ Obter Chave (2 min)
```
Acesse: https://aistudio.google.com/app/apikey
→ Login com Google
→ Click "Create API Key"
→ Copiar (Ctrl+C)
```

**Sua chave será assim:**
```
AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
```

### 2️⃣ Criar Arquivo `.env` (1 min)

**Abra o Bloco de Notas ou VS Code**

**Cole isto:**
```
GEMINI_API_KEY=sua_chave_aqui
```

**Substitua `sua_chave_aqui` pela chave copiada**

Exemplo:
```
GEMINI_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
```

**Salve como:**
```
Nome: .env
Localização: ML-CHATBOT-BUG-BUSTERS/
Tipo: Todos os arquivos (*)
```

### 3️⃣ Executar (1 min)
```bash
PROJETO_SISTEMA_DIAGNOSTICO/09_Scripts_Uteis/run_chatbot_gemini.bat
```

---

## ⚠️ IMPORTANTE - LOCALIZAÇÃO EXATA

```
❌ ERRADO - Estas localizações NÃO funcionam:
ML-CHATBOT-BUG-BUSTERS/PROJETO_SISTEMA_DIAGNOSTICO/.env
ML-CHATBOT-BUG-BUSTERS/PROJETO_SISTEMA_DIAGNOSTICO/04_Interface/.env

✅ CORRETO - Coloque AQUI:
ML-CHATBOT-BUG-BUSTERS/.env
```

---

## 🖥️ Passo a Passo no Windows

### Método 1: Bloco de Notas

1. **Abra o Bloco de Notas**
   - Tecla Windows + busque "Bloco de Notas"

2. **Digite:**
   ```
   GEMINI_API_KEY=sua_chave_aqui
   ```

3. **Salve como**
   - `Arquivo` → `Salvar como`
   - Nome: `.env`
   - Localização: `C:\Users\seu_usuario\Desktop\Aulas-2026\Quinto-Semestre\ML-CHATBOT-BUG-BUSTERS`
   - Tipo: Todos os arquivos

4. **Pronto!** Arquivo `.env` criado

### Método 2: VS Code (Recomendado)

1. **Abra VS Code na pasta do projeto**
   - `Arquivo` → `Abrir Pasta`
   - Selecione: `ML-CHATBOT-BUG-BUSTERS`

2. **Crie novo arquivo**
   - `Ctrl+N` ou `Arquivo` → `Novo Arquivo`

3. **Salve como `.env`**
   - `Ctrl+Shift+S` ou `Arquivo` → `Salvar Como`
   - Nome: `.env`

4. **Cole:**
   ```
   GEMINI_API_KEY=sua_chave_aqui
   ```

5. **Salve**
   - `Ctrl+S`

---

## 🔍 Verificar se Deu Certo

### Método 1: Visual
```
Abra a pasta ML-CHATBOT-BUG-BUSTERS
Procure pelo arquivo .env
Se estiver lá, está certo! ✅
```

### Método 2: Terminal
```bash
# Na pasta ML-CHATBOT-BUG-BUSTERS
dir .env

# Se aparecer ".env", está certo ✅
```

---

## 🆘 Não Consigo Criar o Arquivo `.env`

### Problema: Arquivo está "invisível"

**Solução (Windows):**
1. Abra Explorador de Arquivos
2. Clique em "Ver" (Menu)
3. Ative "Extensões de arquivo"
4. Agora você consegue criar `.env`

### Problema: Arquivo criado mas não aparece

**Solução:**
1. Clique em "Ver"
2. Ative "Mostrar arquivos ocultos"
3. Procure `.env` novamente

---

## 📝 Template Completo

Copie e cole exatamente isto no arquivo `.env`:

```
# ===================================
# CONFIGURACAO GEMINI API
# ===================================

# Sua chave do Google Gemini
# Obtenha em: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=sua_chave_aqui
```

---

## ✅ Checklist Final

- [ ] Obtive chave em https://aistudio.google.com/app/apikey
- [ ] Criei arquivo `.env` na raiz do projeto
- [ ] Coloquei `GEMINI_API_KEY=sua_chave_aqui` no arquivo
- [ ] Substituí `sua_chave_aqui` pela chave real
- [ ] Salvei o arquivo `.env`
- [ ] Arquivo está em `ML-CHATBOT-BUG-BUSTERS/.env`
- [ ] Instalei: `pip install google-generativeai python-dotenv`
- [ ] Executei: `run_chatbot_gemini.bat`

---

## 🎉 Pronto!

Se tudo deu certo:
1. Acesse http://localhost:8501
2. Comece a conversar com o chatbot
3. Aproveite a IA Gemini! 🤖

---

**Dúvidas?** Consulte:
- [CONFIGURACAO_GEMINI.md](../CONFIGURACAO_GEMINI.md) - Guia completo
- [INICIO_RAPIDO_GEMINI.md](../INICIO_RAPIDO_GEMINI.md) - Início rápido
- [04_Interface/README_GEMINI.md](../PROJETO_SISTEMA_DIAGNOSTICO/04_Interface/README_GEMINI.md) - Documentação do chatbot
