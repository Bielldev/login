import mysql.connector
import secrets
from werkzeug.security import generate_password_hash, check_password_hash

def conectar_banco_de_dados():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="gabriel2008",
            database="banco_dados"
        )
        cursor = conexao.cursor()
        return conexao, cursor
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return None, None

def gerar_senha():
    return secrets.token_hex(10)

def cadastrar_usuario(cursor, login, senha_hash):
    sql = 'INSERT INTO login (senha_login, usuario_login) VALUES (%s, %s);'
    dados = (senha_hash, login)
    try:
        cursor.execute(sql, dados)
        conexao.commit()
        print("Usuário cadastrado com sucesso!")
    except mysql.connector.Error as erro:
        print(f"Erro ao cadastrar usuário: {erro}")

def verificar_login(cursor, login, senha):
    sql = 'SELECT senha_login FROM login WHERE usuario_login = %s;'
    cursor.execute(sql, (login,))
    resultado = cursor.fetchone()

    if resultado and check_password_hash(resultado[0], senha):
        return True
    return False

conexao, cursor = conectar_banco_de_dados()

if conexao and cursor:
    print("Sua Senha Gerada Está logo abaixo, Guarde-a com segurança:")
    senha = gerar_senha()
    senha_hash = generate_password_hash(senha)
    print(senha)

    login = input("Digite seu nome de usuário: ")
    cadastrar_usuario(cursor, login, senha_hash)

    entrada_login = input("Login: ")
    entrada_senha = input("Senha: ")

    if verificar_login(cursor, entrada_login, entrada_senha):
        print("Você foi logado com sucesso!")
    else:
        print("Login ou senha incorretos.")
        print("Entre em contato com o suporte: @suportedev")

    conexao.close()