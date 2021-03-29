from cards import Deck


class Player:
    """
    Class representing a player of the game, keeping a hand of cards and a
    handle to the deck used by the game instance
    """

    def __init__(self, deck):
        self.hand = []
        self.deck = deck

    def draw_one(self):
        card = self.deck.draw_one()
        self.hand.append(card)
        return card

    def __hash__(self):
        """
        Define a hash function so that this can be a key in dictionaries
        """
        return hash(id(self))

    def reset(self):
        self.hand = []

    @property
    def hand_value(self):
        return sum((card.points for card in self.hand))


class Game:
    """
    Class representing the game. It will create a deck and two players,
    then run the game and report the results.
    """

    def __init__(self, quiet=False):
        """
        Init the game. If quiet is true, console messages will be suppressed
        """
        self.deck = Deck()
        self.player1 = Player(self.deck)
        self.player2 = Player(self.deck)
        self._quiet = quiet

    def draw_cards(self):
        """
        Players alternate drawing until they have drawn 3 each
        """
        for _ in range(3):
            card1 = self.player1.draw_one()
            card2 = self.player2.draw_one()
            if not self._quiet:
                print(f"Player 1 draws {card1}")
                print(f"Player 2 draws {card2}\n--------")

    def compare_hands(self):
        """
        Point values for each hand are calculated and the winner is returned
        """

        points1 = self.player1.hand_value
        points2 = self.player2.hand_value
        winner = None
        if not self._quiet:
            print(f"Player 1 scores {points1} points!")
            print(f"Player 2 scores {points2} points!")
        if points1 != points2:
            winner = self.player1 if points1 > points2 else self.player2
            if not self._quiet:
                print(f"Player {1 if points1 >= points2 else 2} wins!")
        else:
            if not self._quiet:
                print("Players tie and there is no winner!")
        return winner

    def play(self):
        """
        Play the game one time. Each player is reset to an empty hand and the
        deck is shuffled. The winning player is returned.
        """
        self.player1.reset()
        self.player2.reset()
        self.deck.shuffle()

        self.draw_cards()
        winner = self.compare_hands()

        return winner
