from flask import Flask, render_template, request, redirect, session, url_for, flash
import datetime, secrets

i = 0

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)

data_atual = datetime.datetime.now().strftime("%d/%m/%Y")

def verificarCredenciais(username, password):
    with open("usuarios.txt", "r") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            dados = linha.strip().split()
            if len(dados) == 2 and dados[0] == username and dados[1] == password:
                return True
        return False
    
def criarCarta(data, destinatario, mensagem, remetente):
    global i
    carta = open("carta"+str(i)+".txt", "a")
    print(data+destinatario+mensagem+remetente)
    carta.write(data+"\n"+destinatario+"\n"+mensagem+"\n"+remetente)
    carta.close()
    i+=1


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

@app.route("/carta", methods = ["POST", "GET"])
def enviarCarta():
    username = session.get("username")
    if username:
        if request.method == "POST":
            data = data_atual
            destinatario = request.form.get("destinatario")
            mensagem = request.form.get("mensagem")
            remetente = session["username"]
            criarCarta(data, destinatario, mensagem, remetente)
            flash("Carta enviada com sucesso!", "success")
        return render_template("carta.html", username=username, data_atual=data_atual)
    else:
        flash("Você precisa fazer login para acessar essa página.", "error")
        return redirect(url_for("home"))
    
if __name__ == "__main__":
    app.run(debug = True)