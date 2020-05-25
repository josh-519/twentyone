from tkinter import *
import random

# variables
HEIGHT = 600
WIDTH = 800
bg_color = "green"
btn_font = "Helvetica"

DECK = ["2H","2D","2C","2S",
        "3H","3D","3C","3S",
        "4H","4D","4C","4S",
        "5H","5D","5C","5S",
        "6H","6D","6C","6S",
        "7H","7D","7C","7S",
        "8H","8D","8C","8S",
        "9H","9D","9C","9S",
        "10H","10D","10C","10S",
        "JH","JD","JC","JS",
        "QH","QD","QC","QS",
        "KH","KD","KC","KS"
        ,"AH","AD","AC","AS"]
header = "Welcome to BlackJack"
rules = "Highest Card total without going over 21 wins\nFace cards are worth 10\nAces are worth 1 or 11\nAll other cards are worth face value\nDealer stays on 17\nTies go to Dealer"
deck_in_use = DECK
dealers_hand = []
players_hand = []

# creating and displaying card
# takes card x_position and y_position
class Card:
    def __init__(self, dealt_card, x_pos, y_pos):
        self.dealt_card = dealt_card
        self.x_pos = x_pos
        self.y_pos = y_pos

    def draw_card(self):        
        card = PhotoImage(file = f"./img/{self.dealt_card}.gif")
        label = Label(display, image = card)
        label.image = card # keeps a reference
        label.place(x = self.x_pos, y = self.y_pos, relx = 0,rely = 0, height = 150, width = 98)
        

# count the value of the hand and return
def hand_value(hand):
    total = 0
    # counting aces in hand used as 11
    ace_count = 0
    for card in hand:
        if str(card[0]) == "J":
            total += 10
        elif str(card[0]) == "Q":
            total += 10
        elif str(card[0]) == "K":
            total += 10
        elif str(card[0]) == "A":
            if total + 11 > 21:
                total += 1
            else:
                total += 11
                ace_count += 1
        # 1 represents 10 but only pulls first character
        elif int(card[0]) == 1:
            total += 10
        else:
            total += int(card[0])
    # accounting for ace value of 11 busting and multiple aces
    if total > 21 and ace_count != 0:
        while ace_count != 0 and total > 21:
            ace_count -= 1
            total -= 10
    return total

# check if busted
# hit player
# add card to players hand and display
def hit():
    if hand_value(players_hand) <= 21:
        dealt_card = deal_card()
        players_hand.append(dealt_card)
        card_pos = 120
        for card in players_hand:
            card = Card(card, card_pos, 300)
            card.draw_card()
            card_pos += 110
        # debugging
        #print(players_hand)
        
    players_total = hand_value(players_hand)
    # debugging
    #print(players_total)
    if players_total > 21:
        busted("Player", players_total)
    return

# deal card and add to dealers hand
def stay():
    while hand_value(dealers_hand) < hand_value(players_hand) and hand_value(dealers_hand) < 17 and hand_value(players_hand) < 22:
        dealt_card = deal_card()
        dealers_hand.append(dealt_card)
    card_pos = 120
    for card in dealers_hand:
        card = Card(card, card_pos, 100)
        card.draw_card()
        card_pos += 110
    # debugging
    #print(dealers_hand)
    
    dealers_total = hand_value(dealers_hand)
    # debugging
    #print(dealers_total)
    if dealers_total > 21:
        busted("Dealer", dealers_total)
    elif dealers_total >= hand_value(players_hand):
        winner("Dealer", dealers_total)
    else:
        if hand_value(players_hand) < 22:
            total = hand_value(players_hand)
            winner("Player", total)
    return

def busted(who, total):
    # debugging
    #print(f"{who} busted with {total}")
    if who == "Player":
        frame = Frame(display, bg = bg_color)
        frame.place(x = 250, y = 250, height = 50, width = 300)

        label = Label(frame, text = f"{who} bust with {total}", font=(btn_font, 20, "bold"), pady = 5, bg = bg_color)
        label.pack()

        frame = Frame(display, bg = bg_color)
        frame.place(x = 0, y = 500, relheight = 50, relwidth = 1)

        Button(frame, text = 'Play Again', font=(btn_font, 12, "bold"), width = 20, command = replay).place(x = 125, y = 0)
        Button(frame, text = 'Quit', font=(btn_font, 12, "bold"), width = 20, command = end_game).place(x = 465, y = 0)
        
    elif who == "Dealer":
        total = hand_value(players_hand)
        winner("Player", total)

def winner(who, total):
    frame = Frame(display, bg = bg_color)
    frame.place(x = 250, y = 250, height = 50, width = 300)

    label = Label(frame, text = f"{who} wins with {total}", font=(btn_font, 20, "bold"), pady = 5, bg = bg_color)
    label.pack()

    frame = Frame(display, bg = bg_color)
    frame.place(x = 0, y = 500, relheight = 50, relwidth = 1)
    
    Button(frame, text = 'Play Again', font=(btn_font, 12, "bold"), width = 20, command = replay).place(x = 125, y = 0)
    Button(frame, text = 'Quit', font=(btn_font, 12, "bold"), width = 20, command = end_game).place(x = 465, y = 0)

    # debugging
    #print(f"{who} wins with {total}")

def replay():
    for card in dealers_hand:
        deck_in_use.append(card)
    for card in players_hand:
        deck_in_use.append(card)
    del dealers_hand[:]
    del players_hand[:]
    display.delete('all')
    play()

# ends game and closes window
def end_game():
    window.destroy()
    quit()

# selecting a random card from deck and removing it from the deck
def deal_card():
    dealt_card = random.choice(deck_in_use)
    deck_in_use.remove(dealt_card)
    return dealt_card

# dealing a card and adding it to dealers hand
def deal_dealer():    
    dealt_card = deal_card()
    dealers_hand.append(dealt_card)
    return dealers_hand

# dealing a card and adding it to players hand
def deal_player():
    dealt_card = deal_card()
    players_hand.append(dealt_card)
    return players_hand

# deal two cards each with 1st dealer card face down
def first_deal():
    card_pos = 120
    while (2 != len(dealers_hand)):
        deal_player()
        for card in players_hand:
            card = Card(card, card_pos, 300)
            card.draw_card()
        # debugging
        #print(players_hand)
        deal_dealer()
        for card in dealers_hand:
            if card_pos == 120:
                card = Card("red_back", card_pos, 100)
                card.draw_card()
            else:
                card = Card(card, card_pos, 100)
                card.draw_card()
        # debugging
        #print(dealers_hand)        
        card_pos += 110
    return

# game play    
def play():
    display.delete('all')
    frame = Frame(display, bg = bg_color)
    frame.place(x = 0, y = 0, relheight = 1, relwidth = 1)

    first_deal()
    # debugging
    #print("Dealers has : " + str(hand_value(dealers_hand)))
    #print("Player has : " + str(hand_value(players_hand)))

    # hit and stay buttons
    Button(frame, text = 'Hit', font=(btn_font, 12, "bold"), width = 20, command = hit).place(x = 125, y = 500)
    Button(frame, text = 'Stay', font=(btn_font, 12, "bold"), width = 20, command = stay).place(x = 465, y = 500)
    return

# splash screen
def splash():
    frame = Frame(display, bg = bg_color)
    frame.place(x = 0, y = 0, relheight = 1, relwidth = 1)

    header_lbl = Label(frame, text = header, font=(btn_font, 35, "bold"), padx = 5, pady = 5, bg = bg_color)
    header_lbl.place(x = 135, y = 50)
    rules_lbl = Label(frame, text = "Rules: ",fg="red", font=(btn_font, 20), padx = 5, pady = 5, bg = bg_color)
    rules_lbl.place(x = 80, y = 180)
    rules1_lbl = Label(frame, text = rules, font=(btn_font, 20), padx = 5, pady = 5, bg = bg_color, anchor = W, justify = LEFT)
    rules1_lbl.place(x = 175, y = 180)
    
    Button(frame, text = 'Play', font=(btn_font, 12, "bold"), width = 20, command = play).place(x = 125, y = 500)
    Button(frame, text = 'Quit', font=(btn_font, 12, "bold"), width = 20, command = end_game).place(x = 465, y = 500)
    return

if __name__ == '__main__':
    window = Tk()
    window.title('21')
    window.resizable(0,0)
    
    display = Canvas(window, height = HEIGHT, width = WIDTH)
    display.pack()    

    splash()
    

    window.mainloop()
