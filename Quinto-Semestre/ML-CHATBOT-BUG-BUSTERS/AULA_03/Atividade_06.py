import pandas as pd
from sklearn.linear_model import LinearRegression

# Dataset
data = {
    'tempo_conversa_min': [5, 12, 2, 20, 15, 8, 30, 10, 5, 25],
    'mensagens_trocadas': [10, 25, 4, 45, 30, 12, 60, 18, 9, 50],
    'custo_ads_real': [15.5, 32.0, 8.0, 55.0, 40.5, 20.0, 80.0, 25.0, 14.0, 65.0]
}

df = pd.DataFrame(data)

# Variáveis
X = df[['tempo_conversa_min', 'mensagens_trocadas']]
y = df['custo_ads_real']

# Modelo
model = LinearRegression()
model.fit(X, y)

# Previsão
previsao = model.predict([[15, 35]])

# Mostrando valores com 2 casas decimais
print("Previsão:", round(previsao[0], 2))
print("Intercepto:", round(model.intercept_, 2))
print("Coeficientes:", [round(c, 2) for c in model.coef_])