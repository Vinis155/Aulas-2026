"""
=============================================================================
CRIAÇÃO DO BANCO DE DADOS — SISTEMA DE DIAGNÓSTICO CLÍNICO
=============================================================================
Projeto  : Sistema de Diagnóstico de Risco Clínico v2.0
Arquivo  : criar_banco_dados.py
Função   : Criar banco SQLite + tabelas + importar dados CSV

Criará:
    1. clinica.db (SQLite)
    2. Tabelas: usuarios, tipos_exame, pacientes, exames_paciente, resultados
    3. Usuários padrão (admin, medico)
    4. Tipos de exame com limites normais/alerta
    5. Importação de pacientes do CSV

Como rodar:
    python 10_Banco_Dados/criar_banco_dados.py
=============================================================================
"""

import sqlite3
import os
import pandas as pd
import hashlib
from datetime import datetime

# ── CAMINHOS ───────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "clinica.db")
CSV_PATH = os.path.join(BASE_DIR, "..", "05_Dados", "pacientes.csv")

print("=" * 70)
print("  CRIAÇÃO DO BANCO DE DADOS — SISTEMA CLÍNICO")
print("=" * 70)
print()

# ── FUNCOES AUXILIARES ─────────────────────────────────────────────────────
def hash_senha(senha):
    """Gera hash SHA256 da senha"""
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_conexao():
    """Cria conexão com SQLite"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ── PASSO 1: DELETAR BANCO ANTIGO (se existir) ────────────────────────────
print("[PASSO 1] Verificando banco antigo...")
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
    print(f"  ✓ Banco antigo removido")
else:
    print(f"  ✓ Nenhum banco antigo encontrado")

# ── PASSO 2: CRIAR CONEXÃO ─────────────────────────────────────────────────
print("\n[PASSO 2] Criando conexão com SQLite...")
conn = criar_conexao()
cursor = conn.cursor()
print(f"  ✓ Banco criado em: {DB_PATH}")

# ── PASSO 3: CRIAR TABELA DE USUARIOS ──────────────────────────────────────
print("\n[PASSO 3] Criando tabela 'usuarios'...")
cursor.execute("""
    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        senha_hash TEXT NOT NULL,
        nome TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'medico',
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ativo BOOLEAN DEFAULT 1
    )
""")
print("  ✓ Tabela 'usuarios' criada")

# ── PASSO 4: CRIAR TABELA DE TIPOS DE EXAME ────────────────────────────────
print("\n[PASSO 4] Criando tabela 'tipos_exame'...")
cursor.execute("""
    CREATE TABLE tipos_exame (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        unidade TEXT NOT NULL,
        valor_normal_min REAL,
        valor_normal_max REAL,
        valor_alerta_min REAL,
        valor_alerta_max REAL,
        valor_critico_min REAL,
        valor_critico_max REAL,
        descricao TEXT,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
print("  ✓ Tabela 'tipos_exame' criada")

# ── PASSO 5: CRIAR TABELA DE PACIENTES ─────────────────────────────────────
print("\n[PASSO 5] Criando tabela 'pacientes'...")
cursor.execute("""
    CREATE TABLE pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        genero TEXT,
        cpf TEXT UNIQUE,
        email TEXT,
        telefone TEXT,
        endereco TEXT,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ativo BOOLEAN DEFAULT 1
    )
""")
print("  ✓ Tabela 'pacientes' criada")

# ── PASSO 6: CRIAR TABELA DE EXAMES DO PACIENTE ────────────────────────────
print("\n[PASSO 6] Criando tabela 'exames_paciente'...")
cursor.execute("""
    CREATE TABLE exames_paciente (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        tipo_exame_id INTEGER NOT NULL,
        valor REAL NOT NULL,
        data_exame TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        observacao TEXT,
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
        FOREIGN KEY (tipo_exame_id) REFERENCES tipos_exame(id)
    )
""")
print("  ✓ Tabela 'exames_paciente' criada")

# ── PASSO 7: CRIAR TABELA DE RESULTADOS (IA) ───────────────────────────────
print("\n[PASSO 7] Criando tabela 'resultados'...")
cursor.execute("""
    CREATE TABLE resultados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        risco_codigo INTEGER NOT NULL,
        risco_classificacao TEXT NOT NULL,
        probabilidade REAL,
        explicacao TEXT,
        modelo_usado TEXT DEFAULT 'Random Forest',
        data_analise TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
    )
""")
print("  ✓ Tabela 'resultados' criada")

# ── PASSO 8: INSERIR USUÁRIOS PADRÃO ───────────────────────────────────────
print("\n[PASSO 8] Inserindo usuários padrão...")

usuarios = [
    ("admin", hash_senha("admin123"), "Administrador", "admin"),
    ("medico", hash_senha("medico123"), "Dr. Carlos Silva", "medico"),
    ("medico2", hash_senha("senha456"), "Dra. Marina Costa", "medico"),
]

for username, senha_hash, nome, role in usuarios:
    cursor.execute("""
        INSERT INTO usuarios (username, senha_hash, nome, role)
        VALUES (?, ?, ?, ?)
    """, (username, senha_hash, nome, role))

print(f"  ✓ {len(usuarios)} usuários criados")

# ── PASSO 9: INSERIR TIPOS DE EXAME ────────────────────────────────────────
print("\n[PASSO 9] Inserindo tipos de exame...")

tipos_exame = [
    ("Glicose", "mg/dL", 70, 100, 100, 125, 126, 350, "Glicemia de jejum"),
    ("Pressão Arterial", "mmHg", 0, 120, 120, 140, 140, 220, "Pressão sistólica"),
    ("IMC", "kg/m²", 18.5, 25, 25, 30, 30, 55, "Índice de Massa Corporal"),
    ("Colesterol Total", "mg/dL", 0, 200, 200, 240, 240, 400, "Colesterol total"),
    ("HDL", "mg/dL", 40, 60, 30, 40, 0, 30, "Colesterol bom"),
    ("LDL", "mg/dL", 0, 100, 100, 130, 130, 300, "Colesterol ruim"),
    ("Triglicerídeos", "mg/dL", 0, 150, 150, 200, 200, 500, "Triglicerídeos"),
]

for nome, unidade, norm_min, norm_max, alrt_min, alrt_max, crit_min, crit_max, desc in tipos_exame:
    cursor.execute("""
        INSERT INTO tipos_exame 
        (nome, unidade, valor_normal_min, valor_normal_max, 
         valor_alerta_min, valor_alerta_max, valor_critico_min, valor_critico_max, descricao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, unidade, norm_min, norm_max, alrt_min, alrt_max, crit_min, crit_max, desc))

print(f"  ✓ {len(tipos_exame)} tipos de exame criados")

# ── PASSO 10: IMPORTAR PACIENTES DO CSV ────────────────────────────────────
print("\n[PASSO 10] Importando pacientes do CSV...")

if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
    
    for idx, row in df.iterrows():
        cursor.execute("""
            INSERT INTO pacientes (nome, idade)
            VALUES (?, ?)
        """, (str(row['nome']), int(row['idade'])))
    
    print(f"  ✓ {len(df)} pacientes importados do CSV")
else:
    print(f"  ⚠ Arquivo CSV não encontrado: {CSV_PATH}")
    print(f"    Execute antes: python 01_Dataset/1_gerar_dataset.py")

# ── PASSO 11: COMMIT E FECHAMENTO ──────────────────────────────────────────
print("\n[PASSO 11] Salvando banco de dados...")
conn.commit()
conn.close()
print(f"  ✓ Banco de dados salvo com sucesso")

# ── RELATÓRIO FINAL ────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("  BANCO DE DADOS CRIADO COM SUCESSO!")
print("=" * 70)
print()
print("📊 Resumo:")
print(f"  • Arquivo: {DB_PATH}")
print(f"  • Tabelas: 6 (usuarios, tipos_exame, pacientes, exames_paciente, resultados)")
print(f"  • Usuários: 3")
print(f"  • Tipos de Exame: {len(tipos_exame)}")
print()
print("👤 Usuários Padrão:")
print("  • admin / admin123 (Administrador)")
print("  • medico / medico123 (Médico)")
print("  • medico2 / senha456 (Médico 2)")
print()
print("✅ Próximos passos:")
print("  1. Execute: python 04_Interface/interface_streamlit_v2.py")
print("  2. Acesse: http://localhost:8501")
print("  3. Login com as credenciais acima")
print()
print("=" * 70)
