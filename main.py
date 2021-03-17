import random

class Card():
    def __init__(self, suit, rank, available=True):
        self.suit = suit
        self.rank = rank
        self.available = available
        self.hidden = False

    def __str__(self):
        if not self.hidden:
            return "[ " + self.suit + " / " + self.rank + " ]"
        else:
            return "[ hidden / hidden ]"

    def __repr__(self):
        return str(self)

    def get_value(self):
        val = 0
        if (self.rank == "2" or self.rank == "3" or
                self.rank == "4" or self.rank == "5" or
                self.rank == "6" or self.rank == "7" or
                self.rank == "8" or self.rank == "9" or
                self.rank == "10"):
            val = int(self.rank)
        elif (self.rank == "Jack" or self.rank == "Queen" or
              self.rank == "King"):
            val = 10
        elif (self.rank == "Ace"):
            val = 11
        return val


class Deck():
    def __init__(self):
        self.cards = []
        suits = ["HEARTS", "CLUBS", "SPADES", "DIAMONS"]
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def get_random_card(self):
        while True:
            index = random.randint(0, 51)
            if self.cards[index].available:
                self.cards[index].available = False
                return self.cards[index]


class Game():

    def __init__(self):
        # init deck
        self.deck = Deck()
        self.player_cards = []
        self.dealer_cards = []

    def start(self):
        # initialize 2 random cards to the player
        self.player_cards.append(self.dealt_card())
        self.player_cards.append(self.dealt_card())

        # initialize 2 random cards to dealer
        self.dealer_cards.append(self.dealt_card())
        # hide one of the cards
        hidden_card = self.dealt_card()
        hidden_card.hidden = True
        self.dealer_cards.append(hidden_card)

        # display the initial game
        self.print_game()

        while True:
            # ask player what is the next action
            action = input("what do you want yo do? [hit, stay]")
            if action == "hit":
                # if it's hit add a new card and print the game
                self.player_cards.append(self.dealt_card())
                self.print_game()
            elif action == "stay":
                # if it's stay, it will show the hidden card
                self.dealer_cards[1].hidden = False
                # and hit new cards to the deck util complete 17 or more points for the dealer
                while self.get_sum_of_cards(self.dealer_cards) < 17:
                    self.dealer_cards.append(self.dealt_card())
                # print the result
                self.print_game()
                # calculate final points
                self.calculate_points()
                return
            else:
                print(action, " is not a valid action, please try again")

    def dealt_card(self):
        return self.deck.get_random_card()

    def get_sum_of_cards(self, cards):
        card_total = 0
        for card in cards:
            card_total = card_total + card.get_value()
        return card_total

    def print_game(self):
        print("player", self.player_cards)
        print("dealer", self.dealer_cards)
        print("---------------------------")

    def calculate_points(self):
        # check if player have a blackjack
        player_blackjack = self.check_blackjack(self.player_cards)
        # check if dealer have a blackjack
        dealer_blackjack = self.check_blackjack(self.dealer_cards)

        # if both have a blackjack, it's a push, and no one win the game
        if player_blackjack and dealer_blackjack:
            print("push: the player and the dealer received a blackjack")
            return

        # if only the player have a blackjack, the player win the game
        if player_blackjack:
            print("you win the game with a blackjack")
            return

        # if only the dealer have a blackjack, the dealer win the game
        if dealer_blackjack:
            print("the dealer received a blackjack, you lose the game")
            return

        # calculate total points of the player
        player_points = self.get_sum_of_cards(self.player_cards)
        # if it's more than 21, the player lose the game
        if player_points > 21:
            print("You lose the game, the sum exceeded 21 points. Total:", player_points)
            return

        # calculate the dealer points
        dealer_points = self.get_sum_of_cards(self.dealer_cards)

        # If the dealer exceeds 21 ("busts") and the player does not, the player wins
        if dealer_points > 21:
            print("you win the game! the dealer exceeded 21 points")
            return

        # If the player attains a final sum higher than the dealer and does not bust, the player wins.
        if player_points > dealer_points:
            print("you win the game!")
        elif player_points == dealer_points: # if the player and the dealer have the same sum, it's a push
            print("push: the player and the dealer received the same sum")
        else: # if not, player lose the game and dealer win.
            print("you lose the game!")

        # show final score
        print("you: [", player_points, "], dealer:[", dealer_points, "]")

    def check_blackjack(self, cards):
        has_ace = False
        has_ten = False
        for card in cards:
            if card.get_value() == 10:
                has_ten = True
            elif card.get_value() == 11:
                has_ace = True
        return has_ace and has_ten

action = "yes"
while action == "yes":
    # start the game
    game = Game()
    game.start()
    # ask if the player wants to start a new game
    action = input("Do you want to player another game? [yes, no]")
print("Thank you for your time")
