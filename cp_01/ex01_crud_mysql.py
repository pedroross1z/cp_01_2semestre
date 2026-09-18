import mysql.connector
from mysql.connector import errorcode

DB_CONFIG = {"host": "localhost", "user": "root", "password": "SUA_SENHA"}

ativos = [
    ("SRV-WEB01", "192.168.1.10", "servidor", "alta",  "ativo"),
    ("PC-RH03",   "192.168.1.45", "estacao",  "baixa", "ativo"),
    ("SW-CORE01", "192.168.1.1",  "switch",   "media", "inativo"),
]

conn = mysql.connector.connect(**DB_CONFIG)
cur = conn.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS lab_seguranca")
cur.execute("USE lab_seguranca")

cur.execute("DROP TABLE IF EXISTS ativos")
cur.execute("""
    CREATE TABLE ativos (
        id          INT PRIMARY KEY AUTO_INCREMENT,
        nome        VARCHAR(50) NOT NULL,
        ip          VARCHAR(15) NOT NULL UNIQUE,
        tipo        VARCHAR(20) NOT NULL,
        criticidade ENUM('baixa','media','alta') NOT NULL,
        status      VARCHAR(10) NOT NULL
    )
""")

sql_insert = ("INSERT INTO ativos (nome, ip, tipo, criticidade, status) "
              "VALUES (%s, %s, %s, %s, %s)")
cur.executemany(sql_insert, ativos)
conn.commit()
print(f"{cur.rowcount} ativos inseridos.")

cur.execute("SELECT nome, ip, criticidade, status FROM ativos WHERE tipo = %s", ("servidor",))
print("Listar tipo='servidor' ->")
for nome, ip, crit, status in cur.fetchall():
    print(f"  {nome} | {ip} | {crit} | {status}")

cur.execute("UPDATE ativos SET status = %s WHERE nome = %s", ("ativo", "SW-CORE01"))
conn.commit()
print(f"UPDATE SW-CORE01 -> {cur.rowcount} registro atualizado")

try:
    cur.execute(sql_insert, ("SRV-WEB02", "192.168.1.10", "servidor", "alta", "ativo"))
    conn.commit()
except mysql.connector.IntegrityError as e:
    conn.rollback()
    if e.errno == errorcode.ER_DUP_ENTRY:
        print("Erro tratado: IP 192.168.1.10 já cadastrado (violação de UNIQUE)")
    else:
        raise

cur.execute("DELETE FROM ativos WHERE nome = %s", ("PC-RH03",))
conn.commit()
print(f"DELETE PC-RH03 -> {cur.rowcount} registro removido")

cur.close()
conn.close()
