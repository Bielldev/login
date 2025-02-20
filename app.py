from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'gabriel2008'

# Configurações do banco de dados MySQL
MYSQL_HOST = "localhost"  # Ou o endereço do seu servidor MySQL
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

# Função para verificar o login (agora com hash de senha)
def verificar_login(cursor, login, senha):
    try:
        cursor.execute("SELECT senha_login FROM login WHERE usuario_login = %s", (login,))
        resultado = cursor.fetchone()

        if resultado:
            senha_hash_armazenado = resultado[0]
            if check_password_hash(senha_hash_armazenado, senha):  # Verifica o hash
                return True
        return False
    except mysql.connector.Error as erro:
        print(f"Erro na consulta: {erro}")
        return False

@app.route('/', methods=['GET', 'POST'])
def login():
    conexao = conectar_banco_de_dados()  # Conecta ao banco a cada requisição
    if conexao:
        cursor = conexao.cursor()
        if request.method == 'POST':
            login = request.form['login']
            senha = request.form['senha']

            if verificar_login(cursor, login, senha):
                session['login'] = login  # Armazena o login na sessão
                conexao.close()  # Fecha a conexão após o uso
                return redirect(url_for('sucesso'))
            else:
                conexao.close()  # Fecha a conexão mesmo em caso de falha
                return render_template('index.html', erro="Login ou senha incorretos.")

        conexao.close()  # Fecha a conexão para GET também
        return render_template('index.html')
    else:
        return "Erro ao conectar ao banco de dados."  # Ou uma página de erro mais amigável

@app.route('/sucesso')
def sucesso():
    if 'login' in session:  # Verifica se o usuário está logado
        return f"Você foi logado com sucesso, {session['login']}!"
    else:
        return redirect(url_for('login'))  # Redireciona para o login se não estiver logado

if __name__ == '__main__':
    app.run(debug=True)