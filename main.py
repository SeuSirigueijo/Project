#João Gabriel, André Mendes e Maria Eduarda

from flask import Flask, render_template, request, redirect, session, url_for, flash
import datetime, secrets, comandos


app = Flask(__name__)
app.secret_key = secrets.token_hex(24)

data_atual = datetime.datetime.now().strftime("%d/%m/%Y")
hora_atual = datetime.datetime.now().strftime("%H-%M-%S")

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if comandos.verificarCredenciais(username, password):
            session["username"] = username
            session["password"] = password
            return redirect(url_for("enviarCarta"))
        else:
            flash("Usuário ou senha incorretos", "error")
            return redirect(url_for("home"))
    else:
        print("deu errado")
        return redirect(url_for("home"))


@app.route("/cadastrar", methods=["POST", "GET"])
def cadastro():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if comandos.cadastrarUsuario(username, password):
            flash("Usuário cadastrado com sucesso!", "success")
            return redirect(url_for("home"))
        else:
            flash("Usuário existente, tente novamente", "error")
            return redirect(url_for("cadastro"))
    elif request.method == "GET":
        return render_template("cadastro.html")
    return render_template("cadastro.html")


@app.route("/carta", methods=["POST", "GET"])
def enviarCarta():
    username = session.get("username")
    if username:
        if request.method == "POST":
            data = data_atual
            destinatario = request.form.get("destinatario")
            mensagem = request.form.get("mensagem")
            remetente = session["username"]
            comandos.criarCarta(data, destinatario, mensagem, remetente)
            flash("Carta salva com sucesso!", "success")

            nome_arquivo_texto = f"carta{hora_atual}.txt"
            nome_arquivo_pdf = f"carta{hora_atual}.pdf"

            with open(nome_arquivo_texto, "r", encoding="utf-8") as arquivo_texto:
                conteudo_texto = arquivo_texto.read()

            comandos.txtParaPdf(conteudo_texto, nome_arquivo_pdf)

        return render_template("carta.html", username=username, data_atual=data_atual)
    else:
        flash("Você precisa fazer login para acessar essa página.", "error")
        return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)