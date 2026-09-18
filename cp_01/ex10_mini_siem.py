import re
from datetime import datetime
from pymongo import MongoClient
from sklearn.tree import DecisionTreeClassifier

ARQUIVO_LOG = "auth.log"
LIMITE_SUSPEITO = 5

PADRAO = re.compile(r"^(\S+ \S+) (\w+) usuario=(\S+) ip=(\S+)$")

documentos = []
with open(ARQUIVO_LOG, encoding="utf-8") as f:
    for num, linha in enumerate(f, start=1):
        linha = linha.strip()
        if not linha:
            continue
        m = PADRAO.match(linha)
        if not m:
            print(f"Linha {num} ignorada (formato inválido): {linha}")
            continue
        ts, tipo, usuario, ip = m.groups()
        documentos.append({
            "timestamp": datetime.strptime(ts, "%Y-%m-%d %H:%M:%S"),
            "tipo": tipo.upper(),
            "usuario": usuario,
            "ip": ip,
        })

client = MongoClient("mongodb://localhost:27017/")
col = client["lab_seguranca"]["auth_eventos"]
col.delete_many({})
col.insert_many(documentos)
print(f"Eventos inseridos no MongoDB: {col.count_documents({})}")

pipeline = [
    {"$match": {"tipo": "FAIL"}},
    {"$group": {"_id": "$ip", "fails": {"$sum": 1}}},
    {"$sort": {"fails": -1}},
]
contagem = list(col.aggregate(pipeline))

print("Contagem por IP:")
for doc in contagem:
    rotulo = 1 if doc["fails"] >= LIMITE_SUSPEITO else 0
    print(f"  {doc['_id']:<15} -> {doc['fails']} FAILs (suspeito={rotulo})")

X = [[doc["fails"]] for doc in contagem]
y = [1 if doc["fails"] >= LIMITE_SUSPEITO else 0 for doc in contagem]

referencia = [0, 1, 2, 4, 6, 12, 20]
X += [[q] for q in referencia]
y += [1 if q >= LIMITE_SUSPEITO else 0 for q in referencia]
print(f"Dataset de treino: {X} rótulos {y}")

modelo = DecisionTreeClassifier(random_state=42)
modelo.fit(X, y)

novo = [[8]]
pred = modelo.predict(novo)[0]
print(f"Previsão para IP com 8 falhas -> {'Suspeito' if pred == 1 else 'Normal'} ({pred})")

client.close()
