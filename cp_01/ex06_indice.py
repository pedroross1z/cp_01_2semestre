from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
col = client["lab_seguranca"]["eventos_massa"]
col.drop()

ips = ["185.220.101.1", "91.240.118.172", "45.33.32.156", "192.168.1.10"]
eventos = []
for i in range(1000):
    eventos.append({
        "seq": i,
        "ip": ips[i % len(ips)],
        "tipo": "FAIL" if i % 3 else "OK",
    })

col.insert_many(eventos)
print(f"{col.count_documents({})} eventos inseridos.")

col.create_index("ip")
print("Índice criado em 'ip'.")

alvo = "185.220.101.1"
print(f"Eventos do IP {alvo}: {col.count_documents({'ip': alvo})}")

# Por que o índice importa:
# Sem índice o MongoDB faz COLLSCAN: lê todos os documentos, custo O(n), que cresce junto com a coleção.
# Com índice (árvore B) ele faz IXSCAN e vai direto aos registros do IP, ~O(log n), mesmo com milhões de eventos.

client.close()
