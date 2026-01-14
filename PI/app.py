from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
from backend.database import criar_tabelas, registrar_usuario, autenticar_usuario, listar_pendentes, aprovar_usuario, obter_qrcode_path
from backend.gerar_qrcode import gerar_qrcode

app = Flask(__name__)
CORS(app)

criar_tabelas()

@app.route('/registrar', methods=['POST'])
def registrar():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    tipo = data.get('tipo', 'usuario') 
    
    if not nome or not email or not senha:
        return jsonify({'success': False, 'message': 'Campos obrigatórios faltando.'})
    
    success = registrar_usuario(nome, email, senha, tipo)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Email já cadastrado ou erro no servidor.'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    senha = data.get('senha')
    
    if not email or not senha:
        return jsonify({'success': False, 'message': 'Email e senha obrigatórios.'})
    
    user = autenticar_usuario(email, senha)
    if user:
        return jsonify({'success': True, 'usuario': user})
    else:
        return jsonify({'success': False, 'message': 'Credenciais inválidas ou usuário não aprovado.'})

@app.route('/usuarios_pendentes', methods=['GET'])
def usuarios_pendentes():
    return jsonify(listar_pendentes())

@app.route('/aprovar_usuario/<int:usuario_id>', methods=['POST'])
def aprovar(usuario_id):
    if aprovar_usuario(usuario_id):
        gerar_qrcode(usuario_id)
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/qrcode/<int:usuario_id>', methods=['GET'])
def qrcode(usuario_id):
    caminho = obter_qrcode_path(usuario_id)
    if not caminho:
        admin_path = os.path.join('backend', 'qrcodes', f'admin_{usuario_id}.png')
        if os.path.exists(admin_path):
            return send_file(admin_path, mimetype='image/png')
        return jsonify({'error': 'QR Code não encontrado'}), 404

    if os.path.exists(caminho):
        return send_file(caminho, mimetype='image/png')
    return jsonify({'error': 'QR Code não encontrado'}), 404

@app.route('/html/<path:filename>')
def serve_html(filename):
    return send_from_directory('frontend/html', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('frontend/js', filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('frontend', filename)

if __name__ == '__main__':
    app.run(debug=True)