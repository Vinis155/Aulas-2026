# 🚀 GUIA DE EXECUÇÃO — Sistema de Diagnóstico de Risco Clínico

## 📋 Pré-requisitos

- ✅ Python 3.10+ instalado
- ✅ pip funcional
- ✅ Navegador web (Chrome/Firefox/Edge)
- ✅ Terminal com permissões normais

## 🔧 Instalação de Dependências

### Windows (cmd ou PowerShell)

```bash
pip install pandas numpy scikit-learn matplotlib joblib fastapi uvicorn streamlit requests
```

### Linux/macOS

```bash
pip install pandas numpy scikit-learn matplotlib joblib fastapi uvicorn streamlit requests
```

### Verificar Instalação

```bash
python -c "import pandas, numpy, sklearn, matplotlib, joblib, fastapi, uvicorn, streamlit, requests; print('✅ Todas as dependências instaladas')"
```

---

## 📊 PASSO 1: Gerar Dataset

### Terminal Único (não precisa de paralelo)

```bash
cd 01_Dataset
python 1_gerar_dataset.py
```

### Output Esperado

```
============================================================
  GERADOR DE DATASET — RISCO CLINICO
============================================================
  Registros gerados : 2000

  Distribuicao das classes de risco:
    Classe 0 (Baixo):  325  16.2%  ########
    Classe 1 (Medio):  1367 68.3%  ##################################
    Classe 2 (Alto ):  308  15.4%  #######

  Arquivo '../05_Dados/pacientes.csv' salvo com sucesso.
============================================================
```

### Verificação

Arquivo `05_Dados/pacientes.csv` foi criado? ✅ SIM → Continue

---

## 🧠 PASSO 2: Treinar Modelos de ML

### Terminal Único

```bash
cd ../02_ML_Pipeline
python 2_pipeline_ml.py
```

### Output Esperado

```
============================================================
  SISTEMA DE PREVISAO DE RISCO CLINICO — PIPELINE ML
============================================================

[ETAPA 1] Lendo 'pacientes.csv'...
  Shape            : (2000, 7)  (linhas x colunas)
  ...

[ETAPA 8] Comparacao e selecao do melhor modelo...

  RANKING (por F1-Score ponderado):
  1. Random Forest       F1=0.9874  Acuracia=0.9875  ⭐ MELHOR
  2. KNN                F1=0.8708  Acuracia=0.8750
  3. Regressão Logística F1=0.7489  Acuracia=0.7625

  >>> MELHOR MODELO: Random Forest <<<

[ETAPA 11] Salvando modelo e scaler para producao...

  [OK] Modelo 'Random Forest' salvo como './06_Modelos/melhor_modelo.pkl'
  [OK] StandardScaler salvo como './06_Modelos/scaler.pkl'
  [OK] Metadados salvos como './06_Modelos/metadados_modelo.pkl'

Pipeline concluido com sucesso.
✅ Pronto para usar na API e Interface!
============================================================
```

### Verificação

Arquivos criados em `06_Modelos/`? ✅ SIM (3 arquivos .pkl)  
Gráficos criados em `07_Graficos/`? ✅ SIM (3 arquivos .png)  
Continue → Continue

---

## 🌐 PASSO 3: Iniciar API REST

### Terminal 1 (dedicado à API)

```bash
cd ../03_API
uvicorn api_biomedicina:app --port 8000
```

### Output Esperado

```
INFO:     Carregando modelo treinado...
INFO:     ✅ Modelo carregado com sucesso
INFO:     Carregando scaler (normalizador)...
INFO:     ✅ Scaler carregado com sucesso
INFO:     Carregando metadados...
INFO:     ✅ Metadados carregados: Random Forest
INFO:     Acurácia: 0.9875
INFO:     F1-Score: 0.9874
INFO:     Uvicorn running on http://0.0.0.0:8000 [Press CTRL+C to quit]
```

### Verificação

Acesse no navegador:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/health

Ambas funcionando? ✅ SIM → Continue  
❌ NÃO? Verifique se porta 8000 está disponível

### ⚠️ MANTER ESTE TERMINAL ABERTO

Deixe este terminal rodando enquanto usar o sistema.

---

## 🎨 PASSO 4: Iniciar Interface Streamlit

### Terminal 2 (dedicado à Interface)

```bash
cd ../04_Interface
streamlit run interface_streamlit.py
```

### Output Esperado

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Navegador

Abre automaticamente em `http://localhost:8501`?  
Se não, acesse manualmente.

### Verificação

✅ Página carregou?  
✅ Formulário visível?  
✅ Indicador da API mostra "✅ API conectada"?  

Tudo OK? → Continue  
Erro na API? → Volte ao Terminal 1 e verifique

---

## 🩺 PASSO 5: Testar Diagnóstico

### No Navegador (Streamlit)

1. Preencha o formulário:
   - **Nome:** João Silva
   - **Idade:** 63
   - **Glicose:** 148.0
   - **Pressão:** 155.0
   - **IMC:** 31.5
   - **Colesterol:** 248.0

2. Clique no botão **"🔍 Fazer Diagnóstico"**

3. Resultado esperado:
   ```
   ❌ Risco Alto (2)
   Probabilidade: 95%
   Explicação: Paciente apresenta glicose elevada (possível diabetes), hipertensão, 
              obesidade, colesterol alto.
   ```

4. Pode baixar resultado em JSON clicando em **"📥 Baixar resultado"**

### ✅ Sucesso

Se viu o resultado acima, o sistema está funcionando!

---

## 🧪 PASSO 6: Testar com curl (Opcional)

### No Terminal (sem abrir navegador)

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "nome":"Maria Santos",
       "idade":63,
       "glicose":148.0,
       "pressao":155.0,
       "imc":31.5,
       "colesterol":248.0
     }'
```

### Esperado

```json
{
  "nome": "Maria Santos",
  "idade": 63,
  "risco_codigo": 2,
  "risco_classificacao": "Alto",
  "probabilidade": 0.95,
  "explicacao": "Paciente apresenta..."
}
```

---

## 🛑 Parar o Sistema

### Para fechar tudo:

1. **Terminal 1 (API):** Pressione `Ctrl+C`
2. **Terminal 2 (Streamlit):** Pressione `Ctrl+C`
3. **Navegador:** Feche a aba

---

## 📁 Estrutura de Pastas (Após Execução)

```
PROJETO_SISTEMA_DIAGNOSTICO/
├── 01_Dataset/
│   ├── 1_gerar_dataset.py
│   └── README.md
├── 02_ML_Pipeline/
│   ├── 2_pipeline_ml.py
│   └── README.md
├── 03_API/
│   ├── api_biomedicina.py
│   └── README.md
├── 04_Interface/
│   ├── interface_streamlit.py
│   └── README.md
├── 05_Dados/
│   ├── pacientes.csv ✅ GERADO
│   └── README.md
├── 06_Modelos/
│   ├── melhor_modelo.pkl ✅ GERADO
│   ├── scaler.pkl ✅ GERADO
│   ├── metadados_modelo.pkl ✅ GERADO
│   └── README.md
├── 07_Graficos/
│   ├── graficos_comparacao.png ✅ GERADO
│   ├── matriz_confusao.png ✅ GERADO
│   ├── curva_roc.png ✅ GERADO
│   └── README.md
├── 08_Documentacao/
│   ├── README_SISTEMA.md
│   ├── GUIA_EXECUCAO.md (este arquivo)
│   └── ...
└── 09_Scripts_Uteis/
    └── ...
```

---

## 🐛 Troubleshooting

### ❌ "Connection refused" ao acessar API

**Problema:** Streamlit não consegue conectar à API

**Solução:**
1. Verifique se Terminal 1 (API) está rodando
2. Verifique se porta 8000 está livre: `netstat -ano | findstr :8000` (Windows)
3. Reinicie ambos os terminais

### ❌ "ModuleNotFoundError: No module named 'fastapi'"

**Problema:** Dependências não instaladas

**Solução:**
```bash
pip install -r requirements.txt
```

### ❌ "Port 8000 already in use"

**Problema:** Outra aplicação usando a porta 8000

**Solução:**
```bash
# Encontre qual processo está usando a porta
netstat -ano | findstr :8000

# Mate o processo
taskkill /PID <PID> /F

# Ou use porta diferente
uvicorn api_biomedicina:app --port 8001
```

### ❌ "FileNotFoundError: pacientes.csv not found"

**Problema:** Dataset não foi gerado

**Solução:**
1. Volte ao PASSO 1
2. Execute `python 1_gerar_dataset.py`
3. Verifique arquivo em `05_Dados/pacientes.csv`

### ❌ Streamlit abre mas não consegue fazer diagnóstico

**Problema:** Provavelmente erro na API

**Solução:**
1. Vá ao Terminal 1 (API)
2. Procure por mensagens de erro (vermelha)
3. Se estiver vermelho, reexecute todo o pipeline

---

## ⏱️ Tempo Total de Execução

```
PASSO 1 (Gerar Dataset)    :  ~5 segundos
PASSO 2 (Treinar Modelos)  : ~30 segundos
PASSO 3 (Iniciar API)      :  ~3 segundos
PASSO 4 (Iniciar Streamlit):  ~5 segundos
PASSO 5 (Fazer Diagnóstico):  <1 segundo
──────────────────────────────────────────
TOTAL                      : ~45 segundos
```

---

## ✅ Checklist Final

- [ ] Dependencies instaladas
- [ ] Dataset gerado (pacientes.csv)
- [ ] Modelos treinados (3 arquivos .pkl)
- [ ] Gráficos gerados (3 arquivos .png)
- [ ] API rodando sem erros
- [ ] Streamlit acessível
- [ ] Diagnóstico funciona
- [ ] Resultado exibido corretamente

Se todos os itens estão marcados: **🎉 SUCESSO!**

---

## 📞 Suporte

- Verifique mensagens de erro no terminal
- Leia o `README_SISTEMA.md` para mais contexto
- Consulte README.md de cada módulo específico

---

**Última Atualização:** 27/04/2026  
**Status:** ✅ Testado e Funcionando
