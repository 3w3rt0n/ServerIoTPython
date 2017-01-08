import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Hello World</hi>"


@app.route("/<name>")
def index(name):
    if name.lower() == "ewerton":
        return "Olá {}".format(name)
    else:
        return "Not Found"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
