"""Author: Paul Hancock, Casino v1.2
This program creates a text box based casino which can play Craps,
Blackjack, and Roulette. It uses a SQL database to allow registration,
login, and deposit."""

#Import required libraries
import random
import string
from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import re
from functools import partial


# If sql is not yet supported, download from https://sqlitebrowser.org/dl/

"""Create a resizable Tkinter window"""
root = Tk()
root.title("Cougar Casino")

width = 640
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(True, True)

# ==============================VARIABLES==============================
USERNAME = StringVar()
PASSWORD = StringVar()
EMAIL = StringVar()
BALANCE = StringVar()
UPDATEPASSWORD = StringVar()
UPDATEDEPOSIT = StringVar()
BET = IntVar()
ROULETTECHOICE = StringVar()
BLACKJACKCHOICE = StringVar()
MYOPTION = ""

# Create the DB variable and open SQL connection
def database():
    """Creates a SQL database and links to it"""
    global CONN, cursor
    CONN = sqlite3.connect("casino.db")
    cursor = CONN.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS `member`
                      (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                      username TEXT, password TEXT, email TEXT, balance INTEGER)""")


# Create Tkinter login form
def login_form():
    """Define the frame, buttons, and labels of the login form"""
    global LOGINFRAME, LBL_RESULT1
    LOGINFRAME = Frame(root)
    LOGINFRAME.pack(side=TOP, pady=80)
    
    lbl_username = Label(LOGINFRAME,text="Username:", font=('arial',25), bd=18)
    lbl_username.grid(row=1)
    
    lbl_password = Label(LOGINFRAME, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=2)
    
    LBL_RESULT1 = Label(LOGINFRAME, text="", font=('arial', 18))
    LBL_RESULT1.grid(row=3, columnspan=2)
    
    entry_username = Entry(LOGINFRAME, font=('arial', 20), textvariable=USERNAME, width=15)
    entry_username.grid(row=1, column=1)
    
    entry_password = Entry(LOGINFRAME,font=('arial',20),textvariable=PASSWORD,width=15,show="*")
    entry_password.grid(row=2, column=1)
    
    btn_login = Button(LOGINFRAME,text="Login",font=('arial',18),width=29,command=login)
    btn_login.grid(row=4, columnspan=2, pady=20, padx=(28, 0))
    
    lbl_register = Label(LOGINFRAME, text="Register", fg="Blue", font=('arial',12))
    lbl_register.grid(row=0, sticky=W, padx=(25,0))
    
    lbl_register.bind('<Button-1>', toggle_to_register)


""" Create Tkinter Register form"""

def register_form():
    """Define the frame, buttons, and labels of the register form """
    global REGISTERFRAME, LBL_RESULT2, password
    REGISTERFRAME = Frame(root)
    REGISTERFRAME.pack(side=TOP, pady=40)
    
    lbl_username = Label( REGISTERFRAME, text="Username:", font=( 'arial', 18), bd=18)
    lbl_username.grid(row=1, sticky="w")
    
    lbl_password = Label(REGISTERFRAME,text="Password:",font=('arial',18), bd=18)
    lbl_password.grid(row=2, sticky="w")
    
    lbl_email = Label(REGISTERFRAME, text="Email:", font=('arial', 18), bd=18)
    lbl_email.grid(row=3, sticky="w")
    
    LBL_BALANCE = Label(REGISTERFRAME, text="Balance:", font=('arial', 18), bd=18)
    LBL_BALANCE.grid(row=4, sticky="w")
    
    LBL_RESULT2 = Label(REGISTERFRAME, text="", font=('arial', 18))
    LBL_RESULT2.grid(row=5, columnspan=2)
    
    username = Entry(REGISTERFRAME, font=('arial',20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    
    password = Entry(REGISTERFRAME,font=('arial',20),textvariable=PASSWORD,width=15,show="*")
    password.grid(row=2, column=1)
    
    email = Entry(REGISTERFRAME, font=('arial', 20), textvariable=EMAIL, width=15)
    email.grid(row=3, column=1)
    
    balance = Entry(REGISTERFRAME,font=('arial',20),textvariable=BALANCE,width=15)
    balance.grid(row=4, column=1)
    
    btn_passgen = Button(REGISTERFRAME, text="Generate Password", font=('arial', 18), width=35,command=partial(passgen, "register"))
    btn_passgen.grid(row=6, columnspan=2)
    
    btn_register = Button( REGISTERFRAME, text="Register", font=('arial', 18), width=35, command=register)
    btn_register.grid(row=7, columnspan=2)
    
    lbl_login = Label(REGISTERFRAME, text="Login", fg="blue", font=( 'arial', 12))
    lbl_login.grid(row=0, sticky=W, padx=(18, 0))
    
    lbl_login.bind('<Button-1>', toggle_to_login)


# ------------------------- HomeScreen -------------------------
def home_screen():
    """Define the frame, buttons, and labels of the homescreen"""
    global HOMESCREENFRAME, LBL_RESULT2, LBL_BALANCE
    HOMESCREENFRAME = Frame(root)
    HOMESCREENFRAME.pack(side=TOP, pady=(20,0))

    lbl_welcome = Label(HOMESCREENFRAME,text=("Welcome\n" + USERNAME.get()),font=('arial',18),bd=18)
    lbl_welcome.grid(column=0, row=0)
    
    LBL_BALANCE = Label(HOMESCREENFRAME,text=("Balance\n$" + BALANCE.get()),font=('arial',18),bd=18)
    LBL_BALANCE.grid(column=1, row=0)

    button_out = Button(HOMESCREENFRAME,text="Logout",font=('arial',12),bd=5, command=exit_program)
    button_out.grid(column=2, row=0)
    
    lbl_choose = Label(HOMESCREENFRAME,text=("Pick a game:"),font=('arial',18),bd=18)
    lbl_choose.grid(column=0, row=1, pady= (50,0), columnspan=3)
    
    button_black_jack = Button(HOMESCREENFRAME,text="BlackJack",font=('arial',18),bd=10, width=11, command = open_blackjack_window)
    button_black_jack.grid(column=0, row=2, columnspan=1, sticky="we")
    
    button_craps = Button(HOMESCREENFRAME,text="Craps",font=('arial',18),bd=10, width=11)
    button_craps.grid(column=1, row=2, columnspan=1, sticky="we")
    
    button_roulette = Button(HOMESCREENFRAME,text="Roulette",font=('arial',18),bd=10, width=11, command=open_roulette_window)
    button_roulette.grid(column=2, row=2, columnspan=1, sticky="we")
    
    button_deposit = Button(HOMESCREENFRAME,text="Deposit",font=('arial',12),bd=8, command= update_deposit, width=17)
    button_deposit.grid(column=0, row=3, pady=(150,0), sticky="s", columnspan=1)
    
    button_withdraw= Button(HOMESCREENFRAME,text="Withdraw",font=('arial',12),bd=8, command= update_withdraw, width=17)
    button_withdraw.grid(column=1, row=3, pady=(150,0),sticky="s", columnspan=1)
    
    button_change_pw = Button(HOMESCREENFRAME,text="Change Password",font=('arial',12),bd=8, command=update_password, width=17)
    button_change_pw.grid(column=2, row=3, pady=(150,0), sticky="s", columnspan=1)

"""Define button functions"""

# Define update password buttons
def update_password():
    global enter_password, update_pw_label

    top= Toplevel(root)
    top.geometry("400x400")
    top.title("Update Password")
    Label(top, text= "Enter new password:", font=('arial 18 bold')).place(x=75,y=80)
           
    enter_password = Entry(top,font=('arial',20), textvariable=UPDATEPASSWORD,width=15)
    enter_password.place(x=80, y=150)
    
    update_pw_label = Label(top, text= "", font=('arial 8 bold'))
    update_pw_label.place(x=80,y=200)
    
    btn_password = Button(top, text = 'Generate Password', font=('arial',14),width=20, command=partial(passgen, "change"))
    btn_password.place(x=80, y=250)
    
    btn_update_pw = Button(top, text = 'Update Password', font=('arial',14),width=20, command=update_password_submit)
    btn_update_pw.place(x=80, y=300)
    
def update_password_submit():
    check_password_req(UPDATEPASSWORD.get(), 2)
    enter_password.delete(0, END)
    
# Define update deposit buttons
def update_deposit():
    global enter_deposit, update_deposit_label

    top= Toplevel(root)
    top.geometry("400x400")
    top.title("Update Deposit")

    def deposit_funds():
        """Deposit funds into the balance of database"""
        global BALANCE
        amount = enter_deposit.get()
        try:
            amount = int(amount)
        except ValueError:
            tkMessageBox.showerror(
                "Invalid Input",
                "Deposit amount must be an integer.")
            return
        new_balance = int(BALANCE.get()) + amount
        cursor.execute("UPDATE member SET balance=? WHERE mem_id=?", (new_balance, 1))
        CONN.commit()
        BALANCE.set(new_balance)
        LBL_BALANCE.config(text=("Balance\n$" + BALANCE.get()))
        tkMessageBox.showinfo("Success", "Deposit successful.")

    Label(top, text= "Enter Deposit Amount:", font=('arial 18 bold')).place(x=75,y=80)
           
    enter_deposit = Entry(top,font=('arial',20), width=15)
    enter_deposit.place(x=80, y=150)
    
    update_deposit_label = Label(top, text= "", font=('arial 8 bold'))
    update_deposit_label.place(x=80,y=200)
    
    button_update_deposit = Button(top, text='Deposit', font=('arial',14), width=20, command=deposit_funds)
    button_update_deposit.place(x=80, y=300)

########################withdraw###############################

def update_withdraw():
    global enter_withdraw, update_withdraw_label

    top= Toplevel(root)
    top.geometry("400x400")
    top.title("Update Withdraw")

    def withdraw_funds():
        """Withdraw funds into the balance of database"""
        global BALANCE
        amount = enter_withdraw.get()
        try:
            amount = int(amount)
        except ValueError:
            tkMessageBox.showerror(
                "Invalid Input",
                "Withdraw amount must be an integer.")
            return
        new_balance = int(BALANCE.get()) - amount
        cursor.execute("UPDATE member SET balance=? WHERE mem_id=?", (new_balance, 1))
        CONN.commit()
        BALANCE.set(new_balance)
        LBL_BALANCE.config(text=("Balance\n$" + BALANCE.get()))
        tkMessageBox.showinfo("Success", "Withdrawal successful.")

    Label(top, text= "Enter Withdrawal Amount:", font=('arial 18 bold')).place(x=75,y=80)
           
    enter_withdraw = Entry(top,font=('arial',20), width=15)
    enter_withdraw.place(x=80, y=150)
    
    update_withdraw_label = Label(top, text= "", font=('arial 8 bold'))
    update_withdraw_label.place(x=80,y=200)
    
    button_update_withdraw = Button(top, text='Withdraw', font=('arial',14), width=20, command=withdraw_funds)
    button_update_withdraw.place(x=80, y=300)
    
    
# Define Register Tkinter buttons
def exit_program():
    """Add a dropdown to exit the program"""
    result = tkMessageBox.askquestion('You still have money, stay!','Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

def passgen(register_or_change):
    '''This is the Password Automatic Generator'''
    generated_pw = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation) for _ in range(10))
    while not (any(c.isupper() for c in generated_pw) and any(c.islower() for c in generated_pw) and any(c.isdigit() for c in generated_pw) \
        and any(c in string.punctuation for c in generated_pw) and len(generated_pw) >= 10):
        generated_pw = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation) for _ in range(10))
        
    if register_or_change == "change":
        enter_password.delete(0, END)  # clear the entry field
        enter_password.insert(0, generated_pw)
    if register_or_change == "register": 
        LBL_RESULT2.config(text=generated_pw, fg="red")
        password.delete(0, END)  # clear the entry field
        password.insert(0, generated_pw)
        
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
    
    if USERNAME.get() == "" or PASSWORD.get() == "" or EMAIL.get() == "" or BALANCE.get() == "":
        
        LBL_RESULT2.config(text="Please complete the required field!", fg="orange")
        
    # check if password meets requirements
    else:
        check_password_req(PASSWORD.get(), 1)

# Define Password Check Requirements
def check_password_req(passed_password, passvar):
    print(passed_password)
    if passvar == 1:
        if re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{10,}$', passed_password):
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
        else:
            LBL_RESULT2.config(text="Password does not meet requirements!", fg="black")
    else:
        if passvar == 2:
            if re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{10,}$', passed_password):
                cursor.execute("UPDATE member SET password = ? WHERE username = ?", (passed_password, USERNAME.get()))
                CONN.commit()
                enter_password.delete(0, END)
                update_pw_label.config(text="Password Successfully Updated!", fg="black")
            else:
                update_pw_label.config(text="Password does not meet requirements!", fg="red")
            

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
            "SELECT * FROM member WHERE username = ? and password = ?",
            (USERNAME.get(),
            PASSWORD.get()))
        if cursor.fetchone() is not None:
            LBL_RESULT1.config(text="You Successfully Login", fg="blue")
            cursor.execute("SELECT balance FROM member WHERE username = ?", [USERNAME.get()])
            result = cursor.fetchone()
            BALANCE.set(result[0])
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

def logout():
    """Leave the game and close the frame"""
    global HOMESCREENFRAME
    HOMESCREENFRAME.destroy()
    login_form()


# ----------------BlackJack Window------------------------------------
def open_blackjack_window():
    global BLACKJACK_WINDOW, LBL_BLACKJACK, LBL_OUTCOME, LBL_OUTCOME1, LBL_OUTCOME2, LBL_OUTCOME3
    BLACKJACK_WINDOW = Toplevel(root)
    BLACKJACK_WINDOW.title("Blackjack")
    BLACKJACK_WINDOW.geometry("600x400")

    # Create a label to display the game output
    LBL_BLACKJACK = Label(BLACKJACK_WINDOW, text="Your Current Balance Is: $" + BALANCE.get(), font=("Arial", 14))
    LBL_BLACKJACK.pack(pady=10)
    
    lbl_bj_bet = Label(BLACKJACK_WINDOW, text="How much do you want to bet? ", font=("Arial", 14))
    lbl_bj_bet.pack(pady=10)
    
    entry_bj_bet = Entry(BLACKJACK_WINDOW, textvariable=BET, font=("Arial", 14))
    entry_bj_bet.pack(pady=10)

    btn_hit = Button(BLACKJACK_WINDOW, text="HIT", font=("Arial", 14), command=button_clicked)
    btn_hit.pack(pady=10)
    
    #btn_passgen = Button(REGISTERFRAME, text="Generate Password", font=('arial', 18), width=35,command=partial(passgen, "register"))
    
    
    btn_stand = Button(BLACKJACK_WINDOW, text="STAND", font=("Arial", 14))
    btn_stand.pack(pady=10)
    
    # Create a button to play the game
    Button(BLACKJACK_WINDOW, text="Play Blackjack", command=blackjack_submit).pack()
    
    LBL_OUTCOME= Label(BLACKJACK_WINDOW, text="", font=("Arial", 14))
    LBL_OUTCOME.pack(pady=5)
    
    LBL_OUTCOME1= Label(BLACKJACK_WINDOW, text="", font=("Arial", 14))
    LBL_OUTCOME1.pack(pady=5)
    
    LBL_OUTCOME2= Label(BLACKJACK_WINDOW, text="", font=("Arial", 14))
    LBL_OUTCOME2.pack(pady=5)
    
    LBL_OUTCOME3= Label(BLACKJACK_WINDOW, text="", font=("Arial", 14))
    LBL_OUTCOME3.pack(pady=5)
    
def blackjack_submit():
    blackjack()
    
def button_clicked():
    global MYOPTION
    MYOPTION= 'HIT'
    print(MYOPTION)
    
######Blackjack Game#############
def blackjack():
    SUITS = ['hearts', 'diamonds', 'spades', 'clubs']
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    VALUES = {
        '2': 2, '3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9,'10': 10,
        'J': 10,'Q': 10,'K': 10,'A': 11}


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
                
                #Compound operator
                a = "\nPlayer's hand is: \n"
                for x in self.player.hand:
               # b = "Player's hand value: 
                    a+= x + "\n" + self.player.value #"""compund operator means a=a+x+"\n"  """
                LBL_OUTCOME.config(text = a)
                LBL_OUTCOME1.config(text = b)
                #print("\nPlayer's hand is: ", *self.player.cards, sep='\n ')
                #print("Player's hand value: ", self.player.value)
                

              #  player_choice = input("Would you like to hit or stand? ").lower()
                LBL_OUTCOME.config (text= "Would you like to hit or stand? ")
                player_choice = MYOPTION
                if player_choice == 'HIT':
                    self.player.add_card(self.deck.deal())

                    if self.player.value > 21:
                        LBL_OUTCOME.config(text = "Player busts!")
                        game_over = True

                else:
                    game_over = True

            if self.player.value <= 21:
                while self.dealer.value < 17:
                    self.dealer.add_card(self.deck.deal())
            if self.dealer.value > 21:
                LBL_OUTCOME.config(text = "Dealer busts!")
            elif self.dealer.value > self.player.value:
                LBL_OUTCOME.config(text = "Dealer wins!")
            elif self.dealer.value < self.player.value:
                LBL_OUTCOME.config(text = "Player wins!")
            else:
                LBL_OUTCOME.config(text = "It's a tie!")


    a = Game()
    a.play()

    

# #-------------------------------------Craps---------------------------

# def roll_dice():
#     return random.randint(1, 6) + random.randint(1, 6)

# def craps_game(balance):
#     print("Welcome to the game of craps!")
#     print("The rules are simple: roll two dice and try to get a sum of 7 or 11 on the first roll.")
#     print("If you roll a sum of 2, 3, or 12 on the first roll, you lose.")
#     print("Otherwise, the sum you rolled on the first roll becomes your point.")
#     print("You then keep rolling the dice until either you roll your point again (in which case you win)")
#     print("or you roll a 7 (in which case you lose).")
#     print("Let's begin!")

#     print("Your current balance is: $", balance)
#     bet = int(input("How much would you like to bet? "))
#     while bet > balance:
#         print("You do not have sufficient funds.")
#         bet = int(input("Please enter a new bet amount: "))
    
#     first_roll = roll_dice()
#     print("You rolled a", first_roll)

#     if first_roll in (7, 11):
#         balance += bet
#         print("You win! Your new balance is: $", balance)
#         return balance

#     if first_roll in (2, 3, 12):
#         balance -= bet
#         print("You lose! Your new balance is: $", balance)
#         return balance

#     point = first_roll
#     print("Your point is", point)

#     while True:
#         next_roll = roll_dice()
#         print("You rolled a", next_roll)
#         if next_roll == 7:
#             balance -= bet
#             print("You lose! Your new balance is: $", balance)
#             return balance
#         if next_roll == point:
#             balance += bet
#             print("You win! Your new balance is: $", balance)
#             return balance

# if __name__ == '__main__':
#     balance = 100
#     while balance > 0:
#         balance = craps_game(balance)
#         play_again = input("Do you want to play again? (yes/no): ").lower()
#         if play_again == 'no':
#             break
#     print("Thanks for playing! Your final balance is $", balance)

# pass

# #This code uses a while loop to keep playing the craps game as long as
# # the player's balance is greater than 0. After each game, the player 
# # is prompted to play again using the input function. If the player 
# # enters 'no', the break statement is executed to exit the while loop
# # and the game ends. The final balance is printed after the player has
# # decided to stop playing.

# #-----------------------Roulette------------------------------------

def open_roulette_window():
    global ROULETTE_WINDOW, LBL_ROULETTE, LBL_OUTCOME
    ROULETTE_WINDOW = Toplevel(root)
    ROULETTE_WINDOW.title("Roulette")
    ROULETTE_WINDOW.geometry("600x400")

    # Create a label to display the game output
    LBL_ROULETTE = Label(ROULETTE_WINDOW, text="Your Current Balance Is: $" + BALANCE.get(), font=("Arial", 14))
    LBL_ROULETTE.pack(pady=10)
    
    lbl_rbet = Label(ROULETTE_WINDOW, text="How much do you want to bet? ", font=("Arial", 14))
    lbl_rbet.pack(pady=10)
    
    entry_rbet = Entry(ROULETTE_WINDOW, textvariable=BET, font=("Arial", 14))
    entry_rbet.pack(pady=10)

    lbl_rinput = Label(ROULETTE_WINDOW, text="What would you like to bet on? ", font=("Arial", 14))
    lbl_rinput.pack(pady=10)

    entry_rinput = Entry(ROULETTE_WINDOW, textvariable=ROULETTECHOICE, font=("Arial", 14))
    entry_rinput.pack(pady=10)
    
    lbl_rinfo = Label(ROULETTE_WINDOW, text="(even, odd, red, black, 1-18, 19-36, or specific number)", font=("Arial", 14))
    lbl_rinfo.pack(pady=10)
    
    # Create a button to play the game
    Button(ROULETTE_WINDOW, text="Play Roulette", command=roulette_submit).pack()
    
    LBL_OUTCOME= Label(ROULETTE_WINDOW, text="", font=("Arial", 14))
    LBL_OUTCOME.pack(pady=10)
    
def roulette_submit():
    roulette(BET.get(), ROULETTECHOICE.get(), BALANCE.get())

def roulette(BET,ROULETTECHOICE,BALANCE):
    cursor.execute(
            "SELECT * FROM member WHERE username = ? and balance = ?",
            (USERNAME.get(),
            BALANCE))
    print (BET, ROULETTECHOICE, BALANCE)
    balance=int(BALANCE)
    print(BALANCE)
    if balance > 0:
        bet_choice = ROULETTECHOICE
        bet_amount = int(BET)
        balance -= bet_amount

        # Spin the roulette wheel
        spin = random.randint(0, 36)

        # Determine the color of the winning number
        if spin == 0:
            color = "green"
        elif spin in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
            color = "red"
        else:
            color = "black"

        # Determine if the winning number is even or odd
        if spin == 0:
            even_odd = "neither"
        elif spin % 2 == 0:
            even_odd = "even"
        else:
            even_odd = "odd"

        # Check if the player won or lost
        if (bet_choice == "even" and even_odd == "even") or (bet_choice == "odd" and even_odd == "odd") or \
            (bet_choice == "red" and color == "red") or (bet_choice == "black" and color == "black") or \
            (bet_choice == "1-18" and spin >= 1 and spin <= 18) or (bet_choice == "19-36" and spin >= 19 and spin <= 36) or (bet_choice.isdigit() and int(bet_choice) == spin):
            balance += bet_amount * 36 // 35
            LBL_OUTCOME.config(text="The spin was " + str(spin) + " " + color + " " + even_odd + ". You won $" + str(bet_amount * 36 // 35) + "! Your balance is now $" + str(balance) + ".")
        else:
            LBL_OUTCOME.config(text="The spin was " + str(spin) + " " + color + " " + even_odd + ". You lost $" + str(bet_amount) + ". Your balance is now $" + str(balance - bet_amount) + ".")
    else:
        LBL_OUTCOME.config(text= "You balance is 0")
    #LBL_OUTCOME.config(text="You have run out of money. Game over.")

# root = Tk()
# open_roulette_window()
root.mainloop()

# roulette() # Call the roulette function at the end.



# The player has the option to bet on a specific number, in addition
# to even or odd, red or black, and within a range. The payouts for
# betting on a specific number have been adjusted to 36:35 odds, 
# meaning that if the player wins, they receive $36 for every $35 bet.
# The player continues to play until their balance is zero, at which 
# point the game ends.

