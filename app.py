from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_wtf.csrf import CSRFProtect
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'gabriel2008'  # Chave secreta para sessões e CSRF
csrf = CSRFProtect(app)  # Proteção CSRF

# Configurações do banco de dados MySQL
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "gabriel2008"
MYSQL_DATABASE = "banco_dados"

# Função para conectar ao banco de dados
def conectar_banco_de_dados():
    try:
        conexao = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        return conexao
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return None

# Função para verificar o login
def verificar_login(cursor, login, senha):
    try:
        cursor.execute("SELECT senha_login FROM login WHERE usuario_login = %s", (login,))
        resultado = cursor.fetchone()

        if resultado:
            senha_hash_armazenado = resultado[0]
            if check_password_hash(senha_hash_armazenado, senha):
                return True
        return False
    except mysql.connector.Error as erro:
        print(f"Erro na consulta: {erro}")
        return False

# Função para registrar um novo usuário
def registrar_usuario(cursor, login, senha):
    try:
        senha_hash = generate_password_hash(senha)
        cursor.execute(
            "INSERT INTO login (usuario_login, senha_login) VALUES (%s, %s)",
            (login, senha_hash)
        )
        return True
    except mysql.connector.Error as erro:
        print(f"Erro ao registrar usuário: {erro}")
        return False

# Rota principal (login)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('usuario_login')
        senha = request.form.get('senha_login')

        if not login or not senha:
            flash('Por favor, preencha todos os campos.', 'error')
        else:
            conexao = conectar_banco_de_dados()
            if conexao:
                cursor = conexao.cursor()
                if verificar_login(cursor, login, senha):
                    session['login'] = login  # Armazena o login na sessão
                    flash('Login realizado com sucesso!', 'success')
                    return redirect(url_for('sucesso'))
                else:
                    flash('Login ou senha incorretos.', 'error')
                cursor.close()
                conexao.close()
            else:
                flash('Erro ao conectar ao banco de dados.', 'error')
    return render_template('login.html')

# Rota de sucesso após o login
@app.route('/sucesso')
def sucesso():
    if 'login' in session:
        return render_template('sucesso.html', usuario=session['login'])
    else:
        flash('Você precisa fazer login para acessar esta página.', 'error')
        return redirect(url_for('login'))

# Rota de logout
@app.route('/logout')
def logout():
    session.pop('login', None)
    flash('Você foi deslogado com sucesso.', 'success')
    return redirect(url_for('login'))

# Rota de registro de usuários
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        # Processar os dados do formulário
        login = request.form.get('usuario_login')
        senha = request.form.get('senha_login')
        confirmar_senha = request.form.get('confirmar_senha')

        if not login or not senha or not confirmar_senha:
            flash('Por favor, preencha todos os campos.', 'error')
        elif senha != confirmar_senha:
            flash('As senhas não coincidem.', 'error')
        else:
            conexao = conectar_banco_de_dados()
            if conexao:
                cursor = conexao.cursor()
                if registrar_usuario(cursor, login, senha):
                    conexao.commit()
                    flash('Usuário registrado com sucesso! Faça login.', 'success')
                    return redirect(url_for('login'))
                else:
                    flash('Erro ao registrar usuário.', 'error')
                cursor.close()
                conexao.close()
            else:
                flash('Erro ao conectar ao banco de dados.', 'error')
    return render_template('registrar.html')

if __name__ == '__main__':
    app.run(debug=True)