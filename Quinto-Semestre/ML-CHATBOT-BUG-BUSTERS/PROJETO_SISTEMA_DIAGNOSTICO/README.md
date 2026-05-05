# 🏥 SISTEMA DE DIAGNÓSTICO DE RISCO CLÍNICO

## ✨ Visão Geral

Sistema completo de **previsão de risco clínico** usando **Machine Learning (Random Forest)**. Classifica pacientes em 3 níveis de risco (Baixo/Médio/Alto) baseado em 5 características biomédicas.

**Acurácia: 98.75% ✅**

---

## 🚀 Começar em 45 Segundos

### Windows

1. **Instale dependências:**
   ```bash
   pip install pandas numpy scikit-learn matplotlib joblib fastapi uvicorn streamlit requests
   ```

2. **Execute tudo de uma vez:**
   ```bash
   09_Scripts_Uteis/run_all.bat
   ```

3. **Acesse no navegador:**
   - Interface: http://localhost:8501
   - API Docs: http://localhost:8000/docs

4. **Pronto!** Sistema está rodando 🎉

---

## 📋 Estrutura de Pastas

```
PROJETO_SISTEMA_DIAGNOSTICO/
│
├── 01_Dataset/                    # Gera 2000 registros
├── 02_ML_Pipeline/                # Treina 3 modelos (RF vence!)
├── 03_API/                        # FastAPI (porta 8000)
├── 04_Interface/                  # Streamlit UI (porta 8501)
│
├── 05_Dados/                      # Dataset pacientes.csv
├── 06_Modelos/                    # Modelos .pkl serializados
├── 07_Graficos/                   # Gráficos PNG
├── 08_Documentacao/               # Guias e análises
├── 09_Scripts_Uteis/              # Scripts .bat
│
└── README.md                      # Este arquivo
```

---

## 📊 Resultados

| Métrica | Valor |
|---------|-------|
| Melhor Modelo | Random Forest |
| Acurácia | **98.75%** ✅ |
| F1-Score | **98.74%** ✅ |
| AUC (ROC) | **1.00** (Perfeito) |

---

## 🎯 Como Funciona

### 1️⃣ Input
```json
{
  "nome": "João Silva",
  "idade": 63,
  "glicose": 148.0,
  "pressao": 155.0,
  "imc": 31.5,
  "colesterol": 248.0
}
```

### 2️⃣ Processamento
- Normaliza features
- Passa pelo Random Forest treinado
- Calcula probabilidades

### 3️⃣ Output
```json
{
  "risco_classificacao": "Alto",
  "probabilidade": 0.95,
  "explicacao": "Paciente apresenta glicose elevada, hipertensão, obesidade, colesterol alto."
}
```

---

## 🔧 Componentes

### 📊 Dataset (01_Dataset/)
- 2000 registros de pacientes sintéticos
- Distribuição realista de dados biomédicos
- Script: `1_gerar_dataset.py`

### 🧠 ML Pipeline (02_ML_Pipeline/)
- Treina 3 modelos em paralelo
- Valida com 5-fold cross-validation
- Seleciona melhor (Random Forest)
- Script: `2_pipeline_ml.py`

### 🌐 API REST (03_API/)
- Endpoints: `/predict`, `/health`, `/info`
- Framework: FastAPI
- Porta: 8000
- Script: `api_biomedicina.py`

### 🎨 Interface Web (04_Interface/)
- Formulário amigável
- Indicadores em tempo real
- Framework: Streamlit
- Porta: 8501
- Script: `interface_streamlit.py`

---

## 📖 Documentação

| Arquivo | Descrição |
|---------|-----------|
| **08_Documentacao/README_SISTEMA.md** | Visão geral completa |
| **08_Documentacao/GUIA_EXECUCAO.md** | Passo a passo detalhado |
| **08_Documentacao/ANALISE_ARQUIVOS_CLAUDE.md** | Análise técnica |
| **08_Documentacao/ANALISE_AULA08_CHECKLIST.md** | Checklist de requisitos |
| **08_Documentacao/COMPATIBILIDADE_AULA09_READINESS.md** | Preparação para AULA_09 |

---

## 🛠️ Scripts Auxiliares

```bash
09_Scripts_Uteis/run_all.bat      # Executa tudo (4 terminais)
09_Scripts_Uteis/run_dataset.bat  # Apenas dataset
09_Scripts_Uteis/run_pipeline.bat # Apenas ML
09_Scripts_Uteis/run_api.bat      # Apenas API
09_Scripts_Uteis/run_ui.bat       # Apenas Streamlit
```

---

## 💻 Requisitos

- Python 3.10+
- pip
- ~200 MB espaço em disco

---

## ⏱️ Timeline

```
Gerar Dataset     :  ~5s
Treinar Modelos   : ~30s
Iniciar API       :  ~3s
Iniciar Streamlit :  ~5s
────────────────────────
Total            : ~45s
```

---

## 🐛 Troubleshooting

### API não conecta
```bash
# Verifique se está rodando
curl http://localhost:8000/health

# Reinicie
09_Scripts_Uteis/run_api.bat
```

### Erro ao gerar dataset
```bash
# Executar manualmente
cd 01_Dataset
python 1_gerar_dataset.py
```

### Porta já em uso
```bash
# Mude a porta na API
uvicorn api_biomedicina:app --port 8001
```

---

## 📚 Próximos Passos

1. ✅ Execute o sistema completo
2. ✅ Teste com diferentes dados
3. ✅ Explore o Swagger UI em http://localhost:8000/docs
4. ✅ Leia documentação em `08_Documentacao/`
5. ✅ Prepare apresentação para AULA_09

---

## 🎓 Contexto Acadêmico

- **Curso:** ML-CHATBOT-BUG-BUSTERS
- **Semestre:** 5º
- **Aulas:** 
  - ✅ AULA_08: Sistema completo (Dataset + ML + API + UI)
  - ✅ AULA_09: Banco de dados + Interface com Login
- **Prazo:** 04/05/2026

---

## 🎉 NOVIDADE: AULA_09 — Banco de Dados + Login

### ✨ Nova Pasta: `10_Banco_Dados/`

Implementação de **SQLite** com 5 tabelas relacionadas:

```
usuarios          (login + segurança)
  ↓
tipos_exame       (definição de exames)
  ↓
pacientes         (dados demográficos) ← ~2000 importados do CSV
  ↓
exames_paciente   (histórico de exames)
  ↓
resultados        (predições IA salvas)
```

### ✨ Nova Versão: Interface Streamlit v2.0

```
04_Interface/interface_streamlit_v2.py

├─ 🔐 Login
│  └─ Validação com banco SQL (SHA256)
│
├─ 📊 Dashboard
│  └─ Estatísticas + últimas análises
│
├─ 👥 Gestão de Pacientes
│  └─ CRUD (listar, adicionar)
│
└─ 🤖 Análise de Risco
   └─ Predição com IA + salvamento no banco
```

### 🚀 Como Usar (AULA_09)

**1. Criar Banco de Dados:**
```bash
python 10_Banco_Dados/criar_banco_dados.py
```

**2. Treinar Modelo:**
```bash
python 02_ML_Pipeline/2_pipeline_ml.py
```

**3. Iniciar Interface v2.0:**
```bash
streamlit run 04_Interface/interface_streamlit_v2.py
```

**4. Fazer Login:**
- Usuário: `medico`
- Senha: `medico123`

### 📚 Documentação AULA_09

- `08_Documentacao/GUIA_AULA09.md` — **Guia completo passo a passo**
- `10_Banco_Dados/README.md` — Schema SQL detalhado
- `04_Interface/README_V2.md` — Funcionalidades da interface

### ✅ Checklist AULA_09

- [x] Banco de dados relacional (SQLite) criado
- [x] 5 tabelas com relacionamentos
- [x] ~2000 pacientes importados de CSV
- [x] 3 usuários padrão (admin, medico, medico2)
- [x] 7 tipos de exame com limites normais/alerta
- [x] Interface Streamlit v2.0 com login
- [x] CRUD de pacientes funcionando
- [x] Análise com IA (modelo .pkl)
- [x] Salvamento de resultados no banco
- [x] Dashboard com estatísticas
- [x] Segurança: SHA256 para senhas

---

## 📄 Licença

Código disponível para fins educacionais.

---

## 👤 Desenvolvido

Como parte do curso ML-CHATBOT-BUG-BUSTERS.

---

**Status:** ✅ **AULA_08 + AULA_09 COMPLETO**  
**Acurácia:** 98.75%  
**Banco de Dados:** SQLite (clinica.db)  
**Versão Interface:** 2.0 (com login)  
**Última Atualização:** 02/04/2026
