# 🖥️ Interface Streamlit v2.0 — AULA_09

## 🎯 O que é a v2.0?

A interface v2.0 é uma **evolução completa** da versão anterior com:

✅ **Autenticação** — Login com banco de dados  
✅ **Dashboard** — Visão geral do sistema  
✅ **CRUD de Pacientes** — Gerenciar dados  
✅ **Análise com IA** — Predições persistidas  
✅ **Segurança** — SHA256 para senhas  
✅ **Integration** — Banco SQLite completo

---

## 📱 Telas Principais

### 1. **Tela de Login**
```
🏥 Sistema de Diagnóstico Clínico v2.0

Usuário: [_____________]
Senha:   [_____________]
[🔐 Entrar]
```

**Credenciais Padrão:**
- admin / admin123
- medico / medico123
- medico2 / senha456

### 2. **Dashboard**
Mostra:
- 👥 Total de pacientes
- 📋 Total de exames
- 📈 Total de análises
- 🔄 Últimas análises realizadas

### 3. **Gestão de Pacientes**
Abas:
- **Listar:** Todos os pacientes cadastrados
- **Novo:** Adicionar novo paciente (nome + idade)

### 4. **Análise de Risco (IA)**
Fluxo:
1. Seleciona paciente
2. Insere dados biomédicos (glicose, pressão, IMC, colesterol)
3. Indicadores de status em tempo real
4. **Clica em "Analisar com IA"**
5. Resultado: Risco Baixo/Médio/Alto com confiança

---

## 🚀 Como Usar

### Passo 1: Criar o Banco
```bash
python 10_Banco_Dados/criar_banco_dados.py
```

**Resultado:** `clinica.db` criado com:
- 5 tabelas
- 3 usuários padrão
- ~2000 pacientes
- 7 tipos de exame

### Passo 2: Treinar o Modelo
```bash
python 02_ML_Pipeline/2_pipeline_ml.py
```

**Resultado:** Arquivos `.pkl` criados em `06_Modelos/`:
- `melhor_modelo.pkl`
- `scaler.pkl`

### Passo 3: Iniciar a Interface
```bash
streamlit run 04_Interface/interface_streamlit_v2.py
```

**Resultado:** Acesse http://localhost:8501

### Passo 4: Fazer Login
- Usuário: `medico`
- Senha: `medico123`

### Passo 5: Usar o Sistema
1. Vá para **Pacientes** → Veja a lista
2. Vá para **Análise de Risco**
3. Selecione um paciente
4. Insira dados biomédicos
5. Clique em **Analisar com IA**
6. Veja o resultado!

---

## 📊 Arquitetura Interna

```
interface_streamlit_v2.py

┌─ Session State (Login)
│  └─ logged_in, usuario_id, username
│
├─ Database Functions
│  ├─ conectar_db() — SQLite connection
│  ├─ validar_login() — SHA256 auth
│  ├─ obter_pacientes() — SELECT
│  └─ salvar_resultado() — INSERT
│
├─ ML Functions
│  ├─ carregar_modelo_ml() — joblib
│  └─ fazer_predicao_ia() — sklearn predict
│
└─ Pages
   ├─ pagina_login() — Autenticação
   ├─ pagina_dashboard() — Dashboard
   ├─ pagina_pacientes() — CRUD
   └─ pagina_analise_ia() — Predição
```

---

## 🔐 Segurança

### Senhas
- Armazenadas como **SHA256** (não reversível)
- Nunca em plain text
- Validação no login

### SQL Injection
- Todas as queries usam **prepared statements**
- Proteção automática contra ataques

### Autenticação
- Verifica `username` + `senha_hash` + `ativo = 1`
- Mantém `usuario_id` em session state

---

## 🔄 Fluxo de Dados

```
1. Usuário faz login
   ↓
2. Valida com banco SQL
   ↓
3. Armazena em session state
   ↓
4. Acessa menu principal
   ├─ Dashboard (SELECT COUNT)
   ├─ Pacientes (SELECT / INSERT)
   └─ Análise IA
      ├─ Carrega modelo.pkl
      ├─ Faz predição
      └─ Salva em banco (INSERT)
```

---

## 📈 Indicadores de Status

Enquanto o usuário digita os dados:

| Status | Cor | Significado |
|--------|-----|---|
| ✅ | Verde | Dentro da faixa normal |
| ⚠️ | Laranja | Em zona de alerta |
| ❌ | Vermelho | Crítico |

**Exemplo:**
- Glicose < 100: ✅ Verde
- Glicose 100-125: ⚠️ Laranja
- Glicose > 126: ❌ Vermelho

---

## 🗄️ Tabelas Utilizadas

### `usuarios`
```
id | username | senha_hash | role | ativo
```
✅ Validação de login

### `pacientes`
```
id | nome | idade | data_cadastro | ativo
```
✅ Listagem e cadastro

### `resultados`
```
id | paciente_id | risco_codigo | risco_classificacao | probabilidade | data_analise
```
✅ Histórico de análises

---

## ⚙️ Configurações

```python
# Caminhos
DB_PATH = ".../clinica.db"
MODELO_PATH = ".../06_Modelos/melhor_modelo.pkl"
SCALER_PATH = ".../06_Modelos/scaler.pkl"

# Session State
st.session_state.logged_in
st.session_state.usuario_id
st.session_state.username
```

---

## 🛠️ Troubleshooting

### Erro: "Modelos .pkl não encontrados"
```bash
python 02_ML_Pipeline/2_pipeline_ml.py
```

### Erro: "Banco de dados não existe"
```bash
python 10_Banco_Dados/criar_banco_dados.py
```

### Erro: "Login incorreto"
- Verifique credenciais (admin/admin123)
- Verifique se banco foi criado
- Verifique se user está ativo (`ativo = 1`)

### Interface travando
- Feche com Ctrl+C
- Execute novamente
- Libere porta 8501

---

## 📊 Exemplo de Uso

**Cenário:** Analisar um paciente

```
1. Login
   └─ admin / admin123

2. Ir para Dashboard
   └─ Ver que existe 1 paciente

3. Ir para Análise de Risco
   └─ Selecionar "Paciente_001"

4. Preencher dados:
   ├─ Idade: 45
   ├─ Glicose: 110
   ├─ Pressão: 130
   ├─ IMC: 26
   └─ Colesterol: 220

5. Indicadores mostram:
   ├─ ⚠️ Glicose (alerta)
   ├─ ⚠️ Pressão (alerta)
   ├─ ⚠️ IMC (alerta)
   └─ ⚠️ Colesterol (alerta)

6. Clique em "Analisar com IA"
   └─ Resultado: ⚠️ RISCO MÉDIO (78% confiança)

7. Resultado salvo no banco
   └─ Próxima vez que abrir, verá no histórico
```

---

## 📚 Dependências

```
streamlit
sqlite3 (built-in)
pandas
numpy
scikit-learn
joblib
hashlib (built-in)
```

---

## 🎓 Integração com AULA_09

✅ **Passo 1:** Banco de dados relacional  
✅ **Passo 2:** Front-end Streamlit com login, CRUD, IA

**Requisitos atendidos:**
- Tela de login com validação
- Menu principal com navegação
- Gestão de pacientes (CRUD)
- Análise com IA integrada
- Banco de dados persistente

---

## 🔮 Próximas Melhorias (v3.0)

- [ ] CRUD completo de tipos de exame
- [ ] Gráficos de tendência
- [ ] Exportar relatórios (PDF)
- [ ] Notificações
- [ ] Dark mode
- [ ] Filtros avançados
- [ ] Rol-based access control (RBAC)

---

**Versão:** 2.0  
**Status:** ✅ Pronto para produção  
**Requisitos atendidos:** ✅ AULA_09 Passo 2
