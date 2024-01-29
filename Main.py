# Receber pedido de ligação (nome do cliente, telefone para contato, pedido, observações, endereço de entrega, 
# ponto de referencia, senha do pedido)
## Adicionar depois receber pedido por wpp.
# Cadastrar em uma planilha.
# O cliente deve receber via wpp todas essas informações.
import openpyxl
import customtkinter as custom
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
opcoes = webdriver.ChromeOptions()
opcoes.add_experimental_option("detach", True)

navegador = webdriver.Chrome(service=service, options=opcoes)
navegador.get("https://web.whatsapp.com/")

def confirma_exclusao():
    linhas = sheet_pedidos.max_row
    sheet_pedidos.delete_rows(2,linhas)
    excel_pedidos.save('./pedidos.xlsx')

    pedido_excluido = custom.CTkToplevel()
    pedido_excluido.title("Confirmação")
    pedido_excluido.geometry("400x130")
    pedido_excluido.resizable(False, False)
    pedido_excluido.grab_set()
    tex = custom.CTkLabel(pedido_excluido, text="Seu pedido foi excluído com sucesso!", font=fonte_label)
    tex.place(x=50,y=40)

    tex = custom.CTkButton(pedido_excluido, fg_color='green', text="Ok", font=('Tahoma bold', 13), command=pedido_excluido.destroy)
    tex.place(x=125,y=70)
    
def excluir_pedidos():
    confirmar = custom.CTkToplevel()
    confirmar.title("Confirmação")
    confirmar.geometry("400x130")
    confirmar.resizable(False, False)
    confirmar.grab_set()

    tex = custom.CTkLabel(confirmar, text="Deseja realmente excluir os pedidos?", font=fonte_label)
    tex.place(x=50,y=30)

    tex = custom.CTkButton(confirmar, fg_color='red', text="Confirmo", font=('Tahoma bold', 13), command=confirma_exclusao)
    tex.place(x=125,y=60)

def pegar_dados():
    nome = nome_entry.get()
    DDD = DDD_entry.get().removeprefix('0').replace(' ', '')
    telefone = telefone_entry.get().replace(' ', '')
    pedido = pedido_entry.get("0.0", "end")
    obs = obs_entry.get()
    endereco = endereco_entry.get("0.0", "end")
    referencia = referencia_entry.get()
    sheet_pedidos.append((nome,DDD+telefone,pedido,obs,endereco, referencia))
    excel_pedidos.save('pedidos.xlsx')
    
# Interação whatsapp
# link personalizado: https://web.whatsapp.com/send?phone=PAÍSDDDtelefone&text=TEXTO
# %0A -> função enter; %20 -> função espaço; *negrito*; _italico_; ~tachado~
    text = f"""
*Nome:* {nome}ENTER
*Pedido:* {pedido}ENTER
*Observações:* {obs}ENTER
*Endereço de entrega:* {endereco}ENTER
*Referência:* {referencia}ENTER""".replace(" ", "%20").replace("ENTER", "%0A")

    navegador.get(f"https://web.whatsapp.com/send?phone=55{DDD}{telefone}&text={text}")
    sleep(7)
    loading = 1
    while loading == 1:
        try:
            navegador.find_element('xpath', '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[3]')
        except:
            loading = 0
    navegador.find_element('xpath', '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span').click()

    pedido_salvo = custom.CTkToplevel()
    pedido_salvo.title("Confirmação")
    pedido_salvo.geometry("250x150")
    pedido_salvo.resizable(False, False)
    pedido_salvo.grab_set()
    tex = custom.CTkLabel(pedido_salvo, text="Seu pedido foi salvo!", font=fonte_label)
    tex.place(x=50,y=40)

    tex = custom.CTkButton(pedido_salvo, fg_color='green', text="Ok", font=('Tahoma bold', 13), command=pedido_salvo.destroy)
    tex.place(x=50,y=70)

excel_pedidos = openpyxl.load_workbook('./pedidos.xlsx')
sheet_pedidos = excel_pedidos['Pedidos']

janela = custom.CTk()
janela.geometry("480x550")
janela.title("Pedidos")
janela.resizable(False, False)

fonte_label = ('Tahoma bold', 15)
fonte_entry = ('Tahoma', 12)

# aviso para entrar no wpp primeiro
aviso = custom.CTkToplevel(janela)
aviso.geometry('450x100')
aviso.title('AVISO')
aviso.resizable(False, False)
aviso.grab_set()
t = custom.CTkLabel(aviso, text='Entre no whatsapp web antes de iniciar os registros.', font=fonte_label, text_color='RED')
t.place(x=25,y=15)
t = custom.CTkButton(aviso, fg_color='green', text="Ok", font=('Tahoma bold', 13), command=aviso.destroy)
t.place(x=150,y=50)

# Nome do cliente
nome = custom.CTkLabel(janela, text="Nome do cliente:", font=fonte_label)
nome.place(x=30,y=10)
nome_entry = custom.CTkEntry(janela, width=250, font=fonte_entry)
nome_entry.place(x=160,y=10)

# telefone para contato
telefone = custom.CTkLabel(janela, text="Número para contato:", font=fonte_label)
telefone.place(x=30,y=60)

DDD_entry = custom.CTkEntry(janela, width=37, placeholder_text='DDD', font=fonte_entry)
DDD_entry.place(x=197,y=60)

telefone_entry = custom.CTkEntry(janela, width=150, placeholder_text='Número', font=fonte_entry)
telefone_entry.place(x=245,y=60)

# pedido
pedido = custom.CTkLabel(janela, text="Pedido:", font=fonte_label)
pedido.place(x=30,y=120)
pedido_entry = custom.CTkTextbox(janela, width=250, height=150, font=fonte_entry)
pedido_entry.place(x=110,y=120)

# observações
obs = custom.CTkLabel(janela, text="Observações:", font=fonte_label)
obs.place(x=30,y=290)
obs_entry = custom.CTkEntry(janela, width=273, font=fonte_entry)
obs_entry.place(x=137,y=290)

# endereço de entrega
endereco = custom.CTkLabel(janela, text="Endereço da entrega:", font=fonte_label)
endereco.place(x=30,y=340)
endereco_entry = custom.CTkTextbox(janela, width=170, height=100, font=fonte_entry)
endereco_entry.place(x=205,y=340)

# ponto de referencia
referencia = custom.CTkLabel(janela, text="Referência:", font=fonte_label)
referencia.place(x=30,y=460)
referencia_entry = custom.CTkEntry(janela, width=288, font=fonte_entry)
referencia_entry.place(x=121,y=460)

# Salvar
salvar = custom.CTkButton(janela, text="Enviar", fg_color='green', font=('Tahoma bold', 13), command=pegar_dados)
salvar.place(x=80,y=500)

# Excluir pedidos
excluir = custom.CTkButton(janela, fg_color='red', text="Excluir pedidos", font=('Tahoma bold', 13), command=excluir_pedidos)
excluir.place(x=250,y=500)

janela.mainloop()
