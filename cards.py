"""
Classes that support cards and decks, their values in the game, and behavior
"""

from functools import total_ordering
import random

random.seed()  # Defaults to current system time


# pylint: disable=too-few-public-methods
class Suit:
    """
    Class representing data about card suits, their values in the game, and
    how they should be printed.
    """

    # Enum that also functions as point values
    SPADE = 1
    DIAMOND = 2
    HEART = 3
    CLUB = 4

    # Easily iterable set of suits
    ALL_SUITS = {SPADE, DIAMOND, HEART, CLUB}

    # Printable names for the suits
    PRETTY_NAME = {
        SPADE: "Spade",
        DIAMOND: "Diamond",
        HEART: "Heart",
        CLUB: "Club",
    }


@total_ordering
class Card:
    """
    Class representing a single card, with a suit and value
    """

    # Printable names for the special ones
    _PRETTY_VALUE = {
        11: "Jack",
        12: "Queen",
        13: "King",
        14: "Ace",
    }

    def __init__(self, suit, value):
        """
        Init the card with a suit and value, and sanity check the inputs
        """
        assert suit in Suit.ALL_SUITS
        assert isinstance(value, int)
        assert 2 <= value <= 14
        self.suit = suit
        self.value = value

    def __eq__(self, other):
        """
        Equality comparison should rely on same type, suit and value
        """
        if not isinstance(other, type(self)):
            return False
        return self.suit == other.suit and self.value == other.value

    def __lt__(self, other):
        """
        Ordering is first by suit value, then by card value
        (our comparisons are symmetric and sensible, so total_ordering can
        take it from here)
        """
        if self.suit == other.suit:
            return self.value < other.value
        return self.suit < other.suit

    def __str__(self):
        """
        A more readable representation, "2 of Hearts" for example
        """
        return f"{self.pretty_value} of {self.pretty_suit}s"

    def __repr__(self):
        """
        A more compact representation, "(Jack, Spade)" for example
        """
        return f"({self.pretty_suit}, {self.pretty_value})"

    @property
    def points(self):
        """ Return the calculated value of this card """
        return self.suit * self.value

    @property
    def pretty_value(self):
        """
        Look up the pretty value, defaulting to the number
        """
        return Card._PRETTY_VALUE.get(self.value, self.value)

    @property
    def pretty_suit(self):
        """
        Look up the nice name for the suit.
        """
        return Suit.PRETTY_NAME[self.suit]


class Deck:
    """
    Class representing a standard deck of cards
    """

    def __init__(self):
        """
        Init the deck by creating a list of cards with values 2 through 14, and
        an empty discard pile.
        """
        self.cards = [Card(a, b) for a in Suit.ALL_SUITS for b in range(2, 15)]
        self.pile = []

    def combine_deck_and_pile(self):
        """
        Add the discard pile back to the deck
        """
        self.cards.extend(self.pile)
        self.pile = []

    def shuffle(self):
        """
        Shuffle this deck. This assumes that we should recombine the pile
        first.
        """
        self.combine_deck_and_pile()
        new_cards = []

        # Remove 52 cards from the old deck one by one, each time randomly
        # choosing which of the remaning cards to pull out. This method
        # keeps memory use relatively stable (all card objects are preserved,
        # and a temporary list stores them), and shuffles in a single pass.
        for i in range(51, -1, -1):
            rand_card = random.randint(0, i)
            new_cards.append(self.cards.pop(rand_card))
        self.cards = new_cards

    def draw_one(self):
        """
        Draw a card from the deck. It goes into the discard pile, and the Card
        is returned to the caller
        """
        next_card = self.cards.pop(0)
        self.pile.append(next_card)
        return next_card

    def sort(self):
        """
        Sort the deck. We can use sorted because Cards have a proper ordering.
        The assumption here is that it's preferable to sort them rather than
        statically define the (known) set of 52 cards that will always
        represent a standard sorted deck.

        The second assumption is that we're not concerned with memory use, as
        this will create a copy of the deck list temporarily, rather than
        sorting in place.
        """
        self.combine_deck_and_pile()
        self.cards = sorted(self.cards)
