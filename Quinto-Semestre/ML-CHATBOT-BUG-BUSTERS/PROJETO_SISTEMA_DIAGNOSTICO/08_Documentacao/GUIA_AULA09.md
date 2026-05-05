# 🎓 GUIA COMPLETO — AULA_09

## 📚 Objetivos da AULA_09

1. ✅ **Criar banco de dados relacional** (SQLite)
2. ✅ **Implementar interface com login** (Streamlit v2.0)
3. ✅ **Integrar CRUD de dados** (Pacientes, Exames, Resultados)
4. ✅ **Conectar com IA** (Modelo de predição)

---

## 🚀 Execution Step-by-Step

### ✅ Step 1: Preparar o Ambiente (5 minutos)

#### 1.1 Navegar até o diretório do projeto
```bash
cd Desktop/Aulas-2026/Quinto-Semestre/ML-CHATBOT-BUG-BUSTERS/PROJETO_SISTEMA_DIAGNOSTICO
```

#### 1.2 Verificar estrutura
```bash
dir
```

Você deve ver:
```
01_Dataset/
02_ML_Pipeline/
03_API/
04_Interface/
05_Dados/
06_Modelos/
07_Testes/
08_Documentacao/
09_Scripts_Uteis/
10_Banco_Dados/
requirements.txt
```

#### 1.3 Ativar ambiente virtual (se existir)
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

---

### ✅ Step 2: Criar o Banco de Dados (3 minutos)

#### 2.1 Opção A: Via Script Batch (Windows)
```bash
09_Scripts_Uteis\setup_database.bat
```

#### 2.2 Opção B: Via Terminal
```bash
python 10_Banco_Dados/criar_banco_dados.py
```

#### 2.3 Esperado (Output)
```
======================================================================
  CRIAÇÃO DO BANCO DE DADOS — SISTEMA CLÍNICO
======================================================================

[PASSO 1] Verificando banco antigo...
  ✓ Nenhum banco antigo encontrado

[PASSO 2] Criando conexão com SQLite...
  ✓ Banco criado em: .../clinica.db

[PASSO 3] Criando tabela 'usuarios'...
  ✓ Tabela 'usuarios' criada

[PASSO 4] Criando tabela 'tipos_exame'...
  ✓ Tabela 'tipos_exame' criada

[PASSO 5] Criando tabela 'pacientes'...
  ✓ Tabela 'pacientes' criada

[PASSO 6] Criando tabela 'exames_paciente'...
  ✓ Tabela 'exames_paciente' criada

[PASSO 7] Criando tabela 'resultados'...
  ✓ Tabela 'resultados' criada

[PASSO 8] Inserindo usuários padrão...
  ✓ 3 usuários criados

[PASSO 9] Inserindo tipos de exame...
  ✓ 7 tipos de exame criados

[PASSO 10] Importando pacientes do CSV...
  ✓ 2000 pacientes importados do CSV

[PASSO 11] Salvando banco de dados...
  ✓ Banco de dados salvo com sucesso

======================================================================
  BANCO DE DADOS CRIADO COM SUCESSO!
======================================================================

📊 Resumo:
  • Arquivo: .../clinica.db
  • Tabelas: 6
  • Usuários: 3
  • Tipos de Exame: 7

👤 Usuários Padrão:
  • admin / admin123 (Administrador)
  • medico / medico123 (Médico)
  • medico2 / senha456 (Médico 2)
```

#### 2.4 Verificar se foi criado
```bash
dir *.db
```

Deve mostrar: `clinica.db`

---

### ✅ Step 3: Treinar o Modelo de IA (5-10 minutos)

#### 3.1 Opção A: Via Script Batch (Windows)
```bash
09_Scripts_Uteis\run_pipeline.bat
```

#### 3.2 Opção B: Via Terminal
```bash
python 02_ML_Pipeline/2_pipeline_ml.py
```

#### 3.3 Esperado (Output)
```
[ETAPA 1] Carregando dados...
  ✓ 2000 registros carregados

[ETAPA 2] Preparando dados...
  ✓ Features: 5, Alvos: 2000

[ETAPA 3] Normalizando dados...
  ✓ StandardScaler aplicado

[ETAPA 4] Dividindo dataset...
  ✓ Treino: 1600, Teste: 400

[ETAPA 5] Treinando Random Forest...
  ✓ Modelo treinado com sucesso

[ETAPA 6] Avaliando no conjunto de teste...
  ✓ Acurácia: 98.75%
  ✓ F1-Score: 98.74%

[ETAPA 7] Validação Cruzada (5-fold)...
  ✓ CV Score: 98.50% (±0.35%)

[ETAPA 8] Matriz de Confusão...
  ✓ Gráfico salvo: 08_Documentacao/matriz_confusao.png

[ETAPA 9] Gerando visualizações...
  ✓ ROC Curve: 06_Modelos/roc_curve.png
  ✓ Feature Importance: 06_Modelos/feature_importance.png

[ETAPA 10] Fazendo demo de predição...
  ✓ Predição realizada com sucesso

[ETAPA 11] Serializando modelos (joblib)...
  ✓ melhor_modelo.pkl salvo
  ✓ scaler.pkl salvo
  ✓ metadados_modelo.pkl salvo

======================================================================
  MODELO TREINADO COM SUCESSO!
======================================================================
```

#### 3.4 Verificar se foi criado
```bash
dir 06_Modelos\*.pkl
```

Deve mostrar:
- `melhor_modelo.pkl` ✅
- `scaler.pkl` ✅
- `metadados_modelo.pkl` ✅

---

### ✅ Step 4: Iniciar a Interface Streamlit v2.0 (2 minutos)

#### 4.1 Opção A: Via Script Batch (Windows)
```bash
09_Scripts_Uteis\run_ui.bat
```

#### 4.2 Opção B: Via Terminal
```bash
streamlit run 04_Interface/interface_streamlit_v2.py
```

#### 4.3 Esperado (Output)
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

#### 4.4 Acessar a Interface
Abra o navegador e vá para: **http://localhost:8501**

---

### ✅ Step 5: Fazer Login (1 minuto)

#### 5.1 Tela de Login Aparece
```
🏥 Sistema de Diagnóstico Clínico v2.0

Usuário: [_____________________]
Senha:   [_____________________]

[🔐 Entrar]
```

#### 5.2 Inserir Credenciais
- **Usuário:** `medico`
- **Senha:** `medico123`

#### 5.3 Clicar em "Entrar"

#### 5.4 Esperado: Dashboard
```
📊 Dashboard

👥 Pacientes: 2000
📋 Exames: 0
📈 Análises: 0
```

---

### ✅ Step 6: Explorar o Dashboard (2 minutos)

#### 6.1 Navegação (Sidebar esquerda)
```
👋 Bem-vindo, medico!

○ Dashboard (ativo)
○ Pacientes
○ Análise de Risco

[🚪 Logout]
```

#### 6.2 Conteúdo do Dashboard
- 📊 Três cards com estatísticas
- 📈 Lista das últimas análises (vazia por enquanto)

---

### ✅ Step 7: Gerenciar Pacientes (3 minutos)

#### 7.1 Clicar em "Pacientes" (Sidebar)

#### 7.2 Duas Abas Aparecem
- **Listar Pacientes:** Mostra todos os ~2000 cadastrados
- **Novo Paciente:** Formulário para adicionar

#### 7.3 Experimentar
- Vá para aba "Listar Pacientes"
- Veja a lista de pacientes
- Vá para aba "Novo Paciente"
- Adicione um novo paciente

#### 7.4 Novo Paciente (Exemplo)
```
Nome do Paciente: João Silva
Idade: 45

[✅ Adicionar Paciente]
```

---

### ✅ Step 8: Fazer Análise com IA (5 minutos)

#### 8.1 Clicar em "Análise de Risco" (Sidebar)

#### 8.2 Selecionar Paciente
```
Selecione o Paciente: [Paciente_001 ▼]
```

#### 8.3 Dados do Paciente Aparecem
```
Nome: Paciente_001
ID: 1
Idade: 50
Data Cadastro: 2026-04-02
```

#### 8.4 Preencher Dados Biomédicos
```
Idade (anos): 50
Glicose (mg/dL): 110
Pressão Sistólica (mmHg): 130
IMC (kg/m²): 26
Colesterol (mg/dL): 220
```

#### 8.5 Indicadores de Status Aparecem em Tempo Real
```
✅ Glicose    ⚠️ Pressão    ⚠️ IMC    ⚠️ Colesterol    ✅ Idade
105            120           25.5         200             45
(Normal)       (Normal)      (Normal)     (Normal)        (Normal)
```

#### 8.6 Clicar em "🔍 Analisar com IA"

#### 8.7 Resultado
```
⚠️ RISCO MÉDIO
Confiança: 78.5%

Risco Baixo:  15.2%
Risco Médio:  78.5%
Risco Alto:   6.3%
```

#### 8.8 Resultado Salvo no Banco
O resultado é automaticamente salvo em `resultados` table:
- `paciente_id`: 1
- `risco_codigo`: 1 (médio)
- `risco_classificacao`: "Médio"
- `probabilidade`: 0.785
- `data_analise`: 2026-04-02 14:30:00

---

### ✅ Step 9: Voltar ao Dashboard (1 minuto)

#### 9.1 Clicar em "Dashboard" (Sidebar)

#### 9.2 Verificar Atualização
```
📊 Dashboard

👥 Pacientes: 2001  (aumentou!)
📋 Exames: 0
📈 Análises: 1  (aumentou!)

📈 Últimas Análises:
• Paciente_001 → Médio 78.5%
```

---

## 🔄 Fluxo Completo Automatizado

### Opção 1: Script Único (Windows)
```bash
cd PROJETO_SISTEMA_DIAGNOSTICO
09_Scripts_Uteis\run_all.bat
```

**O que ele faz:**
1. Gera dataset
2. Treina modelo
3. Inicia API
4. Inicia Streamlit

### Opção 2: Passo a Passo (Recomendado)

```bash
# Terminal 1: Criar banco
python 10_Banco_Dados/criar_banco_dados.py

# Terminal 2: Treinar modelo
python 02_ML_Pipeline/2_pipeline_ml.py

# Terminal 3: Iniciar interface
streamlit run 04_Interface/interface_streamlit_v2.py

# Navegador: http://localhost:8501
```

---

## 🎓 Conceitos Aprendidos

### AULA_09 Passo 1: Banco de Dados ✅
- [x] Criar banco SQLite
- [x] Criar 5 tabelas relacionadas
- [x] Importar dados CSV
- [x] Inserir dados padrão

**Arquivo:** `10_Banco_Dados/criar_banco_dados.py`

### AULA_09 Passo 2: Interface com Login ✅
- [x] Tela de login com validação SQL
- [x] Menu principal com navegação
- [x] Dashboard com estatísticas
- [x] CRUD de pacientes
- [x] Análise com IA integrada

**Arquivo:** `04_Interface/interface_streamlit_v2.py`

---

## 📊 Dados de Exemplo

### Usuários
```
| username | senha     | role        |
|----------|-----------|-------------|
| admin    | admin123  | Administrador |
| medico   | medico123 | Médico      |
| medico2  | senha456  | Médico      |
```

### Tipos de Exame (7)
1. Glicose (mg/dL)
2. Pressão Arterial (mmHg)
3. IMC (kg/m²)
4. Colesterol Total (mg/dL)
5. HDL (mg/dL)
6. LDL (mg/dL)
7. Triglicerídios (mg/dL)

### Pacientes (~2000)
```
| id  | nome         | idade |
|-----|--------------|-------|
| 1   | Paciente_001 | 45    |
| 2   | Paciente_002 | 38    |
| ... | ...          | ...   |
```

---

## 🛠️ Troubleshooting

### ❌ Erro: "banco de dados já existe"
```
⚠️  Banco de dados já existe: clinica.db
Deseja recriá-lo? (s/n): s
```
Responda `s` para recriar.

### ❌ Erro: "Modelos .pkl não encontrados"
**Solução:** Execute o pipeline primeiro
```bash
python 02_ML_Pipeline/2_pipeline_ml.py
```

### ❌ Erro: "Login incorreto"
**Verificar:**
- Usuário: `medico` (exatamente)
- Senha: `medico123` (exatamente)
- Banco foi criado: `clinica.db` existe

### ❌ Erro: "Porta 8501 já está em uso"
```bash
# Feche a interface anterior (Ctrl+C)
# Ou use porta diferente:
streamlit run 04_Interface/interface_streamlit_v2.py --server.port 8502
```

### ❌ Erro: "Nenhum paciente cadastrado"
**Causa:** CSV não foi importado  
**Solução:**
```bash
# Recrie o banco (responda 's')
python 10_Banco_Dados/criar_banco_dados.py
```

---

## ✨ Checklist Final

Antes de considerar completo, verifique:

- [ ] Banco de dados criado (`clinica.db` existe)
- [ ] Tabelas criadas (6 tabelas)
- [ ] Usuários inseridos (3 usuários)
- [ ] Pacientes importados (~2000)
- [ ] Modelo treinado (`melhor_modelo.pkl` existe)
- [ ] Interface iniciada (http://localhost:8501)
- [ ] Login funciona (medico/medico123)
- [ ] Dashboard mostra dados
- [ ] Pode adicionar paciente
- [ ] Pode fazer análise com IA
- [ ] Resultado salvo no banco
- [ ] Histórico atualizado no dashboard

---

## 📈 Próximas Melhorias

- [ ] Adicionar CRUD completo de tipos de exame
- [ ] Gráficos de tendência de pacientes
- [ ] Exportar relatórios em PDF
- [ ] Sistema de notificações
- [ ] Dark mode
- [ ] Filtros avançados
- [ ] Autenticação com 2FA

---

## 📚 Documentação Adicional

Consulte também:
- `10_Banco_Dados/README.md` — Schema SQL
- `04_Interface/README_V2.md` — Interface detalhada
- `08_Documentacao/` — Guias gerais

---

## 🎓 Conclusão

Você completou com sucesso:

✅ **AULA_09 Passo 1:** Banco de dados relacional  
✅ **AULA_09 Passo 2:** Interface com login e CRUD  

**Status:** 🎉 **AULA_09 COMPLETA!**

Agora você tem um **sistema de diagnóstico clínico profissional** com:
- Autenticação segura (SHA256)
- Banco de dados persistente (SQLite)
- Interface amigável (Streamlit)
- Integração com IA (modelo 98.75% acurado)
- CRUD completo (pacientes, resultados)
- Dashboard com métricas

---

**Versão:** 1.0  
**Data:** 04/2026  
**Status:** ✅ Pronto para produção
