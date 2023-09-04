from flask import Flask, render_template, request, redirect, session, url_for, flash
import datetime, secrets, textwrap, sys

sys.stdout.reconfigure(encoding='utf-8')

from fpdf import FPDF

i = 0

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)

data_atual = datetime.datetime.now().strftime("%d/%m/%Y")

def verificarCredenciais(username, password):
    with open("usuarios.txt", "r", encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            dados = linha.strip().split()
            if len(dados) == 2 and dados[0] == username and dados[1] == password:
                return True
        return False
    
def criarCarta(data, destinatario, mensagem, remetente):
    global i
    carta = open("carta"+str(i)+".txt", "a", encoding='utf-8')
    print(data+destinatario+mensagem+remetente)
    carta.write("Data: "+data+"\n"+"Destinatário: "+destinatario+"\n"+"Mensagem:\n"+mensagem+"\n"
                +"Remetente: "+remetente)
    carta.close()
    i+=1
    
    
def txtParaPdf(txt, arquivo):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fontsize_pt)
    splitted = txt.split('\n')
    
    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)
            
    pdf.output(arquivo, 'F')


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
            
            nome_arquivo_texto = f"carta{i-1}.txt"
            nome_arquivo_pdf = f"carta{i-1}.pdf"
            
            with open(nome_arquivo_texto, "r", encoding='utf-8') as arquivo_texto:
                conteudo_texto = arquivo_texto.read()
                
                txtParaPdf(conteudo_texto, nome_arquivo_pdf)
            
        return render_template("carta.html", username=username, data_atual=data_atual)
    else:
        flash("Você precisa fazer login para acessar essa página.", "error")
        return redirect(url_for("home"))
    
if __name__ == "__main__":
    app.run(debug = True)