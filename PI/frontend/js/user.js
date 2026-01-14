window.onload = () => {
    const id = localStorage.getItem('usuarioId');
    document.getElementById('qrcode').src = `http://localhost:5000/qrcode/${id}`;
};

function logout() {
    localStorage.clear();
    location.href = 'login.html';
}
