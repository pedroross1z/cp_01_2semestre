from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
col = client["lab_seguranca"]["vulnerabilidades"]
col.delete_many({})

vulns = [
    {"cve_id": "CVE-2024-001", "tipo": "SQL Injection",  "severidade": "Alta",    "corrigida": False},
    {"cve_id": "CVE-2024-002", "tipo": "XSS",            "severidade": "Media",   "corrigida": True},
    {"cve_id": "CVE-2024-003", "tipo": "Path Traversal", "severidade": "Critica", "corrigida": False},
]

res = col.insert_many(vulns)
print(f"{len(res.inserted_ids)} documentos inseridos.")

print("Buscar severidade='Alta' ->")
for v in col.find({"severidade": "Alta"}):
    print(f"  {v['cve_id']}: {v['tipo']}")

res = col.update_one({"cve_id": "CVE-2024-001"}, {"$set": {"corrigida": True}})
print(f"update corrigida=True em 001 -> {res.modified_count} documento modificado")

print(f"count corrigida=False -> {col.count_documents({'corrigida': False})}")

res = col.delete_one({"cve_id": "CVE-2024-002"})
print(f"delete CVE-2024-002 -> {res.deleted_count} documento removido")

client.close()
