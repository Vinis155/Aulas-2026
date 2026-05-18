# 🤖 ESPECIFICAÇÃO DO BOT DE DIAGNÓSTICO CLÍNICO
**Documento de Definição: Persona, Funcionalidades e Fluxo Conversacional**

---

## 📌 ÍNDICE
1. [Definição da Persona e Tom de Voz](#1-definição-da-persona-e-tom-de-voz)
2. [Requisitos Funcionais](#2-requisitos-funcionais)
3. [Design do Fluxo Conversacional](#3-design-do-fluxo-conversacional)
4. [Tratamento de Erros e Exceções](#4-tratamento-de-erros-e-exceções)

---

## 1. DEFINIÇÃO DA PERSONA E TOM DE VOZ

### 1.1 Nome do Bot
**Assistente:** `ClinicoIA` ou `Dr. Diagnóstico`

**Identificação no Sistema:**
- Nome exibido: "🏥 ClinicoIA"
- Status: "Assistente de Triagem Inteligente"
- Disponibilidade: 24/7

---

### 1.2 Personalidade
O assistente é um **profissional de triagem médica ágil, empático, mas rigoroso**:

| Aspecto | Descrição |
|---------|-----------|
| **Nível de Formalidade** | Profissional, mas não extremamente formal. Usar "você" (linguagem natural). |
| **Empatia** | Alto — reconhece preocupações do paciente, nunca é mecanicista. |
| **Urgência** | Identifica perigos imediatos; recomenda encaminhamento para ER se necessário. |
| **Conhecimento** | Referencia dados clínicos reais; explica lógica das avaliações. |
| **Função** | **NÃO é médico, é um triador inteligente.** Recomenda, não diagnostica. |

**Slogans/Posicionamento:**
- ✓ "Aqui para ajudar você a entender seu risco"
- ✓ "Seus dados, nossa análise, sua saúde"
- ✓ "Triagem inteligente. Ação rápida. Saúde em foco."

---

### 1.3 Exemplo de Saudação
**Primeira mensagem do bot ao usuário:**

```
👋 Olá! Bem-vindo ao ClinicoIA.

Eu sou um assistente de triagem de risco clínico. Minha função é ajudá-lo 
a entender melhor seus indicadores de saúde e avaliar o nível de risco 
que você apresenta em relação a doenças crônicas.

⚠️ IMPORTANTE: Não sou um médico. Minhas análises são complementares e 
não substituem uma consulta profissional. Se você sentir qualquer mal-estar 
grave, procure atendimento de emergência imediatamente.

Vamos começar? Pode me contar:
1️⃣  Qual é o seu nome?
2️⃣  Qual é a sua idade?
```

**Variação 2 (mais breve para usuários já familiarizados):**

```
🏥 Bem-vindo de volta! 

Pronto para uma nova avaliação de risco clínico? 
Ou você prefere revisar seus resultados anteriores?

[Iniciar Avaliação] [Ver Histórico] [Ajuda]
```

---

### 1.4 Características Verbais

| Situação | Tom | Exemplo |
|----------|-----|---------|
| **Saudação** | Caloroso, profissional | "Olá! Vou ajudá-lo a..." |
| **Pedido de dados** | Claro, incentivador | "Precisamos de alguns dados biomédicos. Relaxe, é rápido!" |
| **Diagnóstico Baixo Risco** | Positivo, motivador | "Parabéns! Seus indicadores estão em dia. Continue assim!" |
| **Diagnóstico Alto Risco** | Urgente, empático | "Detectei sinais importantes. Recomendo consultar um profissional **logo**." |
| **Erro/Incompreensão** | Paciente, didático | "Desculpe, não entendi. Pode reformular? Por ex: 'Meu IMC é 28.5'" |

---

## 2. REQUISITOS FUNCIONAIS

### 2.1 Função Principal #1: Triagem de Emergência
**O que faz:** Identifica sintomas graves em tempo real via análise de palavras-chave (Regex).

**Palavras-chave monitoradas (Regex):**
```regex
dor\s+(no\s+)?peito|angina|infarto|
falta\s+de\s+ar|dispneia|sufoco|
desmaio|desmaiu|perda\s+de\s+consciência|
convulsão|crise\s+epiléptica|
hemorragia|sangramento\s+(grave|profuso|descontrolado)|
pressão\s+extremamente\s+alta|PAS\s+>\s*200|
glicose\s+crítica|hipoglicemia\s+grave
```

**Ação Automática:**
```
SE (paciente descreve sintoma grave) ENTÃO:
  ✅ DISPARAR ALERTA
  ✅ Mensagem: "⚠️ EMERGÊNCIA DETECTADA!"
  ✅ Sugerir: Chamar 192 (SAMU) imediatamente
  ✅ Pausar coleta de dados
  ✅ Registrar incidente no banco com timestamp
```

**Implementação Sugerida:**
```python
import re

SINTOMAS_GRAVES = r"(dor\s+(no\s+)?peito|falta\s+de\s+ar|desmaio|hemorragia)"

def verificar_emergencia(mensagem: str) -> bool:
    return bool(re.search(SINTOMAS_GRAVES, mensagem.lower()))

if verificar_emergencia(input_usuario):
    disparar_alerta_emergencia()
```

---

### 2.2 Função Principal #2: Consulta de Valores (Baseline Clínico)
**O que faz:** Valida se um valor de indicador biomédico é perigoso comparando com faixas clínicas.

**Tabela de Referência (Faixas Saudáveis vs. Perigosas):**

| Indicador | Saudável | Alerta | Crítico | Fonte |
|-----------|----------|--------|---------|--------|
| **Glicose (mg/dL)** | 70–100 | 100–125 | >126 ou <60 | OMS |
| **Pressão (mmHg)** | <120 | 120–139 | ≥140 | ACC/AHA |
| **IMC (kg/m²)** | 18.5–24.9 | 25–29.9 | ≥30 | WHO |
| **Colesterol (mg/dL)** | <200 | 200–239 | ≥240 | ATP III |
| **Idade** | 18–59 | 60–74 | ≥75 | Risco |

**Fluxo da Função:**
```
Usuário: "Minha glicose é 180"
  ↓ (Parse de número)
  ↓ (Comparação com tabela)
  ↓ Mensagem: "Glicose: 180 mg/dL = ⚠️ ALERTA (acima de 125)"
  ↓ (Sugestão: "Isso indica possível pré-diabetes. Recomendo
                 consultar um endocrinologista.")
```

**Query SQL (Banco clinica.db):**
```sql
SELECT nome, glicose, pressao, imc, colesterol, risco_classificacao
FROM analises
WHERE paciente_id = ? AND data_analise >= DATE('now', '-30 days')
ORDER BY data_analise DESC
LIMIT 5;
```

**Implementação Sugerida:**
```python
def avaliar_indicador(tipo: str, valor: float) -> dict:
    """
    Retorna: {'status': 'SAUDÁVEL'|'ALERTA'|'CRÍTICO', 
              'explicacao': str}
    """
    referencias = {
        'glicose': {'saudavel': (70, 100), 'alerta': (100, 125), 'critico': (0, 60) | (126, 350)},
        'pressao': {'saudavel': (80, 119), 'alerta': (120, 139), 'critico': (0, 79) | (140, 300)},
        'imc': {'saudavel': (18.5, 24.9), 'alerta': (25, 29.9), 'critico': (0, 18.4) | (30, 100)},
    }
    # ... validação lógica
```

---

### 2.3 Função Principal #3: Coleta Inteligente para IA
**O que faz:** Solicita dados necessários para o modelo Random Forest de forma conversacional e validada.

**Dados Coletados:**
| Campo | Tipo | Exemplo | Validação |
|-------|------|---------|-----------|
| **Nome** | String | "João Silva" | Len > 2, sem números |
| **Idade** | Int | 45 | 18 ≤ idade ≤ 120 |
| **Glicose** | Float | 148.5 | 60 ≤ glicose ≤ 350 |
| **Pressão** | Float | 155.0 | 80 ≤ pressão ≤ 220 |
| **IMC** | Float | 31.5 | 15 ≤ IMC ≤ 55 |
| **Colesterol** | Float | 248.0 | 100 ≤ colesterol ≤ 400 |

**Fluxo de Coleta (Conversacional):**
```
Bot: "Perfeito, vamos coletar suas informações. Comece fácil — qual é o seu nome?"
Usuário: "João"
Bot: "Prazer, João! 👋 Quantos anos você tem?"
Usuário: "45"
Bot: "Ótimo! Agora vou precisar de seus indicadores de saúde. 
      Qual é a sua glicose (em mg/dL)? Se não souber, podemos pular."
Usuário: "148"
Bot: "Registrado! Glicose: 148 mg/dL → ⚠️ Pré-diabetes"
...
```

**Validação em Tempo Real:**
```python
def validar_entrada(campo: str, valor: str) -> Tuple[bool, str]:
    """Retorna (é_valido, mensagem)"""
    validacoes = {
        'nome': lambda x: len(x) > 2 and not any(c.isdigit() for c in x),
        'idade': lambda x: x.isdigit() and 18 <= int(x) <= 120,
        'glicose': lambda x: 60 <= float(x) <= 350,
        # ...
    }
    # Lógica de validação com feedback
```

---

## 3. DESIGN DO FLUXO CONVERSACIONAL

### 3.1 Caminho Feliz (Happy Path) - Fluxo Normal

```
┌─────────────────────────────────────────────────────────────────┐
│ INÍCIO: Usuário acessa a interface                              │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
        ┌──────────────────────────────────────────┐
        │ 1️⃣  SAUDAÇÃO DO BOT                      │
        │ "Olá! Bem-vindo ao ClinicoIA..."         │
        │ [Iniciar Avaliação] [Ver Histórico]      │
        └──────────────┬───────────────────────────┘
                       │
             ┌─────────▼──────────┐
             │  VERIFICAR EMERGÊNCIA?
             │  (Regex de sintomas graves)
             └────┬──────────────┬┘
          NÃO │    │             │ SIM
             │    │             │
       ┌─────▼────┴─┐     ┌─────▼──────────────────┐
       │ Continuar │     │ ⚠️  DISPARAR ALERTA    │
       │ fluxo     │     │ "Emergência Detectada" │
       │ normal    │     │ Chamar 192 (SAMU)      │
       └────┬──────┘     │ [FIM DO FLUXO]         │
            │            └────────────────────────┘
            │
            ▼
   ┌─────────────────────────────────────────────────┐
   │ 2️⃣  COLETA DE DADOS BIOMÉDICOS                 │
   │ (Conversação interativa)                        │
   │                                                  │
   │ "Qual é o seu nome?"      ← usuário digita     │
   │ "Quantos anos você tem?"  ← usuário digita     │
   │ "Qual é a sua glicose?"   ← usuário digita     │
   │ "Sua pressão arterial?"   ← usuário digita     │
   │ "Qual é seu IMC?"         ← usuário digita     │
   │ "Colesterol total?"       ← usuário digita     │
   │                                                  │
   │ ✅ Validação em tempo real para cada entrada   │
   └────────┬────────────────────────────────────────┘
            │
            ▼
    ┌──────────────────────────────────────────────┐
    │ 3️⃣  ANÁLISE DE URGÊNCIA DO BOT              │
    │ (Verificar valores contra baseline clínico) │
    │                                              │
    │ Glicose 148 → ⚠️ Alerta (pré-diabetes)     │
    │ Pressão 155 → ⚠️ Alerta (hipertensão 2)    │
    │ IMC 31.5 → ⚠️ Alerta (obesidade)           │
    │ Colesterol 248 → ⚠️ Alerta (elevado)       │
    └────────┬─────────────────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────────────────┐
    │ 4️⃣  SOLICITAÇÃO DE INDICADORES              │
    │ (dados coletados com sucesso)                │
    │                                              │
    │ "Seus dados foram registrados!"             │
    │ "Vou analisar agora com meu modelo de IA..." │
    │ ⏳ [Processando...]                          │
    └────────┬─────────────────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────────────────────┐
    │ 5️⃣  PREDIÇÃO COM MODELO DE IA (Random Forest)  │
    │ (Chamar modelo_saude.pkl)                       │
    │                                                  │
    │ Entrada: [idade, glicose, pressão, IMC, ...]  │
    │ Saída: [risco_baixo, risco_médio, risco_alto] │
    │                                                  │
    │ Decisão: Max(probas) = risco_alto (95%)        │
    └────────┬──────────────────────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────────────────┐
    │ 6️⃣  ENTREGA DO DIAGNÓSTICO                  │
    │ (Resultado com explicação clara)             │
    │                                              │
    │ 🔴 RISCO: ALTO (95%)                        │
    │                                              │
    │ Indicadores que elevam seu risco:           │
    │   • Glicose elevada (148 mg/dL)             │
    │   • Hipertensão (155 mmHg)                  │
    │   • Sobrepeso/Obesidade (IMC 31.5)          │
    │   • Colesterol elevado (248 mg/dL)          │
    │                                              │
    │ 📋 RECOMENDAÇÕES:                            │
    │   1. Agende consulta com endocrinologista   │
    │   2. Reduza sódio e açúcares                │
    │   3. Aumente atividade física (30 min/dia)  │
    │   4. Monitore glicose semanalmente          │
    │   5. Faça novo teste em 30 dias             │
    │                                              │
    │ ℹ️  Este é um resultado orientativo.         │
    │    Consulte seu médico para diagnóstico     │
    │    definitivo.                              │
    └────────┬──────────────────────────────────────┘
             │
             ▼
    ┌──────────────────────────────────────────────┐
    │ 7️⃣  ENCERRAMENTO                            │
    │ (Salvar no banco de dados)                   │
    │                                              │
    │ ✅ Análise salva com sucesso!               │
    │                                              │
    │ [Nova Avaliação] [Ver Histórico] [Sair]    │
    └──────────────────────────────────────────────┘
```

---

### 3.2 Detalhamento Textual do Fluxo

#### **FASE 1: Saudação e Identificação**
```
Bot: 👋 Olá! Bem-vindo ao ClinicoIA.
     Sou um assistente de triagem de risco clínico inteligente.

Usuário: [clica em "Iniciar Avaliação"]

Bot: Vamos começar? Pode me contar seu nome?
Usuário: João Silva

Bot: Prazer, João! 👋 Quantos anos você tem?
Usuário: 45
```

---

#### **FASE 2: Relato do Sintoma (Opcional)**
```
Bot: Antes de coletarmos seus dados, você está sentindo 
     algum sintoma agora? (Ex: dor, cansaço, etc.)
     Pode deixar em branco se preferir.

Usuário: Tenho sentido cansaço
```

---

#### **FASE 3: Análise de Urgência pelo Bot**
```
Bot: [Verifica com Regex se "cansaço" é symptoma grave]
     ✅ Cansaço não é emergência.
     
Bot: Entendo. Vamos coletar seus indicadores para 
     entender melhor. Qual é a sua glicose (em mg/dL)?
     Se não souber, podemos estimar.

Usuário: 148
```

---

#### **FASE 4: Solicitação de Indicadores**
```
Bot: ✅ Glicose 148 mg/dL registrada
     ℹ️  Isso está acima do normal (ref: <100)

Bot: Agora sua pressão arterial (em mmHg)?
Usuário: 155

Bot: ✅ Pressão 155 mmHg registrada
     ⚠️  Você está em pré-hipertensão estágio 2

Bot: Qual é seu IMC (kg/m²)? Ou me diz altura e peso?
Usuário: 31.5

Bot: ✅ IMC 31.5 registrado
     ⚠️  Indicador de obesidade

Bot: Colesterol total (em mg/dL)?
Usuário: 248

Bot: ✅ Colesterol 248 mg/dL registrado
     ⚠️  Elevado (referência: <200)
```

---

#### **FASE 5: Predição com IA**
```
Bot: Perfeito! Tenho todos os seus dados.
     🔄 Analisando com meu modelo de IA...
     
[Envia para modelo Random Forest]
Input: [45, 148, 155, 31.5, 248]
Output: risco_classificacao = "Alto", prob = 0.95

Bot: ✅ Análise concluída!
```

---

#### **FASE 6: Entrega do Diagnóstico**
```
╔════════════════════════════════════════════════════════╗
║ 📊 RESULTADO DA AVALIAÇÃO DE RISCO CLÍNICO           ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║ Paciente: João Silva | Idade: 45 anos                ║
║ Data: 11/05/2026 | Hora: 14:32                       ║
║                                                        ║
║ 🔴 NÍVEL DE RISCO: ALTO                             ║
║    Probabilidade: 95%                                ║
║                                                        ║
╠════════════════════════════════════════════════════════╣
║ ⚠️  INDICADORES ALARMANTES:                          ║
║                                                        ║
║  • Glicose: 148 mg/dL (Limite: 100)    [CRÍTICO]    ║
║  • Pressão: 155 mmHg (Limite: 139)    [ALERTA]     ║
║  • IMC: 31.5 kg/m² (Limite: 29.9)     [ALERTA]     ║
║  • Colesterol: 248 mg/dL (Limite: 200) [ALERTA]    ║
║                                                        ║
╠════════════════════════════════════════════════════════╣
║ 📋 RECOMENDAÇÕES IMEDIATAS:                           ║
║                                                        ║
║  1. 👨‍⚕️  Consulte um ENDOCRINOLOGISTA nos próximos   ║
║      15 dias para avaliação de diabetes              ║
║                                                        ║
║  2. 🏃 Aumente atividade física: 30 min/dia de      ║
║      caminhada ou exercício moderado                 ║
║                                                        ║
║  3. 🥗 Mude hábitos alimentares:                      ║
║      - Reduza sódio (sal)                            ║
║      - Diminua açúcares refinados                    ║
║      - Aumente fibras (frutas, vegetais)             ║
║      - Limite gorduras saturadas                     ║
║                                                        ║
║  4. 📊 Monitore regularmente:                         ║
║      - Glicose: 1x por semana                        ║
║      - Pressão: 1x por semana                        ║
║      - Peso: 1x por semana                           ║
║                                                        ║
║  5. 🔄 Próxima avaliação: 30 dias (junho/2026)      ║
║                                                        ║
╠════════════════════════════════════════════════════════╣
║ ℹ️  AVISO IMPORTANTE:                                  ║
║                                                        ║
║  Este resultado é ORIENTATIVO apenas.                ║
║  NÃO substitui diagnóstico profissional.             ║
║  Consulte seu médico para confirmação.               ║
║                                                        ║
║  Seus dados foram salvos com segurança no banco.     ║
║                                                        ║
╚════════════════════════════════════════════════════════╝

Bot: Gostaria de repetir a avaliação? Ou precisa de ajuda?
     [Nova Avaliação] [Ver Histórico] [Sair]
```

---

### 3.3 Variações do Fluxo

#### **Variação A: Usuário Recusa Informação**
```
Bot: Qual é a sua glicose?
Usuário: Prefiro não dizer

Bot: Sem problema! Pode deixar em branco. 
     No entanto, sem a glicose, minha análise fica menos precisa.
     Tem certeza? (Y/N)

Usuário: Sim, quero pular
Bot: Tudo bem. Vou estimar baseado nos outros dados.
     [Continua com valores padrão ou aviso de incompletude]
```

---

#### **Variação B: Valor Fora do Intervalo**
```
Bot: Qual é sua idade?
Usuário: 250

Bot: ❌ Desculpe, 250 anos é impossível! 😅
     Pode ser um erro de digitação? 
     Confirme sua idade (18 a 120 anos):

Usuário: 45
Bot: ✅ Perfeito! 45 anos.
```

---

#### **Variação C: Entrada Não Compreendida**
```
Bot: Qual é a sua glicose em mg/dL?
Usuário: não sei

Bot: Sem problema! Se você não souber o valor exato, 
     você tem algumas opções:
     
     📌 Estimar (baixa/normal/elevada)
     📌 Deixar em branco (usaremos valor padrão)
     📌 Digitar um valor que você lembra
     
     O que prefere?

Usuário: Posso estimar?
Bot: Claro! Você diria que sua glicose é:
     [Baixa (<100)] [Normal (100-125)] [Elevada (>125)]
```

---

## 4. TRATAMENTO DE ERROS E EXCEÇÕES

### 4.1 Cenários de Erro e Ações Correspondentes

#### **Erro 1: Usuário Digita Algo Incompreensível**

**Cenário:**
```
Bot: Qual é a sua idade?
Usuário: xyz123@#$
```

**Resposta do Bot:**
```
❌ Desculpe, não consegui entender "xyz123@#$".

Pode reformular? Preciso de um número (exemplo: "25" ou "45 anos").

Sua idade:
```

**Implementação:**
```python
def validar_numero(entrada: str, min_val: int, max_val: int) -> Tuple[bool, Optional[float]]:
    try:
        valor = float(entrada.replace(',', '.'))
        if min_val <= valor <= max_val:
            return True, valor
        else:
            return False, None
    except ValueError:
        return False, None

valor_valido, valor_numerico = validar_numero(user_input, 18, 120)
if not valor_valido:
    print("Entrada inválida. Tente novamente.")
```

---

#### **Erro 2: Usuário Recusa Passar um Dado**

**Cenário:**
```
Bot: Qual é a sua pressão arterial?
Usuário: Não vou contar isso.
```

**Resposta do Bot:**
```
Tudo bem! Respeitamos sua privacidade. 

⚠️  Sem a pressão, minha análise será menos precisa. 
Mas posso continuar com os outros dados.

Gostaria de:
[1] Mudar de ideia e informar
[2] Continuar sem pressão (resultado com asterisco*)
[3] Encerrar avaliação

Escolha (1/2/3):
```

**Implementação:**
```python
CAMPOS_OBRIGATORIOS = ['nome', 'idade', 'glicose']
CAMPOS_OPCIONAIS = ['pressao', 'imc', 'colesterol']

def validar_campos(dados: dict) -> Tuple[bool, str]:
    faltantes = [f for f in CAMPOS_OBRIGATORIOS if not dados.get(f)]
    if faltantes:
        return False, f"Campos obrigatórios faltando: {faltantes}"
    return True, "Todos os campos necessários foram preenchidos"
```

---

#### **Erro 3: Modelo de IA Retorna Erro**

**Cenário:**
```
Bot: [Tentando carregar modelo_saude.pkl]
❌ ERRO: FileNotFoundError: modelo não encontrado
```

**Resposta do Bot (Frente ao Usuário):**
```
Desculpe 😟 Estou enfrentando uma dificuldade técnica.

Meu modelo de IA não está disponível no momento.

Opções:
[A] Tentar novamente em 30 segundos
[B] Salvar seus dados para análise posterior
[C] Chamar suporte técnico

O que você prefere?
```

**Implementação:**
```python
def carregar_modelo():
    try:
        modelo = joblib.load(MODELO_PATH)
        scaler = joblib.load(SCALER_PATH)
        return modelo, scaler
    except FileNotFoundError as e:
        logger.error(f"Modelo não encontrado: {e}")
        return None, None
    except Exception as e:
        logger.error(f"Erro ao carregar modelo: {e}")
        return None, None

modelo, scaler = carregar_modelo()
if modelo is None:
    exibir_mensagem_erro("Modelo indisponível")
    salvar_dados_temporarios()
    return
```

---

#### **Erro 4: Banco de Dados Indisponível**

**Cenário:**
```
Bot: [Tentando salvar análise no banco]
❌ ERRO: sqlite3.DatabaseError: database locked
```

**Resposta do Bot:**
```
⚠️  Não consegui salvar seus dados no banco de dados.

Isso pode ocorrer por:
  • Outro usuário editando os dados
  • Conexão perdida

Tentando novamente...
[Retry 1/3]

[Aguarde 5 segundos]
✅ Sucesso! Dados salvos.
```

**Implementação (com retry):**
```python
import time
from sqlite3 import DatabaseError

def salvar_com_retry(conn, query, params, max_retries=3):
    for tentativa in range(max_retries):
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return True
        except DatabaseError as e:
            if tentativa < max_retries - 1:
                logger.warning(f"Retry {tentativa + 1}/{max_retries}. Erro: {e}")
                time.sleep(1)
            else:
                logger.error(f"Falha permanente após {max_retries} tentativas")
                return False
```

---

#### **Erro 5: Valores Muito Extremos (Outliers)**

**Cenário:**
```
Bot: Qual é a sua glicose?
Usuário: 1000

[Validação detecta: glicose > 350 (fora do intervalo permitido)]
```

**Resposta do Bot:**
```
⚠️  Glicose de 1000 mg/dL está EXTREMAMENTE elevada.

Isso pode indicar:
  • Erro de digitação (exemplo: digitou "100" como "1000")
  • Situação médica crítica

Você está sentindo-se bem agora?
[SIM] [NÃO - Preciso de emergência]

Se escolher NÃO:
  → Chamar 192 (SAMU) imediatamente!

Digite novamente a glicose:
```

---

#### **Erro 6: Timeout do Modelo (IA demora > 5 segundos)**

**Cenário:**
```
[Enviando dados para Random Forest]
[5 segundos se passam sem resposta]
```

**Resposta do Bot:**
```
⏳ A análise está demorando mais do que o esperado...

Causas possíveis:
  • Servidor ocupado
  • Lentidão de rede

[Aguarde mais um pouco...]
[Opção: Cancelar]

[Processando...] ████████░░ 80%

✅ Análise concluída!
```

**Implementação (com timeout):**
```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def prever_com_timeout(dados, timeout_segundos=5):
    with ThreadPoolExecutor() as executor:
        future = executor.submit(modelo.predict_proba, dados)
        try:
            resultado = future.result(timeout=timeout_segundos)
            return resultado
        except TimeoutError:
            logger.error("Timeout ao executar modelo")
            return None
```

---

#### **Erro 7: Conflito de Sessão / Usuário Desconectado**

**Cenário:**
```
[Usuário preenche dados]
[Conexão cai]
[Tenta salvar]
```

**Resposta do Bot:**
```
⚠️  Sua sessão expirou.

Seus dados foram salvos como RASCUNHO.

Você pode:
[1] Fazer login novamente e continuar
[2] Descartar rascunho e começar novo

O que prefere?
```

---

### 4.2 Matriz de Tratamento de Erros

| Tipo de Erro | Detectado Por | Ação | Mensagem ao Usuário |
|--------------|---------------|------|---------------------|
| **Entrada Inválida** | Regex + Try/Except | Pedir re-entrada | "Desculpe, não entendi. Pode reformular?" |
| **Campo Vazio** | Validador | Marcar como opcional | "Campo deixado em branco. Usando valor padrão." |
| **Valor Fora do Intervalo** | Condicional (if min ≤ x ≤ max) | Alertar e pedir novo | "Valor impossível! Tente novamente." |
| **Modelo Não Encontrado** | FileNotFoundError | Registrar e pausar | "Modelo indisponível. Tentando novamente..." |
| **Banco de Dados Offline** | DatabaseError | Retry c/ backoff | "Salvando seus dados..." |
| **Timeout de Processamento** | Timer > 5s | Cancelar e notificar | "Análise demorou. Tente novamente." |
| **Sintoma de Emergência** | Regex | Disparar alerta | "⚠️  EMERGÊNCIA! Chamar 192." |
| **Conexão Perdida** | Socket/Network Error | Reconectar | "Reconectando..." |

---

### 4.3 Fluxo de Recuperação de Erros

```
┌─────────────────────────────────────────────┐
│ ❌ ERRO DETECTADO                           │
└────────────────┬────────────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────────────┐
    │ Classificar Severidade                 │
    │ BAIXA / MÉDIA / ALTA / CRÍTICA         │
    └────┬──────────────────┬──────────────┬─┘
      BAIXA│              MÉDIA│         CRÍTICA│
          │                │            │
          ▼                ▼            ▼
    ┌──────────┐    ┌──────────┐  ┌─────────────┐
    │ Retry    │    │ Alertar  │  │ Parar + SOS │
    │ automático│   │ Usuário  │  │ Chamar 192  │
    │ 1-3x    │    │ + Retry  │  │             │
    └────┬─────┘    └────┬─────┘  └─────────────┘
         │               │
         ▼               ▼
    ┌──────────────────────────────────────────┐
    │ ✅ SUCESSO?                              │
    │ SIM → Continuar fluxo                    │
    │ NÃO → Registrar log + Notificar admin    │
    └──────────────────────────────────────────┘
```

---

## 🔍 RESUMO DE FUNCIONALIDADES

| # | Funcionalidade | Ativação | Saída |
|---|---|---|---|
| 1️⃣ | **Triagem de Emergência** | Regex de sintomas graves | Alerta imediato + recomendação SAMU |
| 2️⃣ | **Consulta de Valores** | Usuário digita indicador | Comparação vs. baseline clínico |
| 3️⃣ | **Coleta para IA** | Formulário conversacional | Dados validados prontos p/ modelo |
| 4️⃣ | **Predição de Risco** | Chamar modelo .pkl | Classificação (Baixo/Médio/Alto) + prob% |
| 5️⃣ | **Tratamento de Erros** | Exceções capturadas | Mensagem amigável + retry automático |

---

## 📝 PRÓXIMOS PASSOS

1. ✅ Refinar prompts conversacionais (tom mais natural)
2. ✅ Adicionar imagens/ícones nos resultados
3. ✅ Integrar chatbot em chatGPT / Telegram / WhatsApp
4. ✅ Adicionar histórico de conversas por paciente
5. ✅ Implementar feedback: "Essa resposta foi útil?"
6. ✅ Validar cumprimento de LGPD (proteção de dados)

---

**Versão:** 1.0  
**Última Atualização:** 11/05/2026  
**Responsável:** Equipo Bug Busters  
**Status:** ✅ Pronto para Implementação
