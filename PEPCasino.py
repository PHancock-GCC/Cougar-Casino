"""Author: Paul Hancock, Casino v1.2
This program creates a text box based casino which can play Craps,
Blackjack, and Roulette. It uses a SQL database to allow registration,
login, and deposit."""

#Import required libraries
import random
from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3


# If sql is not yet supported, download from https://sqlitebrowser.org/dl/

# Create a TKinter Window
"""Create a resizable Tkinter window"""
root = Tk()
root.title("Python: Simple Inventory System")

width = 640
height = 480
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(True, True)


# Create the DB variable and open SQL connection
def database():
    """Creates a SQL database and links to it"""
    global CONN, cursor
    CONN = sqlite3.connect("casino.db")
    cursor = CONN.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS `member`
                      (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                      username TEXT, password TEXT, email TEXT, balance INTEGER)""")


# ==============================VARIABLES==============================
USERNAME = StringVar()
PASSWORD = StringVar()
EMAIL = StringVar()
BALANCE = StringVar()

# Create Tkinter login form
def login_form():
    """Define the frame, buttons, and labels of the login form"""
    global LOGINFRAME, LBL_RESULT1
    LOGINFRAME = Frame(root)
    LOGINFRAME.pack(side=TOP, pady=80)
    lbl_username = Label(
        LOGINFRAME,
        text="Username:",
        font=(
            'arial',
            25),
        bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(
        LOGINFRAME,
        text="Password:",
        font=(
            'arial',
            25),
        bd=18)
    lbl_password.grid(row=2)
    LBL_RESULT1 = Label(LOGINFRAME, text="", font=('arial', 18))
    LBL_RESULT1.grid(row=3, columnspan=2)
    entry_username = Entry(
        LOGINFRAME,
        font=(
            'arial',
            20),
        textvariable=USERNAME,
        width=15)
    entry_username.grid(row=1, column=1)
    entry_password = Entry(
        LOGINFRAME,
        font=(
            'arial',
            20),
        textvariable=PASSWORD,
        width=15,
        show="*")
    entry_password.grid(row=2, column=1)
    btn_login = Button(
        LOGINFRAME,
        text="Login",
        font=(
            'arial',
            18),
        width=35,
        command=login)
    btn_login.grid(row=4, columnspan=2, pady=20)
    lbl_register = Label(
        LOGINFRAME,
        text="Register",
        fg="Blue",
        font=(
            'arial',
            12))
    lbl_register.grid(row=0, sticky=W)
    lbl_register.bind('<Button-1>', toggle_to_register)


def login():
    pass


def toggle_to_register(event=None):
    pass

# Create Tkinter Register form


def register_form():
    """Define the frame, buttons, and labels of the register form """
    global REGISTERFRAME, LBL_RESULT2
    REGISTERFRAME = Frame(root)
    REGISTERFRAME.pack(side=TOP, pady=40)
    lbl_username = Label(
        REGISTERFRAME,
        text="Username:",
        font=(
            'arial',
            18),
        bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(
        REGISTERFRAME,
        text="Password:",
        font=(
            'arial',
            18),
        bd=18)
    lbl_password.grid(row=2)
    lbl_email = Label(REGISTERFRAME, text="Email:", font=('arial', 18), bd=18)
    lbl_email.grid(row=3)
    lbl_balance = Label(
        REGISTERFRAME,
        text="Balance:",
        font=(
            'arial',
            18),
        bd=18)
    lbl_balance.grid(row=4)
    LBL_RESULT2 = Label(REGISTERFRAME, text="", font=('arial', 18))
    LBL_RESULT2.grid(row=5, columnspan=2)
    username = Entry(
        REGISTERFRAME,
        font=(
            'arial',
            20),
        textvariable=USERNAME,
        width=15)
    username.grid(row=1, column=1)
    password = Entry(
        REGISTERFRAME,
        font=(
            'arial',
            20),
        textvariable=PASSWORD,
        width=15,
        show="*")
    password.grid(row=2, column=1)
    email = Entry(
        REGISTERFRAME,
        font=(
            'arial',
            20),
        textvariable=EMAIL,
        width=15)
    email.grid(row=3, column=1)
    balance = Entry(
        REGISTERFRAME,
        font=(
            'arial',
            20),
        textvariable=BALANCE,
        width=15)
    balance.grid(row=4, column=1)
    btn_register = Button(
        REGISTERFRAME,
        text="Register",
        font=(
            'arial',
            18),
        width=35,
        command=register)
    btn_register.grid(row=6, columnspan=2, pady=20)
    lbl_login = Label(
        REGISTERFRAME,
        text="Login",
        fg="blue",
        font=(
            'arial',
            12))
    lbl_login.grid(row=0, sticky=W)
    lbl_login.bind('<Button-1>', toggle_to_login)


# ------------------------- HomeScreen -------------------------
def home_screen():
    """Define the frame, buttons, and labels of the homescreen"""
    global HOMESCREENFRAME, LBL_RESULT2
    HOMESCREENFRAME = Frame(root)
    HOMESCREENFRAME.pack(side=TOP, pady=40)

    lbl_welcome = Label(
        HOMESCREENFRAME,
        text="Welcome: ",
        font=(
            'arial',
            18),
        bd=18)
    lbl_welcome.grid(column=0, row=0)
    lbl_balance = Label(
        HOMESCREENFRAME,
        text="Balance:",
        font=(
            'arial',
            18),
        bd=18)
    lbl_balance.grid(column=1, row=0)
    lbl_add = Label(
        HOMESCREENFRAME,
        text="Deposit:",
        font=(
            'arial',
            18),
        bd=18)
    lbl_add.grid(column=2, row=0)
    lbl_withdraw = Label(
        HOMESCREENFRAME,
        text="Logout:",
        font=(
            'arial',
            18),
        bd=18)
    lbl_withdraw.grid(column=3, row=0)
    lbl_logout = Label(
        HOMESCREENFRAME,
        text="Withdraw:",
        font=(
            'arial',
            18),
        bd=18)
    lbl_logout.grid(column=4, row=0)

    lbl_username = Label(
        HOMESCREENFRAME,
        text="BlackJack:",
        font=(
            'arial',
            18),
        bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(
        HOMESCREENFRAME,
        text="Craps:",
        font=(
            'arial',
            18),
        bd=18)
    lbl_password.grid(row=2)

    LBL_RESULT2 = Label(HOMESCREENFRAME, text="", font=('arial', 18))
    LBL_RESULT2.grid(row=5, columnspan=2)
    username = Entry(
        HOMESCREENFRAME,
        font=(
            'arial',
            20),
        textvariable=USERNAME,
        width=15)
    username.grid(row=1, column=1)
    password = Entry(
        HOMESCREENFRAME,
        font=(
            'arial',
            20),
        textvariable=PASSWORD,
        width=15,
        show="*")
    password.grid(row=2, column=1)
    email = Entry(
        HOMESCREENFRAME,
        font=(
            'arial',
            20),
        textvariable=EMAIL,
        width=15)
    email.grid(row=3, column=1)
    balance = Entry(
        HOMESCREENFRAME,
        font=(
            'arial',
            20),
        textvariable=BALANCE,
        width=15)
    balance.grid(row=4, column=1)
    btn_login = Button(
        HOMESCREENFRAME,
        text="Register",
        font=(
            'arial',
            18),
        width=35,
        command=register)
    btn_login.grid(row=6, columnspan=2, pady=20)
    lbl_login = Label(
        HOMESCREENFRAME,
        text="Login",
        fg="blue",
        font=(
            'arial',
            12))
    lbl_login.grid(row=0, sticky=W)
    lbl_login.bind('<Button-1>', toggle_to_login)


# Define Tkinter buttons
def exit_program():
    """Add a dropdown to exit the program"""
    result = tkMessageBox.askquestion(
        'System',
        'Are you sure you want to exit?',
        icon="warning")
    if result == 'yes':
        root.destroy()
        exit()


def toggle_to_login(event=None):
    """Close the register frame and open the login frame"""
    REGISTERFRAME.destroy()
    login_form()


def toggle_to_register(event=None):
    """Close the login frmae and open the registration frame"""
    LOGINFRAME.destroy()
    register_form()


def toggle_to_home_screen(event=None):
    """Close the login frmae and open the homescreen"""
    LOGINFRAME.destroy()
    home_screen()

    # Define Register button and if/else statement for empty field and
    # used username


def register():
    """Check to see user is already in the database. If not continue to
       register the user in the database."""
    database()
    if USERNAME.get() == "" or PASSWORD.get(
    ) == "" or EMAIL.get() == "" or BALANCE.get() == "":
        LBL_RESULT2.config(
            text="Please complete the required field!",
            fg="orange")
    else:
        cursor.execute(
            "SELECT * FROM `member` WHERE `username` = ?", (USERNAME.get(),))
        if cursor.fetchone() is not None:
            LBL_RESULT2.config(text="Username is already taken", fg="red")
        else:
            cursor.execute(
                "INSERT INTO `member` (username, password, email, balance) VALUES(?, ?, ?, ?)", (str(
                    USERNAME.get()), str(
                    PASSWORD.get()), str(
                    EMAIL.get()), str(
                    BALANCE.get())))
            CONN.commit()
            USERNAME.set("")
            PASSWORD.set("")
            EMAIL.set("")
            BALANCE.set("")
            LBL_RESULT2.config(text="Successfully Created!", fg="black")
        cursor.close()
        CONN.close()

# Define login, if field is blank, and check SQL for username and password


def login():
    """Return an error if field is blank. If username and PW are correct
       display login message. If incorrect display error message"""
    database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        LBL_RESULT1.config(
            text="Please complete the required field!",
            fg="orange")
    else:
        cursor.execute(
            "SELECT * FROM `member` WHERE `username` = ? and `password` = ?",
            (USERNAME.get(),
             PASSWORD.get()))
        if cursor.fetchone() is not None:
            LBL_RESULT1.config(text="You Successfully Login", fg="blue")
            toggle_to_home_screen()
        else:
            LBL_RESULT1.config(text="Invalid Username or password", fg="red")


# Initialize the program
login_form()

# Tkinter menubar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)


# ----------------BlackJack------------------------------------

SUITS = ['hearts', 'diamonds', 'spades', 'clubs']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALUES = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10,
    'A': 11}


class Card:
    """Define a card as an object with a self, suit, and rank"""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    """Define a deck as an object with cards"""
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        """Define the cards in the deck"""
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp

    def shuffle(self):
        """Pick a random card from the deck"""
        random.shuffle(self.deck)

    def deal(self):
        """Pop the chosen card out of the deck"""
        return self.deck.pop()


class Hand:
    """Define a hand"""
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        """Add card"""
        self.cards.append(card)
        self.value += VALUES[card.rank]
        if card.rank == 'A':
            self.aces += 1

    def adjust_for_ace(self):
        """Give aces variable value"""
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Game:
    """Define game as an object with a deck, hand, player and dealer"""
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()

        self.player = Hand()
        self.dealer = Hand()

        self.player.add_card(self.deck.deal())
        self.player.add_card(self.deck.deal())

        self.dealer.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())

    def play(self):
        """Continue game until a bust or stand"""
        game_over = False

        while not game_over:
            print("\nPlayer's hand is: ", *self.player.cards, sep='\n ')
            print("Player's hand value: ", self.player.value)

            player_choice = input("Would you like to hit or stand? ").lower()
            if player_choice == 'hit':
                self.player.add_card(self.deck.deal())

                if self.player.value > 21:
                    print("Player busts!")
                    game_over = True

            else:
                game_over = True

        if self.player.value <= 21:
            while self.dealer.value < 17:
                self.dealer.add_card(self.deck.deal())
        if self.dealer.value > 21:
            print("Dealer busts!")
        elif self.dealer.value > self.player.value:
            print("Dealer wins!")
        elif self.dealer.value < self.player.value:
            print("Player wins!")
        else:
            print("It's a tie!")


a = Game()
a.play()


# Create Tkinter Deposit form
def deposit_money():
    """Create a frame, buttons, and labels for deposit frame"""
    global DEPOSITFRAME, BALANCE
    DEPOSITFRAME = Frame(root)
    DEPOSITFRAME.pack(side=TOP, pady=40)
    lbl_balance = Label(
        DEPOSITFRAME,
        text="Balance:",
        font=(
            'arial',
            18),
        bd=18)
    lbl_balance.grid(row=0)
    balance = Label(
        DEPOSITFRAME,
        text=BALANCE.get(),
        font=(
            'arial',
            18),
        bd=18)
    balance.grid(row=0, column=1)
    lbl_deposit = Label(
        DEPOSITFRAME,
        text="Deposit Amount:",
        font=(
            'arial',
            18),
        bd=18)
    lbl_deposit.grid(row=1)
    deposit = Entry(DEPOSITFRAME, font=('arial', 20), width=15)
    deposit.grid(row=1, column=1)
    btn_deposit = Button(
        DEPOSITFRAME, text="Deposit", font=(
            'arial', 18), width=35, command=lambda: deposit(
            deposit.get()))
    btn_deposit.grid(row=2, columnspan=2, pady=20)

# Deposit function


def deposit(amount):
    """Deposit funds into the balance of database"""
    global BALANCE
    try:
        amount = int(amount)
    except BaseException:
        tkMessageBox.showerror(
            "Invalid Input",
            "Deposit amount must be an integer.")
        return
    new_balance = int(BALANCE.get()) + amount
    cursor.execute(
        "UPDATE member SET balance=? WHERE mem_id=?", (new_balance, 1))
    CONN.commit()
    BALANCE.set(new_balance)
    tkMessageBox.showinfo("Success", "Deposit successful.")

# Logout function


def logout():
    """Leave the game and close the frame"""
    global HOMESCREENFRAME
    HOMESCREENFRAME.destroy()
    login_form()
