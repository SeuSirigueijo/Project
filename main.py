from flask import Flask, render_template, request, redirect, url_for, flash
import datetime

app = Flask(__name__)

data_atual = datetime.datetime.now().strftime("%d-%m-%Y")

def verificarCredenciais(username, password):
    with open("usuarios.txt", "r") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            dados = linha.strip().split()
            if len(dados) == 2 and dados[0] == username and dados[1] == password:
                return True
        return False

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if verificarCredenciais(username, password):
            return render_template("carta.html")
    else:
        print("deu errado")
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug = True)