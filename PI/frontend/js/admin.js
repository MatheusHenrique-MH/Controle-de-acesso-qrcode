const API_URL = 'http://localhost:5000';

window.onload = async () => {
    const usuarioId = localStorage.getItem('usuarioId');

    const qrCodeImg = document.getElementById('qrcodeAdmin');
    if (usuarioId && qrCodeImg) {
        qrCodeImg.src = `${API_URL}/qrcode/${usuarioId}`;
    }

    try {
        const res = await fetch(`${API_URL}/usuarios_pendentes`);
        const lista = await res.json();
        const ul = document.getElementById('lista');
        lista.forEach(user => {
            const li = document.createElement('li');
            li.classList.add('usuario-card');
            li.innerHTML = `${user.nome} (${user.email}) <button onclick="aprovar(${user.id})">Aprovar</button>`;
            ul.appendChild(li);
        });
    } catch (error) {
        console.error('Erro ao carregar usuários pendentes:', error);
    }
};

async function aprovar(id) {
    try {
        const res = await fetch(`${API_URL}/aprovar_usuario/${id}`, {
            method: 'POST'
        });
        const data = await res.json();
        if (data.success) {
            alert('Usuário aprovado com sucesso!');
            location.reload();
        } else {
            alert('Erro ao aprovar usuário.');
        }
    } catch (error) {
        console.error('Erro na aprovação:', error);
        alert('Erro ao aprovar usuário.');
    }
}

function logout() {
    localStorage.clear();
    location.href = 'login.html';
}
