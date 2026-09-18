import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X = np.array([
    [500, 80, 0.1], [1200, 80, 0.5], [64, 22, 0.02], [64000, 4444, 10.0], [45000, 8080, 15.0],
    [60000, 31337, 20.0], [800, 443, 0.3], [300, 53, 0.05], [55000, 9999, 18.0], [200, 25, 0.2],
])
y = np.array([0, 0, 0, 1, 1, 1, 0, 0, 1, 0])
caso_novo = [[58000, 4444, 16.0]]

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.3, random_state=42
)

modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_treino, y_treino)

acc = accuracy_score(y_teste, modelo.predict(X_teste))
print(f"Acurácia no teste: {acc:.2f}")

pred = modelo.predict(caso_novo)[0]
rotulo = "Malicioso" if pred == 1 else "Normal"
print(f"Caso novo {caso_novo[0]} -> {rotulo} ({pred})")
