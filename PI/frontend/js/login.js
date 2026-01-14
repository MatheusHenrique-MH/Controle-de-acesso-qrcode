let modoCadastro = false;
const API_URL = 'http://localhost:5000';

function alternarFormulario() {
    modoCadastro = !modoCadastro;

    const nomeInput = document.getElementById('nome');
    const titulo = document.getElementById('form-title');
    const botao = document.getElementById('actionButton');
    const textoAlternar = document.getElementById('alternarTexto');

    if (modoCadastro) {
        nomeInput.style.display = 'block';
        titulo.innerText = 'Cadastro de Usuário';
        botao.innerText = 'Cadastrar';
        textoAlternar.innerHTML = 'Já tem uma conta? <a href="#" onclick="alternarFormulario()">Entrar</a>';
    } else {
        nomeInput.style.display = 'none';
        titulo.innerText = 'Login';
        botao.innerText = 'Entrar';
        textoAlternar.innerHTML = 'Não tem uma conta? <a href="#" onclick="alternarFormulario()">Cadastre-se</a>';
    }

    document.getElementById('loginStatus').innerText = '';
}

async function executarAcao() {
    modoCadastro ? cadastrarUsuario() : login();
}

async function login() {
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    const res = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha })
    });

    const data = await res.json();
    const status = document.getElementById('loginStatus');

    if (data.success) {
        localStorage.setItem('usuarioId', data.usuario.id);
        localStorage.setItem('tipo', data.usuario.tipo);
        if (data.usuario.tipo === 'admin') {
            location.href = 'admin.html';
        } else if (data.usuario.tipo === 'usuario') {
            location.href = 'user.html';
        } else {
            status.innerText = "Aguardando aprovação do administrador.";
        }
    } else {
        status.innerText = "Login falhou. Verifique os dados.";
    }
}

async function cadastrarUsuario() {
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const senha = document.getElementById('senha').value;

    const res = await fetch(`${API_URL}/registrar`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome, email, senha, tipo: 'usuario' })
    });

    const data = await res.json();
    const status = document.getElementById('loginStatus');

    if (data.success) {
        status.style.color = '#4CAF50';
        status.innerText = 'Cadastro realizado com sucesso! Aguarde aprovação.';
    } else {
        status.style.color = '#ff5555';
        status.innerText = data.message || 'Erro no cadastro.';
    }
}
