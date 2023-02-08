suits = ['hearts', 'diamonds', 'spades', 'clubs']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10, 'A':11}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        
    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp
        
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'A':
            self.aces += 1
            
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Game:
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
            
