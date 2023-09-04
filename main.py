from flask import Flask, render_template, request, redirect, session, url_for, flash
import datetime, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)

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
        password =  request.form.get("password")
        if verificarCredenciais(username, password):
            session["username"] = username
            session["password"] = password
            return redirect(url_for("enviarCarta"))
        else:
            flash("Usuário ou senha incorretos.", "error")
            return redirect(url_for("home"))
    else:
        print("deu errado")
        return redirect(url_for("home"))

@app.route("/carta")
def enviarCarta():
    username = session.get("username")
    password = session.get("password")
    if username:
        return render_template("carta.html", username=username, password=password, data_atual=data_atual)
    else:
        flash("Você precisa fazer login para acessar essa página.", "error")

if __name__ == "__main__":
    app.run(debug = True)