# 🛠️ Módulo 9: Scripts Auxiliares

## Objetivo

Fornecer scripts de conveniência para executar componentes do sistema sem digitar comandos longos.

## Arquivos

### Windows Batch Scripts (.bat)

- **`run_all.bat`** - Executa tudo (abre 3 terminais)
- **`run_dataset.bat`** - Executa apenas o gerador de dataset
- **`run_pipeline.bat`** - Executa apenas o pipeline ML
- **`run_api.bat`** - Inicia a API
- **`run_ui.bat`** - Inicia a Interface Streamlit

## Como Usar

### Opção 1: Executar Tudo

```bash
run_all.bat
```

Abre automaticamente:
1. ✅ Dataset Generator (Terminal 1)
2. ✅ ML Pipeline (Terminal 2)
3. ✅ API Server (Terminal 3 - permanente)
4. ✅ Streamlit UI (Terminal 4 - permanente)

### Opção 2: Executar Componentes Individuais

**Apenas Dataset:**
```bash
run_dataset.bat
```

**Apenas Pipeline:**
```bash
run_pipeline.bat
```

**Apenas API:**
```bash
run_api.bat
```

**Apenas Interface:**
```bash
run_ui.bat
```

## Detalhes de Cada Script

### run_all.bat
```batch
@echo off
start cmd /k "cd 01_Dataset && python 1_gerar_dataset.py"
timeout /t 10 /nobreak
start cmd /k "cd 02_ML_Pipeline && python 2_pipeline_ml.py"
timeout /t 35 /nobreak
start cmd /k "cd 03_API && uvicorn api_biomedicina:app --port 8000"
timeout /t 5 /nobreak
start cmd /k "cd 04_Interface && streamlit run interface_streamlit.py"
```

**Sequência:**
1. Abre Dataset (espera 10s)
2. Abre Pipeline (espera 35s)
3. Abre API (espera 5s)
4. Abre Streamlit

### run_dataset.bat
```batch
@echo off
cd 01_Dataset
python 1_gerar_dataset.py
pause
```

### run_pipeline.bat
```batch
@echo off
cd 02_ML_Pipeline
python 2_pipeline_ml.py
pause
```

### run_api.bat
```batch
@echo off
cd 03_API
uvicorn api_biomedicina:app --port 8000
pause
```

### run_ui.bat
```batch
@echo off
cd 04_Interface
streamlit run interface_streamlit.py
```

## Tempos de Espera

```
Run All Script Sequence:
├─ Dataset start
│  └─ wait 10s (dataset termina ~5s)
├─ Pipeline start
│  └─ wait 35s (pipeline termina ~30s)
├─ API start
│  └─ wait 5s (API inicia ~3s)
└─ Streamlit start
   └─ UI abre no navegador (~5s)
```

## Troubleshooting

### ❌ Scripts não abrem
**Problema:** Extensão .bat não associada a cmd.exe

**Solução:**
1. Duplo clique no arquivo .bat
2. Se pedir programa, selecione cmd.exe

### ❌ "python not recognized"
**Problema:** Python não está no PATH

**Solução:**
```bash
# Verifique Python
python --version

# Se não funcionar, instale ou adicione ao PATH
```

### ❌ "Permission denied"
**Problema:** Permissões insuficientes

**Solução:**
1. Execute como Administrador
2. Ou execute os comandos manualmente

---

## Alternativa: Executar Manualmente

Se preferir não usar scripts, execute em 2-4 terminais:

**Terminal 1: Dataset + Pipeline**
```bash
cd 01_Dataset && python 1_gerar_dataset.py
cd ../02_ML_Pipeline && python 2_pipeline_ml.py
```

**Terminal 2: API**
```bash
cd 03_API
uvicorn api_biomedicina:app --port 8000
```

**Terminal 3: Streamlit**
```bash
cd 04_Interface
streamlit run interface_streamlit.py
```

---

## Criar Seus Próprios Scripts

Você pode personalizar os scripts. Exemplos:

**Usar porta diferente:**
```batch
cd 03_API
uvicorn api_biomedicina:app --port 8001
```

**Adicionar logging:**
```batch
cd 02_ML_Pipeline
python 2_pipeline_ml.py > log_pipeline.txt 2>&1
```

**Executar com timeout:**
```batch
cd 01_Dataset
timeout /t 60
python 1_gerar_dataset.py
```

---

**Status:** ✅ Pronto para usar  
**Data:** 27/04/2026
