#import modules
 
from tkinter import *
import os
import sqlite3                    #importing module for performing SQL operations.
from tkinter import *             #importing module for creating GUI
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
from tkPDFViewer import tkPDFViewer as pdf
 
# Designing window for registration


 
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Registro")
    register_screen.geometry("400x300")
 
    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()
 
    Label(register_screen, text="Por favor entre com os detalhes abaixo", bg="cyan").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Usuário")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Senha")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Registro", width=15, height=3, bg="green", command = register_user).pack()
 
 
# Designing window for login 
 
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("400x300")
    Label(login_screen, text="Por favor ponha as informações abaixo").pack()
    Label(login_screen, text="").pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(login_screen, text="Usuário").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Senha").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()
 
# Implementing event on register button
 
def register_user():
 
    username_infos = username.get()
    password_infos = password.get()
 
    file = open(username_infos, "w")
    file.write(username_infos + "\n")
    file.write(password_infos)
    file.close()
 
    username_entry.delete(0, END)
    password_entry.delete(0, END)
 
    Label(register_screen, text="Registro completado", fg="green", font=("calibri", 13)).pack()
 
# Implementing event on login button 
 
def login_verify():
    username2 = username_verify.get()
    password2 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
 
    list_of_files = os.listdir()
    if username2 in list_of_files:
        file1 = open(username2, "r")
        verify = file1.read().splitlines()
        if password2 in verify:
            login_sucess()
 
        else:
            password_not_recognised()
 
    else:
        user_not_found()
 
# Designing popup for login success
 
def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Sucesso")
    login_success_screen.geometry("200x150")
    Label(login_success_screen, text="Login completado com sucesso").pack()
    #Button(login_success_screen, text="OK", command=delete_login_success).pack()
    Main_Proj()
 
def Main_Proj():
    
    global window
    window = Toplevel(login_success_screen)
    window.title("Arquiproj") #setting title of the window
    login_success_screen.withdraw()
    login_screen.withdraw()
    main_screen.withdraw()

    class DB:                         #creating a class DB with functions to perform various operations on the database. 
        def __init__(self):           #constructor functor for class DB.
            self.conn = sqlite3.connect("arqdb.db")  #connects to a database called arqproj.db
            self.cur = self.conn.cursor()    #creating a cursor to navigate through the database
            self.cur.execute(             
                "CREATE TABLE IF NOT EXISTS arqdb (id INTEGER PRIMARY KEY, Nome TEXT, CPF TEXT, Endereco TEXT, Endereco_Interesse TEXT, Nome_Arquiteto TEXT, CREA TEXT, CAU TEXT, ART TEXT, Valor TEXT, Path TEXT)") #creating a table called book with id, title, author and isbn as columns.
            self.conn.commit()  #commit functions saves everything to the database
    
        def __del__(self):          #destructor created for the class DB
            self.conn.close()   #closes the connection with the database
    
        def view(self):         #To view all the rows present in the table
            self.cur.execute("SELECT * FROM arqdb") #Execute function is to perform the SQL operations. Here, it produces all the rows from the table.
            rows = self.cur.fetchall()  #fetching all the rows one by one from the table and storing it in list rows
            return rows
    
        def insert(self, Nome, CPF, Endereco, Endereco_Int, Nome_Arq, CREA, CAU, ART, Valor, Path):  #inserting a new row in the table. 
            self.cur.execute("INSERT INTO arqdb VALUES (NULL,?,?,?,?,?,?,?,?,?,?)", (Nome, CPF, Endereco, Endereco_Int, Nome_Arq, CREA, CAU, ART, Valor, Path,)) #passing values to the function to store them in the columns
            self.conn.commit()
            self.view()
    
        def update(self, id, Nome, CPF, Endereco, Endereco_Int, Nome_Arq, CREA, CAU, ART, Valor, Path):    #to update the values of the selected row with the values passed by the user
            self.cur.execute("UPDATE arqdb SET Nome=?, CPF=?, Endereco=?, Endereco_Interesse=?, Nome_Arquiteto=?, CREA=?, CAU=?, ART=?, Valor=?, Path=? WHERE id=?", (Nome, CPF, Endereco, Endereco_Int, Nome_Arq, CREA, CAU, ART, Valor, Path, id,))
            self.conn.commit()
            self.view()
    
        def delete(self, id):                   #to delete the row from the table given the value of the id of the selected row.
            self.cur.execute("DELETE FROM arqdb WHERE id=?", (id,))
            self.conn.commit()
            self.view()
    
        def search(self, Nome="", CPF="", Endereco="", Endereco_Int="", Nome_Arq="", CREA="", CAU="", ART="", Valor="", Path=""):
            self.cur.execute("SELECT * FROM arqdb WHERE Nome=? OR CPF=? OR Endereco=? OR Endereco_Interesse=? OR Nome_Arquiteto=? OR CREA=? OR CAU=? OR ART=? OR Valor=? OR Path=?" , (Nome, CPF, Endereco, Endereco_Int, Nome_Arq, CREA, CAU, ART, Valor, Path))
            rows = self.cur.fetchall()
            return rows
    
    
    db = DB()  #created an object of the class DB.
    
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
            pdf.ShowPdf.img_object_li.clear() # clear loaded pages
    
            v1 = pdf.ShowPdf()
            v2 = v1.pdf_view(root_2, pdf_location = selected_tuple[10], bar=False, width = 120, height = 120)
            
            v2.grid()
        
            root_2.mainloop()
        except ValueError:
             tkinter.messagebox.showwarning("Warning","Por favor escolha um arquivo PDF")
             
    
    def get_selected_row(event): #selecting a particular row or multiple rows
        global selected_tuple
        index = list1.curselection()[0] #this is the id of the selected tuple
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
    
    
    
    def view_command():         #to print all the rows of the table using view function of the class DB on to the screen 
        list1.delete(0, END)    #empty the list
        for row in db.view():   
            list1.insert(END, row)  #keeps on inserting each row into the list
    
    
    def search_command(): 
        Path = get_image[0]
        path = os.path.basename(Path)
        list1.delete(0, END)    #empty the list
        for row in db.search(nome_text.get(), cpf_text.get(), endereco_text.get(), endereco_int_text.get(), nome_arq_text.get(), crea_text.get(), cau_text.get(), art_text.get(), valor_text.get(), path): #get the name of the title or the author and pass it to the search function of class DB
            list1.insert(END, row)
    
    
    def add_command():          #to add a new row into the table
        Path = get_image[0]
        path = os.path.basename(Path)
        db.insert(nome_text.get(), cpf_text.get(), endereco_text.get(), endereco_int_text.get(), nome_arq_text.get(), crea_text.get(), cau_text.get(), art_text.get(), valor_text.get(), path) #passing user input values 
        list1.delete(0, END) #empty the list
        list1.insert(END, (nome_text.get(), cpf_text.get(), endereco_text.get(), endereco_int_text.get(), nome_arq_text.get(), crea_text.get(), cau_text.get(), art_text.get(), valor_text.get(), get_image[0]))  #insert into the list and then the table, the values given by the user
    
    
    def delete_command(): #deleting a row 
        db.delete(selected_tuple[0]) #calls the delete function of the class DB and passes the id as the parameter and condition
    
    
    def update_command():
        Path = get_image[0]
        path = os.path.basename(Path)
        db.update(selected_tuple[0], nome_text.get(), cpf_text.get(), endereco_text.get(), endereco_int_text.get(), nome_arq_text.get(), crea_text.get(), cau_text.get(), art_text.get(), valor_text.get(), path) #calls the update function of the class DB and passes the user input as parameters to update value of the row
    
    
    window = Tk() #using Tkinter module, create a GUI window
    
    window.title("Arquiproj") #setting title of the window
    
    
    def on_closing(): #destructor for the window
        dd = db
        if messagebox.askokcancel("Quit", "Você quer sair do Arquiproj?"): #when ok is clicked, displays the following message
            window.destroy()
            main_screen.destroy()
            del dd #deletes the object once window has been closed
    
    window.protocol("WM_DELETE_WINDOW", on_closing)  # handles window closing
    
    l1 = Label(window, text="Nome Completo") #creating input labels in the window
    l1.grid(row=0, column=0) #determining size of the input grid for these labels
    
    l2 = Label(window, text="CPF")
    l2.grid(row=0, column=2)
    
    l3 = Label(window, text="Endereco")
    l3.grid(row=1, column=0)
    
    l4 = Label(window, text="Endereco Interesse")
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
    
    
    list1 = Listbox(window, height=30, width=110) #creating the list space to display all the rows of the table
    list1.grid(row=3, column=0, rowspan=6, columnspan=9) #determining the size
    
    sb1 = Scrollbar(window) #creating a scrollbar for the window to scroll through the list entries
    sb1.grid(row=2, column=8, rowspan=6)
    
    list1.configure(yscrollcommand=sb1.set) #configuring the scroll function for the scrollbar object sb1
    sb1.configure(command=list1.yview)
    
    list1.bind('<<ListboxSelect>>', get_selected_row)
    
    b1 = Button(window, text="Visualizar tudo", width=12, command=view_command) #creating buttons for the various operations. Giving it a name and assigning a particular command to it. 
    b1.grid(row=3, column=0) #size of the button
    
    b2 = Button(window, text="Buscar", width=12, command=search_command)
    b2.grid(row=4, column=0)
    
    b3 = Button(window, text="Adicionar", width=12, command=add_command)
    b3.grid(row=5, column=0)
    
    b4 = Button(window, text="Atualizar", width=12, command=update_command)
    b4.grid(row=6, column=0)
    
    b5 = Button(window, text="Deletar", width=12, command=delete_command)
    b5.grid(row=7, column=0)
    
    b6 = Button(window, text="Fechar", width=12, command=on_closing)
    b6.grid(row=8, column=0)
    
    b7 = Button(window, text="Anexar", width=10, command=filedialogs)
    b7.grid(row=3, column=9)
    
    b8 = Button(window, text="Abrir imagem", width=10, command=showimg)
    b8.grid(row=5, column=9)
    
    b9 = Button(window, text="Abrir PDF", width=10, command=showpdf)
    b9.grid(row=6, column=9)
    
    window.mainloop() #carry the functioning of the GUI window on a loop until it is closed using the destructor
    # Designing popup for login invalid password
 
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Sucesso")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Usuário não encontrado, tente novamente").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()
 
# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Sucesso")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="Usuário não encontrado, tente novamente").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
 
# Deleting popups
 
def delete_login_success():
    login_success_screen.destroy()
 
 
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
 
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy()
 
 
# Designing Main(first) window
 
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Login")
    Label(text="Bem vindo ao Arquiproj", bg="cyan", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = login).pack()
    Label(text="").pack()
    Button(text="Registro", height="2", width="30", command=register).pack()
 
    main_screen.mainloop()
 
 
main_account_screen()

