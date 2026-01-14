import sqlite3
import bcrypt
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'usuarios.db')

def criar_tabelas():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                aprovado INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

def registrar_usuario(nome, email, senha, tipo='usuario'):
    hashed = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()
    try:
        aprovado = 2 if tipo == 'admin' else 0  
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO usuarios (nome, email, senha, aprovado) VALUES (?, ?, ?, ?)',
                      (nome, email, hashed, aprovado))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def autenticar_usuario(email, senha):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id, nome, senha, aprovado FROM usuarios WHERE email = ?', (email,))
        row = c.fetchone()
        if row and bcrypt.checkpw(senha.encode(), row[2].encode()):
            return {'id': row[0], 'nome': row[1], 'tipo': 'admin' if row[3] == 2 else 'usuario' if row[3] == 1 else 'pendente'}
    return None

def listar_pendentes():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('SELECT id, nome, email FROM usuarios WHERE aprovado = 0')
        return [{'id': row[0], 'nome': row[1], 'email': row[2]} for row in c.fetchall()]

def aprovar_usuario(usuario_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('UPDATE usuarios SET aprovado = 1 WHERE id = ?', (usuario_id,))
        conn.commit()
        return c.rowcount > 0

def obter_qrcode_path(usuario_id):
    path = os.path.join(os.path.dirname(__file__), 'qrcodes', f'qrcode_{usuario_id}.png')
    return path if os.path.exists(path) else None