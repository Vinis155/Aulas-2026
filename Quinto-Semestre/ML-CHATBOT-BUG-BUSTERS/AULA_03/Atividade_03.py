import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression



# Gerando 100 mensagens com tamanho entre 10 e 300 caracteres
np.random.seed(42)  # garante que o resultado seja sempre o mesmo

df = pd.DataFrame({
    'tamanho_msg': np.random.randint(10, 300, 100)
})

# Regra: Cada caractere adiciona 0.5 min + 5 min base


df['tempo_real_espera'] = (
    df['tamanho_msg'] * 0.5
) + 5 + np.random.normal(0, 2, len(df))

# 3. Separando Variáveis

X = df[['tamanho_msg']]  # Feature (Entrada)
y = df['tempo_real_espera']  # Target (Saída)

# 4. Treinando o Modelo

reg = LinearRegression()
reg.fit(X, y)

# 5. Mostrando Resultados

print("===== RESULTADO DO MODELO =====\n")

print(f"Intercepto (Tempo Base): {reg.intercept_:.2f} min")
print(f"Coeficiente (Aumento por Caractere): {reg.coef_[0]:.2f} min")

# 6. Teste de Previsão

novo_dado = pd.DataFrame({'tamanho_msg': [200]})
previsao = reg.predict(novo_dado)

print(f"\nPrevisão para 200 caracteres: {previsao[0]:.2f} minutos")