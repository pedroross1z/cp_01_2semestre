from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
col = client["lab_seguranca"]["eventos"]
col.delete_many({})

eventos = [
    {"tipo": "FAIL", "ip": "185.220.101.1"}, {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "OK",   "ip": "192.168.1.10"},  {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "185.220.101.1"}, {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "45.33.32.156"},  {"tipo": "FAIL", "ip": "185.220.101.1"},
]
col.insert_many(eventos)

pipeline = [
    {"$match": {"tipo": "FAIL"}},
    {"$group": {"_id": "$ip", "total": {"$sum": 1}}},
    {"$sort": {"total": -1}},
    {"$limit": 3},
]

for doc in col.aggregate(pipeline):
    print(f"{doc['_id']:<15} -> {doc['total']}")

client.close()
