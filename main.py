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

#Enviar a pagina de login para o navegador
@app.route("/")
def indexHTML():
    return current_app.send_static_file('login.html')

#Verificar se o usuario e a senha estao corretos
@app.route("/login", methods=["POST"])
def login():
    cur.execute("SELECT * FROM login")
    rows = cur.fetchall()
    for row in rows:
        if request.form['email'] == row[2] and request.form['pwd'] == row[3]:
            redirect(url_for('dispositvos.html'))
    return "Email ou senha errado!<br /> <p>Email: {}".format(request.form['email']) + "</p><p>Senha: {}".format(request.form['pwd']) + "</p>"

@app.route("/dispositivos.html")
def dispositivosHTML():
    return current_app.send_static_file('dispositivos.html')    

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
        usuarios = usuarios + "<li>Nome: " + row[1] + "</li><li>Email: " + row[2] + "</li><li>Senha: " + row[3] + "</li><li>-------</li>"
    usuarios += "</ul>" 
    return "Usuarios cadastrados: " + usuarios

#Cadastrar novo usuario
@app.route("/cadastrarDispositivos.html")
def cadastrarDispositivosHTML():
    return current_app.send_static_file('cadastrarDispositivos.html')

#Lista dispositivos cadastrados
@app.route("/listaDispositivos")
def listaDispositivosDB():
    cur.execute("SELECT * FROM dispositivos")
    rows = cur.fetchall()
    dispositivos = "<ul>"
    for row in rows:
        dispositivos = dispositivos + "<li>id Usuario: " + str(row[1]) + "</li><li>MAC: " + row[2] + "</li><li>Estado: " + str(row[3]) + str(row[4]) + str(row[5]) + str(row[6]) + str(row[7]) + str(row[8]) + str(row[9]) + str(row[10]) + str(row[11]) + str(row[12]) + "</li><li>----</li>"
    dispositivos += "</ul>" 
    return "Dispositivos cadastrados: " + dispositivos

@app.route("/cadastrarDispositivos", methods=["POST"])
def cadastrarDispositivoDB():
    cur.execute("INSERT INTO dispositivos VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (2, request.form['idUsuario'], request.form['MAC'], request.form['a0'], request.form['d0'], request.form['d1'], request.form['d2'], request.form['d3'], request.form['d4'], request.form['d5'], request.form['d6'], request.form['d7'], request.form['d8']))
    conn.commit()
    return "Dispositivo inserido com sucesso!"


#----------------------------------------------------------#
#                       Funcoes de Teste                   #
#----------------------------------------------------------#
@app.route("/<name>")
def nome(name):
    return "Pagina nao encontrada: {}".format(name)

@app.route("/criarTabelaLogin")
def criarTabelaLogin():
    cur.execute("CREATE TABLE login(Id INTEGER PRIMARY KEY, nome VARCHAR(30), email VARCHAR(50), senha VARCHAR(20))")    
    conn.commit()
    return "<p>Criado tabela login</p>"

@app.route("/criarTabelaDispositivos")
def criarTabelaDispositivos():
    cur.execute("CREATE TABLE dispositivos(Id INTEGER PRIMARY KEY, idUsuario INTEGER, dispositivo VARCHAR(50), a0 INTEGER, d0 INTEGER, d1 INTEGER, d2 INTEGER, d3 INTEGER, d4 INTEGER, d5 INTEGER, d6 INTEGER, d7 INTEGER, d8 INTEGER)")    
    conn.commit()
    return "<p>Criado tabela dispositivos</p>"
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
