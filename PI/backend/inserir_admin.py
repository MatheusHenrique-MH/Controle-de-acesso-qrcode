import sqlite3
import bcrypt
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'usuarios.db')

nome = "Igor Batista"
email = "igorlmeida@gmail.com"
senha = "igor123"
aprovado = 2 

senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
if cursor.fetchone():
    print("Administrador já existe no banco.")
else:
    cursor.execute('''
        INSERT INTO usuarios (nome, email, senha, aprovado)
        VALUES (?, ?, ?, ?)
    ''', (nome, email, senha_hash, aprovado))

    conn.commit()
    print("Administrador inserido com sucesso.")

conn.close()