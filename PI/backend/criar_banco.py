import sqlite3

conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('admin', 'usuario')),
    aprovado INTEGER DEFAULT 0,
    qrcode_path TEXT
)
''')

conn.commit()
conn.close()

print("Banco de dados criado com sucesso com campo de QR Code incluído.")
