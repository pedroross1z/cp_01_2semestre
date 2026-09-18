import numpy as np
from sklearn.ensemble import IsolationForest

trafego = np.array([
    [100, 5], [120, 6], [110, 5], [105, 4], [50000, 500], [109, 5], [111, 6], [45000, 450],
])

modelo = IsolationForest(contamination=0.25, random_state=42)
rotulos = modelo.fit_predict(trafego)

for i, (amostra, r) in enumerate(zip(trafego, rotulos)):
    status = "ANOMALIA" if r == -1 else "Normal"
    print(f"Amostra {i}: {amostra.tolist()} -> {status}")
