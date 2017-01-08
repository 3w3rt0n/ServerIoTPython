import os
import psycopg2
import urlparse
from flask import Flask, request, url_for, current_app, render_template

#Conexao do banco PostgreSQL
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cur = conn.cursor()

#Define a aplicacao
app = Flask("wtf")

@app.route("/")
def indexHTML():
    return current_app.send_static_file('login.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    return "Email: {}".format(request.form['email']) + "\nSenha: {}".format(request.form['pwd'])

#Cadastrar novo usuario
@app.route("/cadastrarLogin.html")
def cadastrarLoginHTML():
    return current_app.send_static_file('cadastrarLogin.html')

@app.route("/cadastrarLogin", methods=["POST"])
def cadastrarLoginDB():
    cur.execute("INSERT INTO login VALUES(%s, %s, %s, %s)", (2, request.form['nome'], request.form['email'], request.form['pwd']))
    conn.commit()
    return "Usuario inserido com sucesso!"

#Lista usuarios cadastrados
@app.route("/listaLogin")
def listaLoginDB():
    cur.execute("SELECT * FROM login")
    rows = cur.fetchall()
    usuarios = "<ul>"
    for row in rows:
        usuarios = usuarios + "<li>Nome: " + row[1] + "</li><li>Email: " + row[2] + "</li><br\>"
    usuarios += "</ul>" 
    return "Usuarios cadastrados: " + usuarios

#----------------------------------------------------------#
#                       Funcoes de Teste                   #
#----------------------------------------------------------#
@app.route("/<name>")
def nome(name):
    return "Ola {}".format(name)

@app.route("/criarTabela")
def criarTabela():
    cur.execute("CREATE TABLE login(Id INTEGER PRIMARY KEY, nome VARCHAR(30), email VARCHAR(50), senha VARCHAR(20))")    
    conn.commit()
    return "<p>Criado tabela</p>"
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
