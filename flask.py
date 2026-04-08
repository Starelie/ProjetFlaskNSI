from flask import Flask

app = Flask(__name__)


@app.route("/")
def accueil():
    return "<h1>Bienvenue sur mon serveur Flask</h1>"


if __name__ == "__main__":
    app.run(debug=True)
