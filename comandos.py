import textwrap, datetime
from fpdf import FPDF

hora_atual = datetime.datetime.now().strftime("%H-%M-%S")

def verificarCredenciais(username, password):
    with open("usuarios.txt", "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            dados = linha.strip().split()
            if len(dados) == 2 and dados[0] == username and dados[1] == password:
                return True
        return 
    

def criarCarta(data, destinatario, mensagem, remetente):
    global hora_atual
    carta = open("carta" + hora_atual + ".txt", "w", encoding="utf-8")
    print(data + destinatario + mensagem + remetente)
    carta.write(
        "Data: "
        + data
        + "\n"
        + "Destinatário: "
        + destinatario
        + "\n"
        + "Mensagem:\n"
        + mensagem
        + "\n"
        + "Remetente: "
        + remetente
    )
    carta.close()

def txtParaPdf(txt, arquivo):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family="Courier", size=fontsize_pt)
    splitted = txt.split("\n")

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(arquivo, "F")

def cadastrarUsuario(username, password):
    with open("usuarios.txt", "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            dados = linha.strip().split()
            if len(dados) == 2 and dados[0] == username:
                return False

    with open("usuarios.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{username} {password}\n")
    return True
