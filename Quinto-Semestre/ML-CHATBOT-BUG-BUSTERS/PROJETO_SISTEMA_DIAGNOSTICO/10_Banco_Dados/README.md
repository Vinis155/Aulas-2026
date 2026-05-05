# 🗄️ Banco de Dados — Sistema de Diagnóstico Clínico

## Visão Geral

Este diretório contém os scripts para criar e gerenciar o banco de dados SQLite (`clinica.db`) que persiste todos os dados do sistema de diagnóstico clínico.

---

## 📋 Schema do Banco de Dados

### Tabela: `usuarios`
Armazena credenciais de acesso dos médicos.

```sql
├─ id (INTEGER, PK)
├─ username (TEXT, UNIQUE)
├─ senha_hash (TEXT) — SHA256
├─ nome (TEXT)
├─ role (TEXT) — 'admin' ou 'medico'
├─ data_criacao (TIMESTAMP)
└─ ativo (BOOLEAN)
```

**Registros Padrão:**
- admin / admin123 (Administrador)
- medico / medico123 (Médico)
- medico2 / senha456 (Médico 2)

---

### Tabela: `tipos_exame`
Define os tipos de exames com limites normais e de alerta.

```sql
├─ id (INTEGER, PK)
├─ nome (TEXT, UNIQUE)
├─ unidade (TEXT) — ex: 'mg/dL', 'mmHg'
├─ valor_normal_min (REAL)
├─ valor_normal_max (REAL)
├─ valor_alerta_min (REAL)
├─ valor_alerta_max (REAL)
├─ valor_critico_min (REAL)
├─ valor_critico_max (REAL)
├─ descricao (TEXT)
└─ data_criacao (TIMESTAMP)
```

**Exames Padrão:**
1. Glicose (mg/dL)
2. Pressão Arterial (mmHg)
3. IMC (kg/m²)
4. Colesterol Total (mg/dL)
5. HDL (mg/dL)
6. LDL (mg/dL)
7. Triglicerídeos (mg/dL)

---

### Tabela: `pacientes`
Armazena dados demográficos dos pacientes.

```sql
├─ id (INTEGER, PK)
├─ nome (TEXT)
├─ idade (INTEGER)
├─ genero (TEXT)
├─ cpf (TEXT, UNIQUE)
├─ email (TEXT)
├─ telefone (TEXT)
├─ endereco (TEXT)
├─ data_cadastro (TIMESTAMP)
└─ ativo (BOOLEAN)
```

**Preenchimento:** Importado de `05_Dados/pacientes.csv` (~2000 registros)

---

### Tabela: `exames_paciente`
Histórico de exames realizados para cada paciente.

```sql
├─ id (INTEGER, PK)
├─ paciente_id (INTEGER, FK) → pacientes.id
├─ tipo_exame_id (INTEGER, FK) → tipos_exame.id
├─ valor (REAL)
├─ data_exame (TIMESTAMP)
└─ observacao (TEXT)
```

---

### Tabela: `resultados`
Resultados de análises de risco (predições da IA).

```sql
├─ id (INTEGER, PK)
├─ paciente_id (INTEGER, FK) → pacientes.id
├─ risco_codigo (INTEGER) — 0, 1 ou 2
├─ risco_classificacao (TEXT) — 'Baixo', 'Médio', 'Alto'
├─ probabilidade (REAL) — confiança 0-1
├─ explicacao (TEXT)
├─ modelo_usado (TEXT) — ex: 'Random Forest'
└─ data_analise (TIMESTAMP)
```

---

## 🚀 Como Usar

### 1️⃣ Criar/Recriar o Banco

```bash
python 10_Banco_Dados/criar_banco_dados.py
```

**Resultado:**
- `clinica.db` criado na raiz do projeto
- Todas as 6 tabelas criadas
- Usuários padrão inseridos
- Tipos de exame inseridos
- Pacientes importados do CSV

### 2️⃣ Pré-requisitos

**Antes de executar, garanta que:**
- ✅ O arquivo `05_Dados/pacientes.csv` existe
- ✅ O CSV foi gerado por: `python 01_Dataset/1_gerar_dataset.py`

### 3️⃣ Credenciais Padrão

| Usuário | Senha | Função |
|---------|-------|--------|
| admin | admin123 | Administrador |
| medico | medico123 | Médico |
| medico2 | senha456 | Médico |

---

## 🔐 Segurança

### Senhas
- Armazenadas como **SHA256** (não reversível)
- Função: `hashlib.sha256(senha.encode()).hexdigest()`
- **Não armazenar em plain text**

### Validação
- Login valida: `username` + `senha_hash` + `ativo = 1`
- Todas as operações SQL usam **prepared statements** (proteção contra SQL injection)

---

## 📊 Consultas Úteis

### Ver Todos os Usuários
```sql
SELECT username, role, ativo FROM usuarios;
```

### Ver Todos os Pacientes
```sql
SELECT id, nome, idade FROM pacientes;
```

### Ver Exames de um Paciente (id=1)
```sql
SELECT te.nome, ep.valor, te.unidade, ep.data_exame
FROM exames_paciente ep
JOIN tipos_exame te ON ep.tipo_exame_id = te.id
WHERE ep.paciente_id = 1
ORDER BY ep.data_exame DESC;
```

### Ver Resultados de Análise (últimos 10)
```sql
SELECT p.nome, r.risco_classificacao, r.probabilidade, r.data_analise
FROM resultados r
JOIN pacientes p ON r.paciente_id = p.id
ORDER BY r.data_analise DESC
LIMIT 10;
```

---

## 🛠️ Troubleshooting

### Erro: "Arquivo CSV não encontrado"
**Solução:** Execute primeiro:
```bash
python 01_Dataset/1_gerar_dataset.py
```

### Erro: "Banco de dados bloqueado"
**Solução:** Feche a interface Streamlit e tente novamente:
```bash
# Pressione Ctrl+C na janela do Streamlit
python 10_Banco_Dados/criar_banco_dados.py
```

### Erro: "UNIQUE constraint failed"
**Solução:** O banco já existe. A script pergunta se deseja recriá-lo:
```
⚠️  Banco de dados já existe: clinica.db
Deseja recriá-lo? (s/n): s
```

---

## 📈 Próximos Passos

1. ✅ **Banco criado** → Agora execute:
```bash
python 02_ML_Pipeline/2_pipeline_ml.py
```

2. 🤖 **Modelo treinado** → Agora inicie a interface:
```bash
streamlit run 04_Interface/interface_streamlit_v2.py
```

3. 🌐 **Interface rodando** → Acesse:
```
http://localhost:8501
```

---

## 📝 Logs de Execução

A cada execução do `criar_banco_dados.py`, você verá:

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

...

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

---

## 🔗 Relacionamentos

```
usuarios
  ↓
  └─ (sem FK direto, apenas validação em interface)

tipos_exame
  ↓
  └─→ exames_paciente.tipo_exame_id

pacientes
  ├─→ exames_paciente.paciente_id
  └─→ resultados.paciente_id
```

---

## 💾 Backup & Restauração

### Fazer Backup
```bash
cp clinica.db clinica_backup_$(date +%Y%m%d_%H%M%S).db
```

### Restaurar do Backup
```bash
cp clinica_backup_20260402_143000.db clinica.db
```

---

**Arquivo:** `AULA_09/Passo 1 — Banco de Dados`  
**Versão:** 2.0  
**Data:** 04/2026  
**Status:** ✅ Pronto para uso
