# -*- coding: utf-8 -*-
import os
import sys
import psycopg2
import urlparse
from flask import Flask, request, redirect, url_for, current_app, render_template

reload(sys)     
sys.setdefaultencoding("utf-8")

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
cur2 = conn.cursor()

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
            #return redirect(url_for('dispositivosHTML'))
            cur2.execute("SELECT * FROM dispositivos WHERE idUsuario = " + str(row[0]) + " ORDER BY Id ASC")
            rows2 = cur2.fetchall()
            respLogado = current_app.make_response(render_template("dispositivos.html", nome = row[1], dispositivos = rows2, pag = "1"))
            respLogado.set_cookie('IdUsuario', row[0])
            respLogado.set_cookie('Nome', row[1])
            return respLogado
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
    cur.execute("INSERT INTO login (nome, email, senha) VALUES(%s, %s, %s)", (request.form['nome'], request.form['email'], request.form['pwd']))
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
        dispositivos = dispositivos + "<li>id: " + str(row[0]) + "</li><li>id Usuario: " + str(row[1]) + "</li><li>Dispositivo: " + row[2]  + "</li><li>MAC: " + row[3] + "</li><li>Estado: " + str(row[4]) + str(row[5]) + str(row[6]) + str(row[7]) + str(row[8]) + str(row[9]) + str(row[10]) + str(row[11]) + str(row[12]) + str(row[13]) + "</li><li>----</li>"
    dispositivos += "</ul>" 
    return "Dispositivos cadastrados: " + dispositivos

#Cadastrar no banco o dispositivo
@app.route("/cadastrarDispositivos", methods=["POST"])
def cadastrarDispositivoDB():
    cur.execute("INSERT INTO dispositivos ( idUsuario, dispositivo, mac, a0, d0, d1, d2, d3, d4, d5, d6, d7, d8) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ( request.form['idUsuario'], request.form['dispositivo'], request.form['MAC'], request.form['a0'], request.form['d0'], request.form['d1'], request.form['d2'], request.form['d3'], request.form['d4'], request.form['d5'], request.form['d6'], request.form['d7'], request.form['d8']))
    conn.commit()
    return "Dispositivo inserido com sucesso!"

#Atualizar campo no dispositivo --- em teste
#http://site/atualizarDispositivoDB?porta=d0&valor=1&IdDisp=9
@app.route("/atualizarDispositivoDB", methods=["GET"])
def atualizarDispositivoDB():
    SQLcomando = "UPDATE dispositivos SET " + request.args.get('porta') + "=" + request.args.get('valor') + " WHERE Id=" + request.args.get('IdDisp')
    cur.execute(SQLcomando)
    conn.commit()
    
    IdUsuario = request.cookies.get('IdUsuario')
    Nome = request.cookies.get('Nome')
    cur2.execute("SELECT * FROM dispositivos WHERE idUsuario = " + IdUsuario + " ORDER BY Id ASC")
    rows2 = cur2.fetchall()
    print "::" + request.args.get('IdDisp')
    return render_template("dispositivos.html", nome = Nome, dispositivos = rows2, pag = "1") #str(request.args.get('IdDisp')))
   

#----------------------------------------------------------#
#                       Funcoes de Teste                   #
#----------------------------------------------------------#
@app.route("/<name>")
def nome(name):
    return "Pagina nao encontrada: {}".format(name)

#http://site/get?nome=ewerton&frase=aeiou
@app.route("/get", methods=["GET"])
def get():
    nome = request.args.get('nome')
    frase = request.args.get('frase')
    return "Nome: " + nome + " - qualquer coisa: " + frase

@app.route("/criarTabelaLogin")
def criarTabelaLogin():
    cur.execute("CREATE TABLE login(Id SERIAL PRIMARY KEY, nome VARCHAR(30), email VARCHAR(50), senha VARCHAR(20))")    
    conn.commit()
    return "<p>Criado tabela login</p>"

@app.route("/criarTabelaDispositivos")
def criarTabelaDispositivos():
    cur.execute("CREATE TABLE dispositivos(Id SERIAL PRIMARY KEY, idUsuario INTEGER, dispositivo VARCHAR(50), mac VARCHAR(17), a0 INTEGER, d0 INTEGER, d1 INTEGER, d2 INTEGER, d3 INTEGER, d4 INTEGER, d5 INTEGER, d6 INTEGER, d7 INTEGER, d8 INTEGER)")    
    conn.commit()
    return "<p>Criado tabela dispositivos</p>"

@app.route("/deleteTabela/<tabela>")
def deleteTabela(tabela):
    SQLcomando = "DROP TABLE " + tabela
    cur.execute(SQLcomando)    
    conn.commit()
    return "<p>Tabela {} deletada!</p>".format(tabela)    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
