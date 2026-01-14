import qrcode
import os

def gerar_qrcode(usuario_id):
    diretorio = os.path.join(os.path.dirname(__file__), 'qrcodes')
    os.makedirs(diretorio, exist_ok=True)
    caminho = os.path.join(diretorio, f'qrcode_{usuario_id}.png')
    img = qrcode.make(f"ID do usuário: {usuario_id}")
    img.save(caminho)
