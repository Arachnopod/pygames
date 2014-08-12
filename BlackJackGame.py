# Blackjack
# Author: John Liu
# Date: 2014-May-10

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

deck = []



# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        
    def __str__(self):
        hand = ""
        for i in self.cards:
            hand = hand + str(i) + ' '
        return hand
    
    def add_card(self, card):
        self.cards.append(card)
        
    def get_value(self):
        hand = 0
        has_ace = False
        for i in self.cards:
            hand += VALUES[i.get_rank()]
            if i.get_rank() == "A":
                has_ace = True
        if has_ace:               
            if hand < 12:
                hand += 10
        return hand      
                 
    def draw(self, canvas, pos):
        for i in self.cards:
            i.draw(canvas, [ pos[0] + self.cards.index(i) * CARD_SIZE[0], pos[1] ])
                           
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for i in SUITS:
            for j in RANKS:
                self.deck.append(Card(i,j))
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        if len(self.deck) > 0:
            return self.deck.pop()
    
    def __str__(self):
        hand = ""
        for i in self.deck:
            hand = hand + str(i) + ' '
        return hand            
    

#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, deck, outcome, score
    outcome = "Hit or Stand?"
    if in_play:
        score -= 1
        outcome = "Hand Lost in Redeal. Hit or Stand?"
    in_play = True
    # your code goes here
    deck = Deck()
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())    

    print "player", player
    print "dealer", dealer
    
def hit():
    global player, in_play, deck, score, outcome
    # if the hand is in play, hit the player
    if in_play:
        player.add_card(deck.deal_card())
        outcome = "Hit or Stand?"
    # if busted, assign a message to outcome, update in_play and score
        if player.get_value() > 21:
            outcome = "Player Busted!   New Deal?"
            print outcome
            in_play = False
            score -= 1
       
def stand():
    global player, dealer, in_play, deck, score, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())        
            print "dealer", dealer
        print "Player value = ",player.get_value()
        print "Dealer value = ",dealer.get_value()

    # assign a message to outcome, update in_play and score
        in_play = False
        if dealer.get_value() > 21:
            outcome= "Dealer Busted!   New Deal?"
            print outcome
            score += 1
        elif dealer.get_value() >= player.get_value():
            outcome = "Dealer Wins!   New Deal?"
            print outcome
            score -= 1
        else:
            outcome = "Player Wins!   New Deal?"
            print outcome
            score += 1
        
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player, dealer, outcome, player, dealer
    dealer.draw(canvas, [150, 400])
    player.draw(canvas, [150, 100])
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [151 + CARD_BACK_CENTER[0], 401 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    canvas.draw_text("Score = " +str(score), [400,50], 32, "White")
    canvas.draw_text("BlackJack", [50,50], 40, "Orange")
    canvas.draw_text(outcome, [100, 300], 32, "Yellow")
    canvas.draw_text("Player", [50, 150],24, "Aqua")
    canvas.draw_text("Dealer", [50, 450],24, "Aqua")
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric