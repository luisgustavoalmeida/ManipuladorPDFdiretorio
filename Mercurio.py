import tkinter
from tkinter import *
import tkinter.scrolledtext as st

import VerificadorNomes as vn
import Mover



win = Tk()
win.title('Mercurios')

# Set the size of the tkinter window
largura_tela_w = win.winfo_screenwidth()
janela_largura = 400
janela_altura = 800
posicao_horizontal = int((largura_tela_w / 2) - (janela_largura / 2))
posicao_vertical = 15


win.geometry("%dx%d+%d+%d" % (janela_largura, janela_altura, posicao_horizontal, posicao_vertical))
win.resizable(True,True)
#photo = PhotoImage(file="asa.ico")
#win.wm_iconbitmap(photo) # descomentarqundocolocar exe

# Create a Frame
frame = Frame(win)
frame.pack(pady=3)
TextoLabel_4 = StringVar()
TextoLabel_1 = StringVar()

label_1 = Label(win,text="Renomeia os arquivos do tipo .pdf que se encontram em Download",bd='3')

label_1_1 = Label(win,textvariable= TextoLabel_1, anchor="w", width= 50,bd='3')

label_2 = Label(win,text="Move os arquivos renomeados para o diretório expecífico ",bd='3')

label_4 = Label(win,textvariable= TextoLabel_4, anchor="w", width= 50,bd='3')

#def f_label_1():
    #TextoLabel_1.set("Arquivo renomeados: " + str(vn.identificar_caderno()))

def f_label_3():
    TextoLabel_4.set("Arquivo movidos: " + str(len(Mover.lista_movidos)))

    cont = 0
    for i in Mover.lista_movidos:
        lista_log.insert(END, cont, i)

        cont += 1

btn_1 = Button(win, text='Renomear', bd='3', width= 50, command= lambda: [vn.identificar_caderno(vn.selecao_caminho())])

btn_2 = Button(win, text='Mover', bd='3', width= 50, command= lambda: [Mover.mover(),f_label_3()])


lista_log = tkinter.Listbox(win)
scrollbar = Scrollbar(lista_log)
scrollbar.pack(side = RIGHT, fill = BOTH)
lista_log.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = lista_log.yview)

label_1.pack(fill='x')
btn_1.pack(fill='x')
label_1_1.pack(fill='x')
label_2.pack(fill='x')
btn_2.pack(fill='x')
label_4.pack(fill='x')
lista_log.pack(side =tkinter.TOP, fill=tkinter.BOTH, expand=True)
win.update()


win.mainloop()
