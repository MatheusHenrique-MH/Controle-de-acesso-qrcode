import sqlite3
import qrcode
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'usuarios.db')

PASTA_QRCODES = os.path.join(os.path.dirname(__file__), 'qrcodes')
os.makedirs(PASTA_QRCODES, exist_ok=True)

EMAIL_ADMIN = 'igorlmeida@gmail.com'
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT id, nome FROM usuarios WHERE email = ? AND aprovado = 2", (EMAIL_ADMIN,))
admin = cursor.fetchone()

if admin:
    id_admin, nome = admin
    nome_arquivo = os.path.join(PASTA_QRCODES, f"admin_{id_admin}.png")
    conteudo = f"http://localhost:5000/qrcode/{id_admin}"  

    qr = qrcode.make(conteudo)
    qr.save(nome_arquivo)

    print(f"QR Code gerado para admin {nome} (ID: {id_admin}) em {nome_arquivo}")
else:
    print("Admin não encontrado ou ainda não aprovado.")

conn.close()
