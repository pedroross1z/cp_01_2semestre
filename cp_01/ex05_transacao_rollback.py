import mysql.connector

DB_CONFIG = {"host": "localhost", "user": "root", "password": "SUA_SENHA"}

contas = [(1, "Alice", 1000), (2, "Bob", 500)]

conn = mysql.connector.connect(**DB_CONFIG)
conn.autocommit = False
cur = conn.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS lab_seguranca")
cur.execute("USE lab_seguranca")
cur.execute("DROP TABLE IF EXISTS contas")

cur.execute("CREATE TABLE contas (id INT PRIMARY KEY, titular VARCHAR(50), "
            "saldo DECIMAL(10,2) NOT NULL) ENGINE=InnoDB")
cur.executemany("INSERT INTO contas (id, titular, saldo) VALUES (%s, %s, %s)", contas)
conn.commit()

def saldo(conta_id):
    cur.execute("SELECT saldo FROM contas WHERE id = %s", (conta_id,))
    return int(cur.fetchone()[0])

def transferir(origem, destino, valor):
    try:
        cur.execute("UPDATE contas SET saldo = saldo - %s WHERE id = %s", (valor, origem))
        if cur.rowcount == 0:
            raise ValueError("conta origem inexistente")

        cur.execute("UPDATE contas SET saldo = saldo + %s WHERE id = %s", (valor, destino))

        if cur.rowcount == 0:
            raise ValueError("conta destino inexistente")

        conn.commit()
        return True, None
    except (ValueError, mysql.connector.Error) as e:
        conn.rollback()
        return False, str(e)

ok, erro = transferir(1, 2, 200)
if ok:
    print(f"Transferência 1 OK. Alice={saldo(1)}, Bob={saldo(2)}")

ok, erro = transferir(1, 99, 100)
if not ok:
    print(f"Transferência 2 FALHOU ({erro}). Rollback. Alice={saldo(1)}")

cur.close()
conn.close()
