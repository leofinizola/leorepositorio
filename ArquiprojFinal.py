# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 03:29:40 2022

@author: Leonardo 
"""
 
from tkinter import *
import os
import sqlite3                    
from tkinter import *             
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from tkPDFViewer import tkPDFViewer as pdf
 
try:
    import tkinter as tk
except ImportError:
    import tkinter as tk
    
try:
    import ttk
    py3 = false
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


 
def registro():
    global registro_tela
    registro_tela = Toplevel(main_tela)
    registro_tela.title("Registro")
    Label(text="").pack()
    registro_tela.geometry("280x250")
 
    global username
    global senha
    global entrada_usuario
    global entrada_senha
    username = StringVar()
    senha = StringVar()

    
    Label(text="").pack()
    Label(registro_tela, text="Entre com os dados", bg="#d9d9d9", fg="blue", width="300", height="2", font=("Arial",13)).pack()
    Label(registro_tela, text="").pack()
    usuario_label = Label(registro_tela, text="Usuário")
    usuario_label.pack()
    entrada_usuario = Entry(registro_tela, textvariable=username)
    entrada_usuario.pack()
    senha_label = Label(registro_tela, text="Senha")
    senha_label.pack()
    entrada_senha = Entry(registro_tela, textvariable=senha, show='*')
    entrada_senha.pack()
    Label(registro_tela, text="").pack()
    Button(registro_tela, text="Registro", width="15", height="2", bg="yellow", command = registro_usuario).pack()
 
  
def login():
    global login_tela
    login_tela = Toplevel(main_tela)
    login_tela.title("Login ArquiProj")
    login_tela.geometry("280x250")
    Label(login_tela, text="Insira login e senha", bg="#d9d9d9", fg="blue", width="300", height="2", font=("Arial",13)).pack()
    Label(login_tela, text="").pack()
 
    global username_verify
    global senha_verify
 
    username_verify = StringVar()
    senha_verify = StringVar()
 
    global username_login_entry
    global senha_login_entry
 
    Label(login_tela, text="Usuário").pack()
    username_login_entry = Entry(login_tela, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_tela, text="").pack()
    Label(login_tela, text="Senha").pack()
    senha_login_entry = Entry(login_tela, textvariable=senha_verify, show= '*')
    senha_login_entry.pack()
    Label(login_tela, text="").pack()
    Button(login_tela, text="Login", width="15", height="2", bg="yellow", command = login_verificacao).pack()
 
 
def registro_usuario():
    global registro_usuario_tela
 
    informacao_usuario = username.get()
    senha_infos = senha.get()
 
    file = open(informacao_usuario, "w")
    file.write(informacao_usuario + "\n")
    file.write(senha_infos)
    file.close()
 
    entrada_usuario.delete(0, END)
    entrada_senha.delete(0, END)
    Label(registro_tela, text="").pack()
    Label(registro_tela, text="Registro concluído - feche a janela", fg="green", font=("arial", 13)).pack()
    Button(registro_usuario_tela, text="OK", command=delete_registro_usuario_tela).pack()
    
 
def login_verificacao():
    username2 = username_verify.get()
    senha2 = senha_verify.get()
    username_login_entry.delete(0, END)
    senha_login_entry.delete(0, END)
 
    list_of_files = os.listdir()
    if username2 in list_of_files:
        file1 = open(username2, "r")
        verify = file1.read().splitlines()
        if senha2 in verify:
            login_sucess()
 
        else:
            senha_nao_reconhecida()
 
    else:
        usuario_nao_encontrado()
 

 
def login_sucess():
    global login_aceito_tela
    login_aceito_tela = Toplevel(login_tela)
    login_aceito_tela.title("Sucesso")
    login_aceito_tela.geometry("280x250")
    Label(login_aceito_tela, text="Login concluído com sucesso").pack()
    Main_Proj()
 
def Main_Proj():
    
    global window
    window = Toplevel(login_aceito_tela)
    window.title("Arquiproj") 
    login_aceito_tela.withdraw()
    login_tela.withdraw()
    main_tela.withdraw()

    class DB:                          
        def __init__(self):           
            self.conn = sqlite3.connect("arqdb.db")  
            self.cur = self.conn.cursor()    
            self.cur.execute(             
                "CREATE TABLE IF NOT EXISTS arqdb (id INTEGER PRIMARY KEY, Nome TEXT, CPF TEXT, Endereco TEXT, Endereco_Interesse TEXT, Nome_Arquiteto TEXT, CREA TEXT, CAU TEXT, ART TEXT, Valor TEXT, Path TEXT)") 
            self.conn.commit()  
    
        def __del__(self):          
            self.conn.close()   
    
        def view(self):         
            self.cur.execute("SELECT * FROM arqdb") 
            rows = self.cur.fetchall()  
            return rows
    
        def insert(self, Nome, CPF, Endereco, Endereco_Int, Nome_Arq, CREA, CAU, ART, Valor, Path):   
            self.cur.execute("INSERT INTO arqdb VALUES (NULL,?,?,?,?,?,?,?,?,?,?)", (Nome, CPF, Endereco, Endereco_Int, Nome_Arq, CREA, CAU, ART, Valor, Path,)) 
            self.conn.commit()
            self.view()
    
        def update(self, id, Nome, CPF, Endereco, Endereco_Int, Nome_Arq, CREA, CAU, ART, Valor, Path):    
            self.cur.execute("UPDATE arqdb SET Nome=?, CPF=?, Endereco=?, Endereco_Interesse=?, Nome_Arquiteto=?, CREA=?, CAU=?, ART=?, Valor=?, Path=? WHERE id=?", (Nome, CPF, Endereco, Endereco_Int, Nome_Arq, CREA, CAU, ART, Valor, Path, id,))
            self.conn.commit()
            self.view()
    
        def delete(self, id):                   
            self.cur.execute("DELETE FROM arqdb WHERE id=?", (id,))
            self.conn.commit()
            self.view()
    
        def search(self, Nome="", CPF="", Endereco="", Endereco_Int="", Nome_Arq="", CREA="", CAU="", ART="", Valor="", Path=""):
            self.cur.execute("SELECT * FROM arqdb WHERE Nome=? OR CPF=? OR Endereco=? OR Endereco_Interesse=? OR Nome_Arquiteto=? OR CREA=? OR CAU=? OR ART=? OR Valor=? OR Path=?" , (Nome, CPF, Endereco, Endereco_Int, Nome_Arq, CREA, CAU, ART, Valor, Path))
            rows = self.cur.fetchall()
            return rows
    
    
    db = DB()  
    
    get_image = ("1",)
    
    def filedialogs():
        global get_image
        e11.delete(0, END)
        get_image = filedialog.askopenfilenames(title="SELECIONE A IMAGEM", filetypes=( ("png", "*.png"), ("jpg" , "*.jpg"), ("Allfile", "*.*")))
        Path = get_image[0]
        path = os.path.basename(Path)
        Entry.insert(e11, 0, path)
    
    
    def showimg():
        try:
            root = Toplevel()
            root.title('Planta')
            root.geometry("500x300")
                
            canvas = Canvas(root, width = 400, height = 400)      
            canvas.grid()
            
            load = Image.open(selected_tuple[10])
            
            resized_image= load.resize((300,300), Image.ANTIALIAS)
            new_image= ImageTk.PhotoImage(resized_image)
            
            canvas.create_image(15,15, anchor=NW, image=new_image)      
        
            root.mainloop()
        except ValueError:
              tkinter.messagebox.showwarning("Warning","Por favor escolha um arquivo JPEG ou PNG")
    
    def showpdf():
        try:
            root_2 = Toplevel()
            root_2.title('Planta')
            root_2.geometry("1200x800")
            pdf.ShowPdf.img_object_li.clear() 
    
            v1 = pdf.ShowPdf()
            v2 = v1.pdf_view(root_2, pdf_location = selected_tuple[10], bar=False, width = 120, height = 120)
            
            v2.grid()
        
            root_2.mainloop()
        except ValueError:
             tkinter.messagebox.showwarning("Atenção","Escolha um arquivo PDF")
             
    
    def get_selected_row(event): 
        global selected_tuple
        index = list1.curselection()[0] 
        selected_tuple = list1.get(index) 
        e1.delete(0, END)                 
        e1.insert(END, selected_tuple[1]) 
        e2.delete(0, END)
        e2.insert(END, selected_tuple[2]) 
        e3.delete(0, END)
        e3.insert(END, selected_tuple[3]) 
        e4.delete(0, END)
        e4.insert(END, selected_tuple[4])
        e5.delete(0, END)
        e5.insert(END, selected_tuple[5]) 
        e6.delete(0, END)                 
        e6.insert(END, selected_tuple[6]) 
        e7.delete(0, END)
        e7.insert(END, selected_tuple[7]) 
        e8.delete(0, END)
        e8.insert(END, selected_tuple[8]) 
        e9.delete(0, END)
        e9.insert(END, selected_tuple[9])
        e10.delete(0, END)
        e10.insert(END, selected_tuple[10]) 
    
    
    
    def view_command():         
        list1.delete(0, END)    
        for row in db.view():   
            list1.insert(END, row)  
    
    
    def search_command(): 
        Path = get_image[0]
        path = os.path.basename(Path)
        list1.delete(0, END)    
        for row in db.search(nome_text.get(), cpf_text.get(), endereco_text.get(), endereco_int_text.get(), nome_arq_text.get(), crea_text.get(), cau_text.get(), art_text.get(), valor_text.get(), path): 
            list1.insert(END, row)
    
    
    def add_command():          
        Path = get_image[0]
        path = os.path.basename(Path)
        db.insert(nome_text.get(), cpf_text.get(), endereco_text.get(), endereco_int_text.get(), nome_arq_text.get(), crea_text.get(), cau_text.get(), art_text.get(), valor_text.get(), path) 
        list1.delete(0, END) 
        list1.insert(END, (nome_text.get(), cpf_text.get(), endereco_text.get(), endereco_int_text.get(), nome_arq_text.get(), crea_text.get(), cau_text.get(), art_text.get(), valor_text.get(), get_image[0]))  
    
    
    def delete_command(): 
        db.delete(selected_tuple[0]) 
    
    
    def update_command():
        Path = get_image[0]
        path = os.path.basename(Path)
        db.update(selected_tuple[0], nome_text.get(), cpf_text.get(), endereco_text.get(), endereco_int_text.get(), nome_arq_text.get(), crea_text.get(), cau_text.get(), art_text.get(), valor_text.get(), path) 
    
    
    window = Tk() 
    
    window.title("Arquiproj") 
    
    
    def on_closing(): 
        dd = db
        if messagebox.askokcancel("ArquiProj", "Você quer sair do Arquiproj?"): 
            window.destroy()
            main_tela.destroy()
            del dd 
    
    window.protocol("WM_DELETE_WINDOW", on_closing)  
    
    l1 = Label(window, text="Nome Completo") 
    l1.grid(row=0, column=0) 
    
    l2 = Label(window, text="CPF")
    l2.grid(row=0, column=2)
    
    l3 = Label(window, text="Endereço")
    l3.grid(row=1, column=0)
    
    l4 = Label(window, text="Endereço Interesse")
    l4.grid(row=1, column=2)
    
    l5 = Label(window, text="Nome Arquiteto")
    l5.grid(row=0, column=4)
    
    l6 = Label(window, text="CREA")
    l6.grid(row=1, column=4)
    
    l7 = Label(window, text="CAU")
    l7.grid(row=0, column=6)
    
    l8 = Label(window, text="ART")
    l8.grid(row=1, column=6)
    
    l9 = Label(window, text="Valor Projeto")
    l9.grid(row=0, column=8)
    
    l10 = Label(window, text="Planta")
    l10.grid(row=1, column=8)
    
    
    nome_text = StringVar()
    e1 = Entry(window, textvariable=nome_text)
    e1.grid(row=0, column=1)
    
    cpf_text = StringVar()
    e2 = Entry(window, textvariable=cpf_text)
    e2.grid(row=0, column=3)
    
    endereco_text = StringVar()
    e3 = Entry(window, textvariable=endereco_text)
    e3.grid(row=1, column=1)
    
    endereco_int_text = StringVar()
    e4 = Entry(window, textvariable=endereco_int_text)
    e4.grid(row=1, column=3)
    
    nome_arq_text = StringVar()
    e5 = Entry(window, textvariable=nome_arq_text)
    e5.grid(row=0, column=5)
    
    crea_text = StringVar()
    e6 = Entry(window, textvariable=crea_text)
    e6.grid(row=1, column=5)
    
    cau_text = StringVar()
    e7 = Entry(window, textvariable=cau_text)
    e7.grid(row=0, column=7)
    
    art_text = StringVar()
    e8 = Entry(window, textvariable=art_text)
    e8.grid(row=1, column=7)
    
    valor_text = StringVar()
    e9 = Entry(window, textvariable=valor_text)
    e9.grid(row=0, column=9)
    
    path_text = get_image[0]
    e10 = Entry(window, textvariable=path_text)
    e10.grid(row=1, column=9)
    
    
    e11 = Entry(window, bd=3, width=17)
    e11.grid(row = 4, column = 9)
    
    
    list1 = Listbox(window, height=30, width=110) 
    list1.grid(row=3, column=0, rowspan=6, columnspan=9) 
    
    sb1 = Scrollbar(window) 
    sb1.grid(row=2, column=8, rowspan=6)
    
    list1.configure(yscrollcommand=sb1.set) 
    sb1.configure(command=list1.yview)
    
    list1.bind('<<ListboxSelect>>', get_selected_row)
    
    b1 = Button(window, text="Visualizar tudo", bg="yellow", width=12, command=view_command) 
    b1.grid(row=3, column=0) 
    
    b2 = Button(window, text="Buscar", bg="yellow", width=12, command=search_command)
    b2.grid(row=4, column=0)
    
    b3 = Button(window, text="Adicionar", bg="yellow", width=12, command=add_command)
    b3.grid(row=5, column=0)
    
    b4 = Button(window, text="Atualizar", bg="yellow", width=12, command=update_command)
    b4.grid(row=6, column=0)
    
    b5 = Button(window, text="Deletar", bg="red", width=12, command=delete_command)
    b5.grid(row=7, column=0)
    
    b6 = Button(window, text="Fechar", bg="yellow", width=12, command=on_closing)
    b6.grid(row=8, column=0)
    
    b7 = Button(window, text="Anexar", bg="yellow", width=10, command=filedialogs)
    b7.grid(row=3, column=9)
    
    b8 = Button(window, text="Abrir imagem", bg="yellow", width=10, command=showimg)
    b8.grid(row=5, column=9)
    
    b9 = Button(window, text="Abrir PDF", bg="yellow", width=10, command=showpdf)
    b9.grid(row=6, column=9)
    
    window.mainloop() 
 
def senha_nao_reconhecida():
    global senha_nao_reconhecida_tela
    senha_nao_reconhecida_tela = Toplevel(login_tela)
    senha_nao_reconhecida_tela.title("ArquiProj")
    senha_nao_reconhecida_tela.geometry("280x250")
    Label(senha_nao_reconhecida_tela, text="Dados incorretos", fg="red").pack()
    Button(senha_nao_reconhecida_tela, text="OK",bg="yellow", command=delete_senha_nao_reconhecida).pack()
 
 
def usuario_nao_encontrado():
    global usuario_nao_encontrado_tela
    usuario_nao_encontrado_tela = Toplevel(login_tela)
    usuario_nao_encontrado_tela.title("ArquiProj")
    Label(text="").pack()
    usuario_nao_encontrado_tela.geometry("200x150")
    Label(text="").pack()
    Label(usuario_nao_encontrado_tela, text="Dados incorretos", fg="red").pack()
    Label(text="").pack()
    Button(usuario_nao_encontrado_tela, text="OK",bg="yellow", command=delete_usuario_nao_encontrado_tela).pack()
 

def delete_login_aceito():
    login_aceito_tela.destroy()
 
 
def delete_senha_nao_reconhecida():
    senha_nao_reconhecida_tela.destroy()
 
 
def delete_usuario_nao_encontrado_tela():
    usuario_nao_encontrado_tela.destroy()
    
def delete_registro_usuario_tela():
    entrada_usuario_tela.destroy()
    
 
def main_account_tela():
    global main_tela
    main_tela = Tk()
    main_tela.geometry("280x250")
    main_tela.title("ArquiProj")
    Label(text="").pack()
    Label(text="Bem vindo ao Arquiproj", bg="#d9d9d9", fg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", bg="yellow", command = login).pack()
    Label(text="").pack()
    Button(text="Registro", height="2", width="30",bg="yellow", command=registro).pack()
 
    main_tela.mainloop()
 
 
main_account_tela()


