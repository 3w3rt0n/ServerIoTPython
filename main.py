import os
from flask import Flask, request, url_for, current_app, render_template

app = Flask("wtf")

@app.route("/")
def index():
    return current_app.send_static_file('login.html')

@app.route("/<name>")
def nome(name):
    return "Ola {}".format(name)

@app.route("/login", methods=["GET", "POST"])
def login():
    return "Email: {}".format(request.form['email']) + "\nSenha: {}".format(request.form['pwd'])
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
