import mysql.connector

DB_CONFIG = {"host": "localhost", "user": "root", "password": "SUA_SENHA"}

usuarios = [("admin", "admin@x.com"), ("ana", "ana@x.com"), ("bruno", "bruno@x.com")]
entrada = "' OR '1'='1"

conn = mysql.connector.connect(**DB_CONFIG)
cur = conn.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS lab_seguranca")
cur.execute("USE lab_seguranca")
cur.execute("DROP TABLE IF EXISTS usuarios")
cur.execute("CREATE TABLE usuarios (id INT PRIMARY KEY AUTO_INCREMENT, "
            "nome VARCHAR(50), email VARCHAR(100))")
cur.executemany("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", usuarios)
conn.commit()

def buscar_inseguro(cursor, nome):

    sql = "SELECT nome, email FROM usuarios WHERE nome = '" + nome + "'"
    cursor.execute(sql)
    return cursor.fetchall()

def buscar_seguro(cursor, nome):

    cursor.execute("SELECT nome, email FROM usuarios WHERE nome = %s", (nome,))
    return cursor.fetchall()

r1 = buscar_inseguro(cur, entrada)
print(f"[INSEGURO] entrada={entrada}  -> {len(r1)} usuários (VAZAMENTO)")

r2 = buscar_seguro(cur, entrada)
print(f"[SEGURO]   entrada={entrada}  -> {len(r2)} usuários (defesa OK)")

cur.close()
conn.close()
