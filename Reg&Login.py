# Import libraries
from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3

# Create a TKingter Window
root = Tk()
root.title("Python: Simple Inventory System")
 
width = 640
height = 480
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)

# I don't understand what the %d part does*****************************************************

root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(True, True)

# Create the DB variable and open SQL connection
def Database():
    global conn, cursor
    conn = sqlite3.connect("casino.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member`\
    (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
    username TEXT, password TEXT, email TEXT, balance INTEGER)")
    

#=======================================VARIABLES=====================================
USERNAME = StringVar()
PASSWORD = StringVar()
EMAIL = StringVar()
BALANCE = StringVar()

# Create Tkinter login form

def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root)
    LoginFrame.pack(side=TOP, pady=80)
    lbl_username = Label(LoginFrame, text="Username:", font=('arial', 25), bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(LoginFrame, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=2)
    lbl_result1 = Label(LoginFrame, text="", font=('arial', 18))
    lbl_result1.grid(row=3, columnspan=2)
    username = Entry(LoginFrame, font=('arial', 20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    password = Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=35, command=Login)
    btn_login.grid(row=4, columnspan=2, pady=20)
    lbl_register = Label(LoginFrame, text="Register", fg="Blue", font=('arial', 12))
    lbl_register.grid(row=0, sticky=W)
    lbl_register.bind('<Button-1>', ToggleToRegister)

# Create Tkinter Register form

def RegisterForm():
    global RegisterFrame, lbl_result2
    RegisterFrame = Frame(root)
    RegisterFrame.pack(side=TOP, pady=40)
    lbl_username = Label(RegisterFrame, text="Username:", font=('arial', 18), bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(RegisterFrame, text="Password:", font=('arial', 18), bd=18)
    lbl_password.grid(row=2)
    lbl_email = Label(RegisterFrame, text="Email:", font=('arial', 18), bd=18)
    lbl_email.grid(row=3)
    lbl_balance = Label(RegisterFrame, text="Balance:", font=('arial', 18), bd=18)
    lbl_balance.grid(row=4)
    lbl_result2 = Label(RegisterFrame, text="", font=('arial', 18))
    lbl_result2.grid(row=5, columnspan=2)
    username = Entry(RegisterFrame, font=('arial', 20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    password = Entry(RegisterFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    email = Entry(RegisterFrame, font=('arial', 20), textvariable=EMAIL, width=15)
    email.grid(row=3, column=1)
    balance = Entry(RegisterFrame, font=('arial', 20), textvariable=BALANCE, width=15)
    balance.grid(row=4, column=1)
    btn_login = Button(RegisterFrame, text="Register", font=('arial', 18), width=35, command=Register)
    btn_login.grid(row=6, columnspan=2, pady=20)
    lbl_login = Label(RegisterFrame, text="Login", fg="Blue", font=('arial', 12))
    lbl_login.grid(row=0, sticky=W)
    lbl_login.bind('<Button-1>', ToggleToLogin)
    

# Define Tkinter buttons

def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()
 
def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()
 
def ToggleToRegister(event=None):
    LoginFrame.destroy()
    RegisterForm()

# Define Register button and if/else statement for empty field and used username

def Register():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "" or EMAIL.get() == "" or BALANCE.get == "":
        lbl_result2.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (USERNAME.get(),))
        if cursor.fetchone() is not None:
            lbl_result2.config(text="Username is already taken", fg="red")
        else:
            cursor.execute("INSERT INTO `member` (username, password, email, balance) VALUES(?, ?, ?, ?)",\
                           (str(USERNAME.get()), str(PASSWORD.get()), str(EMAIL.get()), str(BALANCE.get())))
            conn.commit()
            USERNAME.set("")
            PASSWORD.set("")
            EMAIL.set("")
            BALANCE.set("")
            lbl_result2.config(text="Successfully Created!", fg="black")
        cursor.close()
        conn.close()

# Define login, if field is blank, and chck SQL for username and password

# I don't understand why it doesn't work if you use username#1 and password#2*****************************

def Login():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            lbl_result1.config(text="You Successfully Login", fg="blue")
        else:
            lbl_result1.config(text="Invalid Username or password", fg="red")
            
# Initialize the program

LoginForm()

# Tkinter menubar

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)
