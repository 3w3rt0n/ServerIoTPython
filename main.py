import os
from flask import Flask, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello World</h1>"


@app.route("/<name>")
def nome(name):
    return "Ola {}".format(name)

@app.route("/login", methods=["GET", "POST"])
def login
    return "Email: {}".format(request.form['email'])
    

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
