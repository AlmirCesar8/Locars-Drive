// Validação frontend básica
document.addEventListener('DOMContentLoaded', function() {
    const formLogin = document.getElementById('form-login');
    const formRegistro = document.getElementById('form-registro');
    
    if (formLogin) {
        formLogin.addEventListener('submit', function(e) {
            const email = document.querySelector('#email');
            const senha = document.querySelector('#senha');
            
            if (!email.value || !senha.value) {
                e.preventDefault();
                alert('Preencha todos os campos.');
            }
        });
    }
    
    if (formRegistro) {
        formRegistro.addEventListener('submit', function(e) {
            const senha = document.querySelector('#senha');
            const confirmarSenha = document.querySelector('#confirmar_senha');
            
            if (senha.value !== confirmarSenha.value) {
                e.preventDefault();
                alert('As senhas não coincidem.');
            }
        });
    }
});