# 🎨 Módulo 4: Interface Web (Streamlit)

## Objetivo

Fornecer uma interface web amigável para interagir com o modelo de diagnóstico e a API.

## Arquivo

- **`interface_streamlit.py`** - Interface Streamlit

## Como Usar

### 1. Instalar Dependências

```bash
pip install streamlit requests pandas
```

### 2. Rodar a Interface

```bash
cd 04_Interface
streamlit run interface_streamlit.py
```

**Esperado:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### 3. Acessar

Abra no navegador: **http://localhost:8501**

## Pré-requisitos

- ✅ API FastAPI deve estar rodando em http://localhost:8000
- ✅ Streamlit instalado
- ✅ Requests e Pandas instalados

## Estrutura da Interface

### 🏥 Cabeçalho
- Título principal
- Breve descrição do sistema

### 📋 Barra Lateral

**Status da API:**
- ✅ Conectada / ❌ Desconectada

**Informações do Modelo:**
- Nome do modelo
- Acurácia
- F1-Score
- Validação Cruzada

**Valores de Referência:**
- Tabela com valores normais/alerta/crítico para:
  - Glicose
  - Pressão Arterial
  - IMC
  - Colesterol

### 📝 Formulário Principal

**Campos de Input:**

| Campo | Tipo | Range | Unidade |
|-------|------|-------|---------|
| Nome | Text | - | - |
| Idade | Número | 18-120 | anos |
| Glicose | Número | 60-350 | mg/dL |
| Pressão | Número | 80-220 | mmHg |
| IMC | Número | 15-55 | kg/m² |
| Colesterol | Número | 100-400 | mg/dL |

### 🎯 Indicadores Rápidos

- Mostra status de cada medida enquanto o usuário digita:
  - ✅ Verde = Normal
  - ⚠️ Laranja = Alerta
  - ❌ Vermelho = Crítico

### 🔍 Botão de Diagnóstico

- Faz a requisição POST para `/predict` da API
- Valida se o nome foi preenchido
- Mostra spinner enquanto processa

### 📊 Resultado do Diagnóstico

Após processar, exibe:

**1. Caixa de Resultado Destacada:**
```
✅ Risco Baixo
Paciente: João Silva (45 anos)
```

**2. Probabilidades por Classe:**
- Risco Baixo: X%
- Risco Médio: Y%
- Risco Alto: Z%

**3. Explicação:**
- Texto legível em português explicando os fatores de risco encontrados

**4. Dados Brutos (JSON):**
- Mostra a resposta completa da API

**5. Download:**
- Botão para baixar o resultado em JSON

## Exemplo de Fluxo

1. Usuário preenche os campos do formulário
2. Indicadores rápidos mostram status de cada valor
3. Usuário clica em "🔍 Fazer Diagnóstico"
4. Interface envia requisição para a API
5. Resultado é exibido em caixa colorida
6. Usuário pode ver probabilidades e explicação
7. Usuário pode baixar o resultado em JSON

## Tratamento de Erros

A interface trata automaticamente:

- ❌ API não conecta → mensagem de erro
- ❌ Timeout → mensagem de erro
- ❌ Campos vazios → validação local
- ❌ Valores fora do intervalo → erro 422 da API

## Session State

Streamlit mantém em memória:

- `ultimo_resultado`: Resultado do último diagnóstico
- `timestamp`: Hora do último diagnóstico

Isso permite que o usuário veja o resultado mesmo se recarregar a página.

## Customizações Possíveis

Você pode customizar:

- **Cores:** Modificar `cores_risco` para RGB customizado
- **Temas:** Usar `st.set_page_config(theme="dark")`
- **Layout:** Reorganizar colunas e espaçamento
- **Campos:** Adicionar/remover campos do formulário

## Próximo Passo

Após a interface estar rodando:

1. ✅ Você tem um sistema completo funcionando
2. ➡️ Vá para **08_Documentacao** para instruções finais
3. ➡️ Execute **09_Scripts_Uteis** para facilitar o uso

---

**Status:** ✅ Pronto para usar  
**Data:** 27/04/2026  
**Porta:** 8501  
**Requer:** API rodando em :8000
