"""
=============================================================================
BLOCO 2 — PIPELINE COMPLETO DE MACHINE LEARNING
=============================================================================
Projeto  : Sistema de Previsao de Risco Clinico
Arquivo  : 2_pipeline_ml.py
Entrada  : ../05_Dados/pacientes.csv
Saidas   : ../07_Graficos/*.png | ../06_Modelos/*.pkl

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
   11.  SALVAR MODELO E SCALER PARA A API
=============================================================================
"""

# ── IMPORTACOES ───────────────────────────────────────────────────────────────
import numpy  as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")           # renderiza sem abrir janela (salva em arquivo)
import matplotlib.pyplot as plt
import joblib                   # para serializar modelo e scaler
import os

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

# ── CRIAR DIRETORIOS SE NAO EXISTIREM ───────────────────────────────────────
output_dir_graficos = os.path.join(os.path.dirname(__file__), "..", "07_Graficos")
output_dir_modelos = os.path.join(os.path.dirname(__file__), "..", "06_Modelos")
os.makedirs(output_dir_graficos, exist_ok=True)
os.makedirs(output_dir_modelos, exist_ok=True)

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

# Caminho relativo para o arquivo
csv_path = os.path.join(os.path.dirname(__file__), "..", "05_Dados", "pacientes.csv")

df = pd.read_csv(csv_path)

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

FEATURES = ["idade", "glicose", "pressao", "imc", "colesterol"]

X = df[FEATURES].values
y = df["risco"].values

print(f"  Features usadas : {FEATURES}")
print(f"  Shape de X      : {X.shape}")
print(f"  Shape de y      : {y.shape}  — classes: {np.unique(y)}")

# ════════════════════════════════════════════════════════════════
# ETAPA 3 — DIVISAO TREINO / TESTE
# ════════════════════════════════════════════════════════════════
print("\n[ETAPA 3] Dividindo em treino (80%) e teste (20%)...")

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

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

for i, feat in enumerate(FEATURES):
    print(f"  {feat:12s}  media={scaler.mean_[i]:7.2f}  desvio={scaler.scale_[i]:.2f}")

# ════════════════════════════════════════════════════════════════
# ETAPA 5 — DEFINICAO E TREINAMENTO DOS MODELOS
# ════════════════════════════════════════════════════════════════
print("\n[ETAPA 5] Treinando modelos...")

lr = LogisticRegression(solver="lbfgs", max_iter=1000, random_state=42)
rf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
knn = KNeighborsClassifier(n_neighbors=7, metric="euclidean")

modelos = {
    "Regressao Logistica": lr,
    "Random Forest"      : rf,
    "KNN"                : knn,
}

for nome_modelo, modelo in modelos.items():
    modelo.fit(X_train_sc, y_train)
    print(f"  [OK] {nome_modelo} treinado.")

# ════════════════════════════════════════════════════════════════
# ETAPA 6 — AVALIACAO DAS METRICAS
# ════════════════════════════════════════════════════════════════
print("\n[ETAPA 6] Avaliando metricas no conjunto de teste...\n")

resultados = {}

print(f"  {'Modelo':<22} {'Acuracia':>9} {'Precision':>10} {'Recall':>7} {'F1-Score':>9}")
print("  " + "-" * 62)

for nome_modelo, modelo in modelos.items():
    y_pred = modelo.predict(X_test_sc)

    acc = accuracy_score(y_test, y_pred)
    pre = precision_score(y_test, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_test, y_pred, average="weighted", zero_division=0)
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

# ── FIGURA 1: Comparacao de metricas entre modelos
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
    for barra, val in zip(barras, valores):
        ax.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.01,
                f"{val:.3f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.axhline(1.0, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)

plt.tight_layout()
plt.savefig(os.path.join(output_dir_graficos, "graficos_comparacao.png"), dpi=150, bbox_inches="tight")
plt.close()
print("  [OK] 'graficos_comparacao.png' salvo.")

# ── FIGURA 2: Matriz de confusao do melhor modelo
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
plt.savefig(os.path.join(output_dir_graficos, "matriz_confusao.png"), dpi=150, bbox_inches="tight")
plt.close()
print("  [OK] 'matriz_confusao.png' salvo.")

# ── FIGURA 3: Curva ROC multiclasse (One-vs-Rest)
y_test_bin = label_binarize(y_test, classes=[0, 1, 2])
y_prob = melhor_modelo.predict_proba(X_test_sc)

fig, ax = plt.subplots(figsize=(8, 6))

cores_roc = ["#1f77b4", "#ff7f0e", "#2ca02c"]
for i, (label, cor) in enumerate(zip(LABELS_RISCO, cores_roc)):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_prob[:, i])
    roc_auc = auc(fpr, tpr)
    ax.plot(fpr, tpr, color=cor, lw=2,
            label=f"Risco {label}  (AUC = {roc_auc:.2f})")

ax.plot([0,1], [0,1], "k--", lw=1.2, label="Aleatorio (AUC = 0.50)")

ax.set_title(f"Curva ROC Multiclasse (OvR)\n{melhor_nome}",
             fontweight="bold", fontsize=12)
ax.set_xlabel("Taxa de Falso Positivo (FPR)", fontsize=11)
ax.set_ylabel("Taxa de Verdadeiro Positivo (TPR)", fontsize=11)
ax.legend(loc="lower right", fontsize=10)
ax.set_xlim([0, 1])
ax.set_ylim([0, 1.05])

plt.tight_layout()
plt.savefig(os.path.join(output_dir_graficos, "curva_roc.png"), dpi=150, bbox_inches="tight")
plt.close()
print("  [OK] 'curva_roc.png' salvo.")

# ════════════════════════════════════════════════════════════════
# ETAPA 10 — PREDICAO PARA UM NOVO PACIENTE
# ════════════════════════════════════════════════════════════════
print("\n[ETAPA 10] Simulando predicao para um novo paciente...\n")

novo_paciente = {
    "nome"      : "Fernanda",
    "idade"     : 63,
    "glicose"   : 148.0,
    "pressao"   : 155.0,
    "imc"       : 31.5,
    "colesterol": 248.0,
}

print("  Dados do novo paciente:")
print(f"  {'Nome':<14}: {novo_paciente['nome']}")
print(f"  {'Idade':<14}: {novo_paciente['idade']} anos")
print(f"  {'Glicose':<14}: {novo_paciente['glicose']} mg/dL")
print(f"  {'Pressao':<14}: {novo_paciente['pressao']} mmHg")
print(f"  {'IMC':<14}: {novo_paciente['imc']} kg/m2")
print(f"  {'Colesterol':<14}: {novo_paciente['colesterol']} mg/dL")

entrada = np.array([[
    novo_paciente["idade"],
    novo_paciente["glicose"],
    novo_paciente["pressao"],
    novo_paciente["imc"],
    novo_paciente["colesterol"]
]])

entrada_sc = scaler.transform(entrada)

classe_predita = melhor_modelo.predict(entrada_sc)[0]
probabilidades = melhor_modelo.predict_proba(entrada_sc)[0]

rotulo_risco = {0: "BAIXO", 1: "MEDIO", 2: "ALTO"}

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

# ════════════════════════════════════════════════════════════════
# ETAPA 11 — SALVAR MODELO E SCALER PARA A API
# ════════════════════════════════════════════════════════════════
print("\n[ETAPA 11] Salvando modelo e scaler para producao...\n")

# Salva o melhor modelo treinado
modelo_path = os.path.join(output_dir_modelos, "melhor_modelo.pkl")
joblib.dump(melhor_modelo, modelo_path)
print(f"  [OK] Modelo '{melhor_nome}' salvo como '{modelo_path}'")

# Salva o scaler para normalizar novos dados
scaler_path = os.path.join(output_dir_modelos, "scaler.pkl")
joblib.dump(scaler, scaler_path)
print(f"  [OK] StandardScaler salvo como '{scaler_path}'")

# Salva metadados
metadados = {
    "melhor_modelo": melhor_nome,
    "features": FEATURES,
    "acuracia": float(melhor_dados["acuracia"]),
    "f1_score": float(melhor_dados["f1"]),
    "cv_media": float(melhor_dados["cv_media"]),
}
metadados_path = os.path.join(output_dir_modelos, "metadados_modelo.pkl")
joblib.dump(metadados, metadados_path)
print(f"  [OK] Metadados salvos como '{metadados_path}'")

print()
print("=" * 62)
print("Pipeline concluido com sucesso.")
print("\nArquivos gerados:")
print(f"  📊 Gráficos:  {output_dir_graficos}")
print(f"     - graficos_comparacao.png")
print(f"     - matriz_confusao.png")
print(f"     - curva_roc.png")
print(f"  🤖 Modelos:   {output_dir_modelos}")
print(f"     - melhor_modelo.pkl (modelo treinado)")
print(f"     - scaler.pkl (normalizador)")
print(f"     - metadados_modelo.pkl (informacoes)")
print("\n✅ Pronto para usar na API e Interface!")
print("=" * 62)
