"""
=============================================================================
BLOCO 2 — PIPELINE COMPLETO DE MACHINE LEARNING
=============================================================================
Projeto  : Sistema de Previsao de Risco Clinico
Arquivo  : 2_pipeline_ml.py
Entrada  : pacientes.csv
Saidas   : graficos_comparacao.png | matriz_confusao.png | curva_roc.png

Etapas executadas:
    1.  Leitura e inspecao do dataset
    2.  Separacao features (X) e target (y)
    3.  Divisao treino / teste  (80% / 20%)
    4.  Normalizacao com StandardScaler
    5.  Treinamento de 3 modelos:
            a) Regressao Logistica
            b) Random Forest
            c) KNN
    6.  Avaliacao: acuracia, precision, recall, F1-score
    7.  Validacao cruzada k-fold (k=5)
    8.  Comparacao dos modelos e selecao do melhor
    9.  Visualizacoes:
            - Grafico de barras comparando acuracias
            - Matriz de confusao do melhor modelo
            - Curva ROC multiclasse (OvR)
   10.  Predicao para um novo paciente ficticio
=============================================================================
"""

# ── IMPORTACOES ───────────────────────────────────────────────────────────────
import numpy  as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")           # renderiza sem abrir janela (salva em arquivo)
import matplotlib.pyplot as plt

from sklearn.model_selection  import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing    import StandardScaler, label_binarize
from sklearn.linear_model     import LogisticRegression
from sklearn.ensemble         import RandomForestClassifier
from sklearn.neighbors        import KNeighborsClassifier
from sklearn.metrics          import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, ConfusionMatrixDisplay,
    roc_curve, auc
)

# Estilo global dos graficos
plt.rcParams.update({
    "figure.facecolor" : "white",
    "axes.facecolor"   : "#f4f6f9",
    "axes.grid"        : True,
    "grid.alpha"       : 0.4,
    "font.size"        : 10,
    "axes.spines.top"  : False,
    "axes.spines.right": False,
})

# Paleta de cores por modelo
CORES = {
    "Regressao Logistica": "#4C72B0",
    "Random Forest"      : "#2ca02c",
    "KNN"                : "#d62728",
}

LABELS_RISCO = ["Baixo (0)", "Medio (1)", "Alto (2)"]

print("=" * 62)
print("  SISTEMA DE PREVISAO DE RISCO CLINICO — PIPELINE ML")
print("=" * 62)


# ════════════════════════════════════════════════════════════════
# ETAPA 1 — LEITURA E INSPECAO DO DATASET
# ════════════════════════════════════════════════════════════════
print("\n[ETAPA 1] Lendo 'pacientes.csv'...")

df = pd.read_csv("pacientes.csv")

print(f"  Shape            : {df.shape}  (linhas x colunas)")
print(f"  Colunas          : {list(df.columns)}")
print(f"  Valores ausentes : {df.isnull().sum().sum()} (total)")
print(f"\n  Distribuicao do target 'risco':")
for cls, label in zip([0,1,2], ["Baixo","Medio","Alto"]):
    n = (df["risco"] == cls).sum()
    print(f"    {cls} ({label}): {n} registros  ({n/len(df)*100:.1f}%)")


# ════════════════════════════════════════════════════════════════
# ETAPA 2 — SEPARACAO DE FEATURES E TARGET
# ════════════════════════════════════════════════════════════════
print("\n[ETAPA 2] Separando features (X) e target (y)...")

# Features: variaveis de entrada que o modelo usa para aprender
# Target  : variavel que queremos prever (risco)
FEATURES = ["idade", "glicose", "pressao", "imc", "colesterol"]

X = df[FEATURES].values   # numpy array shape (2000, 5)
y = df["risco"].values     # numpy array shape (2000,)

print(f"  Features usadas : {FEATURES}")
print(f"  Shape de X      : {X.shape}")
print(f"  Shape de y      : {y.shape}  — classes: {np.unique(y)}")


# ════════════════════════════════════════════════════════════════
# ETAPA 3 — DIVISAO TREINO / TESTE
# ════════════════════════════════════════════════════════════════
print("\n[ETAPA 3] Dividindo em treino (80%) e teste (20%)...")

# stratify=y: garante proporcao de cada classe em treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size   = 0.20,
    random_state= 42,
    stratify    = y
)

print(f"  Treino : {X_train.shape[0]} amostras")
print(f"  Teste  : {X_test.shape[0]} amostras")


# ════════════════════════════════════════════════════════════════
# ETAPA 4 — NORMALIZACAO DOS DADOS
# ════════════════════════════════════════════════════════════════
print("\n[ETAPA 4] Normalizando com StandardScaler...")
#
# StandardScaler transforma cada feature para media=0 e desvio=1.
# Isso e fundamental para modelos sensiveis a escala (Logistica, KNN).
#
# REGRA IMPORTANTE — evitar data leakage:
#   fit_transform() no TREINO: calcula media/desvio do treino e transforma
#   transform()     no TESTE : aplica os parametros do treino (sem recalcular)

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)   # ajusta e transforma
X_test_sc  = scaler.transform(X_test)        # so transforma

# Exibe media e desvio aprendidos pelo scaler
for i, feat in enumerate(FEATURES):
    print(f"  {feat:12s}  media={scaler.mean_[i]:7.2f}  desvio={scaler.scale_[i]:.2f}")


# ════════════════════════════════════════════════════════════════
# ETAPA 5 — DEFINICAO E TREINAMENTO DOS MODELOS
# ════════════════════════════════════════════════════════════════
print("\n[ETAPA 5] Treinando modelos...")

# ── a) Regressao Logistica ─────────────────────────────────────
# Modelo linear que estima probabilidades de cada classe usando
# a funcao softmax (para multiclasse). Simples, interpretavel,
# bom baseline. max_iter alto para garantir convergencia.
lr = LogisticRegression(
    solver       = "lbfgs",        # otimizador eficiente para multiclasse
    max_iter     = 1000,           # iteracoes maximas
    random_state = 42
)

# ── b) Random Forest ──────────────────────────────────────────
# Conjunto (ensemble) de arvores de decisao treinadas em subconjuntos
# aleatorios dos dados. Robusto, bom com dados nao lineares.
rf = RandomForestClassifier(
    n_estimators = 100,    # numero de arvores
    max_depth    = 10,     # profundidade maxima de cada arvore
    random_state = 42,
    n_jobs       = -1      # usa todos os nucleos do processador
)

# ── c) KNN — K-Nearest Neighbors ──────────────────────────────
# Classifica com base nos K vizinhos mais proximos no espaco de features.
# Nao tem treinamento explicito (lazy learner). Muito sensivel a escala,
# por isso a normalizacao da Etapa 4 e essencial aqui.
knn = KNeighborsClassifier(
    n_neighbors = 7,         # K = 7 vizinhos
    metric      = "euclidean"
)

# Dicionario {nome: instancia} para iterar facilmente
modelos = {
    "Regressao Logistica": lr,
    "Random Forest"      : rf,
    "KNN"                : knn,
}

# Treina cada modelo com os dados normalizados de treino
for nome_modelo, modelo in modelos.items():
    modelo.fit(X_train_sc, y_train)
    print(f"  [OK] {nome_modelo} treinado.")


# ════════════════════════════════════════════════════════════════
# ETAPA 6 — AVALIACAO DAS METRICAS
# ════════════════════════════════════════════════════════════════
print("\n[ETAPA 6] Avaliando metricas no conjunto de teste...\n")

# Dicionario para guardar resultados de cada modelo
resultados = {}

# Cabecalho da tabela de resultados
print(f"  {'Modelo':<22} {'Acuracia':>9} {'Precision':>10} {'Recall':>7} {'F1-Score':>9}")
print("  " + "-" * 62)

for nome_modelo, modelo in modelos.items():
    # Predicao no conjunto de teste
    y_pred = modelo.predict(X_test_sc)

    # Acuracia: percentual de predicoes corretas
    acc = accuracy_score(y_test, y_pred)

    # Precision: dos que o modelo disse "positivo", quantos realmente eram?
    # average="weighted" pondera pela frequencia de cada classe
    pre = precision_score(y_test, y_pred, average="weighted", zero_division=0)

    # Recall: dos que realmente eram positivos, quantos o modelo acertou?
    rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)

    # F1-Score: media harmonica entre precision e recall
    f1  = f1_score(y_test, y_pred, average="weighted", zero_division=0)

    resultados[nome_modelo] = {
        "modelo"   : modelo,
        "y_pred"   : y_pred,
        "acuracia" : acc,
        "precision": pre,
        "recall"   : rec,
        "f1"       : f1,
    }

    print(f"  {nome_modelo:<22} {acc:>9.4f} {pre:>10.4f} {rec:>7.4f} {f1:>9.4f}")

print()


# ════════════════════════════════════════════════════════════════
# ETAPA 7 — VALIDACAO CRUZADA K-FOLD (k=5)
# ════════════════════════════════════════════════════════════════
print("[ETAPA 7] Validacao cruzada (StratifiedKFold, k=5)...\n")

# StratifiedKFold: divide em 5 partes mantendo proporcao das classes
# Isso e mais confiavel do que uma unica divisao treino/teste
kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

print(f"  {'Modelo':<22} {'Media CV':>9} {'Desvio CV':>10}")
print("  " + "-" * 44)

for nome_modelo, modelo in modelos.items():
    scores = cross_val_score(
        modelo, X_train_sc, y_train,
        cv      = kfold,
        scoring = "accuracy",
        n_jobs  = -1
    )
    resultados[nome_modelo]["cv_media"]  = scores.mean()
    resultados[nome_modelo]["cv_desvio"] = scores.std()
    print(f"  {nome_modelo:<22} {scores.mean():>9.4f} {scores.std():>10.4f}")

print()


# ════════════════════════════════════════════════════════════════
# ETAPA 8 — COMPARACAO E SELECAO DO MELHOR MODELO
# ════════════════════════════════════════════════════════════════
print("[ETAPA 8] Comparacao e selecao do melhor modelo...")

# Ordena pelo F1-Score ponderado (criterio principal para dados desbalanceados)
ranking = sorted(resultados.items(), key=lambda x: x[1]["f1"], reverse=True)

melhor_nome   = ranking[0][0]
melhor_dados  = ranking[0][1]
melhor_modelo = melhor_dados["modelo"]

print(f"\n  RANKING (por F1-Score ponderado):")
for pos, (nome_m, dados) in enumerate(ranking, start=1):
    print(f"  {pos}. {nome_m:<22}  F1={dados['f1']:.4f}  Acuracia={dados['acuracia']:.4f}")

print(f"\n  >>> MELHOR MODELO: {melhor_nome} <<<")


# ════════════════════════════════════════════════════════════════
# ETAPA 9 — VISUALIZACOES
# ════════════════════════════════════════════════════════════════
print("\n[ETAPA 9] Gerando visualizacoes...")

nomes_m  = list(resultados.keys())
acuracias = [resultados[n]["acuracia"] for n in nomes_m]
f1scores  = [resultados[n]["f1"]       for n in nomes_m]
cv_medias = [resultados[n]["cv_media"]  for n in nomes_m]
cores_barras = [CORES[n] for n in nomes_m]

# ── FIGURA 1: Comparacao de metricas entre modelos ────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Comparacao de Desempenho dos Modelos", fontsize=14, fontweight="bold", y=1.02)

metricas = {
    "Acuracia (Teste)"   : [resultados[n]["acuracia"]  for n in nomes_m],
    "F1-Score Ponderado" : [resultados[n]["f1"]        for n in nomes_m],
    "Acuracia CV Media"  : [resultados[n]["cv_media"]  for n in nomes_m],
}

for ax, (titulo, valores) in zip(axes, metricas.items()):
    barras = ax.bar(nomes_m, valores, color=cores_barras, edgecolor="white",
                    linewidth=1.2, width=0.55)
    ax.set_title(titulo, fontweight="bold", fontsize=11)
    ax.set_ylim(0, 1.1)
    ax.set_ylabel("Score")
    ax.set_xticks(range(len(nomes_m)))
    ax.set_xticklabels(nomes_m, rotation=15, ha="right", fontsize=9)
    # Anota o valor em cima de cada barra
    for barra, val in zip(barras, valores):
        ax.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.01,
                f"{val:.3f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    # Linha de referencia em 1.0
    ax.axhline(1.0, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)

plt.tight_layout()
plt.savefig("graficos_comparacao.png", dpi=150, bbox_inches="tight")
plt.close()
print("  [OK] 'graficos_comparacao.png' salvo.")

# ── FIGURA 2: Matriz de confusao do melhor modelo ─────────────────────────────
fig, ax = plt.subplots(figsize=(7, 6))

cm = confusion_matrix(y_test, melhor_dados["y_pred"])
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=LABELS_RISCO)
disp.plot(ax=ax, colorbar=True, cmap="Blues")

ax.set_title(
    f"Matriz de Confusao\n{melhor_nome}",
    fontweight="bold", fontsize=12
)
ax.set_xlabel("Classe Predita", fontsize=11)
ax.set_ylabel("Classe Real", fontsize=11)

plt.tight_layout()
plt.savefig("matriz_confusao.png", dpi=150, bbox_inches="tight")
plt.close()
print("  [OK] 'matriz_confusao.png' salvo.")

# ── FIGURA 3: Curva ROC multiclasse (One-vs-Rest) ─────────────────────────────
# Binariza y_test: transforma [0,1,2] em 3 colunas binarias
y_test_bin = label_binarize(y_test, classes=[0, 1, 2])

# Probabilidades previstas pelo melhor modelo para cada classe
y_prob = melhor_modelo.predict_proba(X_test_sc)

fig, ax = plt.subplots(figsize=(8, 6))

cores_roc = ["#1f77b4", "#ff7f0e", "#2ca02c"]
for i, (label, cor) in enumerate(zip(LABELS_RISCO, cores_roc)):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_prob[:, i])
    roc_auc = auc(fpr, tpr)
    ax.plot(fpr, tpr, color=cor, lw=2,
            label=f"Risco {label}  (AUC = {roc_auc:.2f})")

# Linha de referencia: classificador aleatorio
ax.plot([0,1], [0,1], "k--", lw=1.2, label="Aleatorio (AUC = 0.50)")

ax.set_title(f"Curva ROC Multiclasse (OvR)\n{melhor_nome}",
             fontweight="bold", fontsize=12)
ax.set_xlabel("Taxa de Falso Positivo (FPR)", fontsize=11)
ax.set_ylabel("Taxa de Verdadeiro Positivo (TPR)", fontsize=11)
ax.legend(loc="lower right", fontsize=10)
ax.set_xlim([0, 1])
ax.set_ylim([0, 1.05])

plt.tight_layout()
plt.savefig("curva_roc.png", dpi=150, bbox_inches="tight")
plt.close()
print("  [OK] 'curva_roc.png' salvo.")


# ════════════════════════════════════════════════════════════════
# ETAPA 10 — PREDICAO PARA UM NOVO PACIENTE
# ════════════════════════════════════════════════════════════════
print("\n[ETAPA 10] Simulando predicao para um novo paciente...\n")

# Dados de um paciente ficticio inseridos manualmente
# (simula a tela de entrada do sistema descrito no documento tecnico)
novo_paciente = {
    "nome"      : "Fernanda",
    "idade"     : 63,
    "glicose"   : 148.0,   # acima do limiar de diabetes (126)
    "pressao"   : 155.0,   # hipertensao estagio 2 (>= 140)
    "imc"       : 31.5,    # obesidade grau I (>= 30)
    "colesterol": 248.0,   # colesterol alto (>= 240)
}

print("  Dados do novo paciente:")
print(f"  {'Nome':<14}: {novo_paciente['nome']}")
print(f"  {'Idade':<14}: {novo_paciente['idade']} anos")
print(f"  {'Glicose':<14}: {novo_paciente['glicose']} mg/dL")
print(f"  {'Pressao':<14}: {novo_paciente['pressao']} mmHg")
print(f"  {'IMC':<14}: {novo_paciente['imc']} kg/m2")
print(f"  {'Colesterol':<14}: {novo_paciente['colesterol']} mg/dL")

# Monta vetor de features na mesma ordem usada no treino
entrada = np.array([[
    novo_paciente["idade"],
    novo_paciente["glicose"],
    novo_paciente["pressao"],
    novo_paciente["imc"],
    novo_paciente["colesterol"]
]])

# Normaliza com o MESMO scaler ajustado no treino
entrada_sc = scaler.transform(entrada)

# Predicao de classe e probabilidades
classe_predita = melhor_modelo.predict(entrada_sc)[0]
probabilidades = melhor_modelo.predict_proba(entrada_sc)[0]

# Mapeamento de classe para rotulo textual
rotulo_risco = {0: "BAIXO", 1: "MEDIO", 2: "ALTO"}
emoji_risco  = {0: "verde ", 1: "amarelo", 2: "vermelho"}

print()
print("  " + "=" * 44)
print(f"  RESULTADO DA ANALISE — {novo_paciente['nome']}")
print("  " + "=" * 44)
print()
print(f"  Modelo utilizado  : {melhor_nome}")
print(f"  Classe predita    : {classe_predita}  ({rotulo_risco[classe_predita]})")
print()
print("  Probabilidades por classe:")
for i, (label, prob) in enumerate(zip(["Baixo","Medio","Alto"], probabilidades)):
    barra = "#" * int(prob * 40)
    print(f"    Risco {label}: {prob*100:5.1f}%  {barra}")

print()
print(f"  >> CLASSIFICACAO FINAL: RISCO {rotulo_risco[classe_predita]} <<")
print("  " + "=" * 44)
print()
print("Pipeline concluido com sucesso.")
print("Arquivos gerados: graficos_comparacao.png | matriz_confusao.png | curva_roc.png")
