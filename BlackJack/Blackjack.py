# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
game_result=""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


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
        # create Hand object
        self.suit_hand=[]
        self.rank_hand=[]
        
    def __str__(self):
        # return a string representation of a hand
        card_length=len(self.rank_hand)
        index=0
        hand_list=[]
        while index < card_length:
            hand_list.append(str(self.suit_hand[index])+str(self.rank_hand[index]))
            index+=1
        return hand_list

    def add_card(self, card):
        # add a card object to a hand
        self.suit_hand.append(card.get_suit())
        self.rank_hand.append(card.get_rank())

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        ace_times=0
        hand_value=0
        for ranks in self.rank_hand:
            if VALUES[ranks] == 1:
                ace_times+=1
            hand_value+=VALUES[ranks]
        while ace_times>0:
            if (hand_value+10) <= 21:
                hand_value+=10
            ace_times-=1
        return hand_value
                
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        card_length=len(self.rank_hand)
        index=0
        normal=pos[0]
        while index < card_length:
            pos[0]=normal
            cards=Card(self.suit_hand[index],self.rank_hand[index])
            pos[0]+=index*(CARD_SIZE[0]*4/3)
            cards.draw(canvas, pos)
            index+=1
            
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck=[]
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(suit+rank)
        

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck)
        
    def deal_card(self):
        # deal a card object from the deck
        card=self.deck.pop(0)
        return card
    
    def __str__(self):
        # return a string representing the deck
        string=""
        for value in self.deck:
            string+=value+","
        return string


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_one, player_two,game_result,score
    # your code goes here
    if in_play == True:
        outcome="Game is already running. score minus 1."
        score-=1
    game_result=""
    deck=Deck()
    deck.shuffle()
    player_one=Hand()
    player_two=Hand()
    card_list=[]
    for index in range(4):
        card_list.append(deck.deal_card())
    for index in range(2):
        card=Card(card_list[index][0],card_list[index][1])
        player_one.add_card(card)
        card2=Card(card_list[index+2][0],card_list[index+2][1])
        player_two.add_card(card2)
        
    in_play = True
    outcome="hit or stand?"
def hit():
    # replace with your code below
    global player_one, outcome, game_result,score, in_play
    # if the hand is in play, hit the player
    card_string=""
    if in_play == True:
        card_string=deck.deal_card()
        card=Card(card_string[0],card_string[1])
        player_two.add_card(card)
    # if busted, assign a message to outcome, update in_play and score
        if player_two.get_value() > 21:
            outcome="You have busted. New deal?"
            game_result="You lose."
            score-=1
            in_play=False
def stand():
    # replace with your code below
    global player_one,player_two,game_result, in_play,score,outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while player_one.get_value() < 17:
            card_string=deck.deal_card()
            card=Card(card_string[0],card_string[1])
            player_one.add_card(card)
    # assign a message to outcome, update in_play and score
        if player_one.get_value() > 21:
            game_result="You Win."
            outcome="BANKER have busted. New deal?"
            score+=1
        else:
            if player_one.get_value() < player_two.get_value():
                game_result="You Win."
                score+=1
            elif player_one.get_value() == player_two.get_value():
                game_result="Win Win."
            else:
                game_result="You lose."
                score-=1
            outcome="New deal?"
        in_play = False
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    if in_play==True:
        canvas.draw_image(card_back, (CARD_CENTER[0],CARD_CENTER[1]), CARD_SIZE, [CARD_SIZE[0] + CARD_CENTER[0], 300-CARD_CENTER[1]], CARD_SIZE)
        banker_list=[]
        banker_list=player_one.__str__()
        cards=Card(banker_list[1][0],banker_list[1][1])
        cards.draw(canvas, [CARD_SIZE[0] + CARD_CENTER[0]+(CARD_SIZE[0]*4/5),300-CARD_SIZE[1]])
        player_two.draw(canvas, [CARD_SIZE[0] ,300+CARD_SIZE[1]])
    else:
        player_one.draw(canvas, [CARD_SIZE[0] ,300-CARD_SIZE[1]])
        player_two.draw(canvas, [CARD_SIZE[0] ,300+CARD_SIZE[1]])
    canvas.draw_text("Blackjack",[CARD_SIZE[0] ,300-(CARD_SIZE[1]*2)],36,'Aqua')
    canvas.draw_text("Banker",[CARD_SIZE[0],300-CARD_SIZE[1]-CARD_CENTER[1]],24,'Black')
    canvas.draw_text("Player",[CARD_SIZE[0],300+CARD_CENTER[1]],24,'Black')
    canvas.draw_text(game_result,[200,300-CARD_SIZE[1]-CARD_CENTER[1]],24,'Black')
    canvas.draw_text(outcome,[200,300+CARD_CENTER[1]],24,'Black')
    result="score = "+str(score)
    canvas.draw_text(result,[430,300-CARD_SIZE[1]-CARD_CENTER[1]],24,'Black')
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
