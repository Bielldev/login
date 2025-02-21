document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Impede o envio do formulário

    // Captura os valores dos campos
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Simulação de credenciais válidas (apenas para exemplo)
    const validUsername = 'usuario';
    const validPassword = 'senha123';

    // Validação
    if (username === validUsername && password === validPassword) {
        document.getElementById('message').textContent = 'Login bem-sucedido!';
        document.getElementById('message').style.color = 'green';
        // Redirecionar para outra página (opcional)
        // window.location.href = 'pagina-secreta.html';
    } else {
        document.getElementById('message').textContent = 'Usuário ou senha incorretos.';
        document.getElementById('message').style.color = 'red';
    }
});