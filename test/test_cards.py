"""
Tests for classes in the cards module
"""
import unittest
from essex.cards import Card, Deck, Suit


class TestSuit(unittest.TestCase):
    """
    Tests for the Suit class
    """

    def test_suit_values(self):
        """
        Test that suits have the correct value
        """
        self.assertEqual(Suit.SPADE, 1)
        self.assertEqual(Suit.DIAMOND, 2)
        self.assertEqual(Suit.HEART, 3)
        self.assertEqual(Suit.CLUB, 4)

    def test_all_suits(self):
        """
        Test that the set of all suits contains the expected
        suits (and no extra)
        """
        for suit in (Suit.SPADE, Suit.DIAMOND, Suit.HEART, Suit.CLUB):
            self.assertIn(
                suit, Suit.ALL_SUITS, f"{Suit.PRETTY_NAME[suit]} not found in ALL_SUITS"
            )
        self.assertEqual(len(Suit.ALL_SUITS), 4, "Incorrect number of suits found")

    def test_pretty_names(self):
        """
        Test that the pretty names are correct
        """
        expected = (
            (Suit.SPADE, "Spade"),
            (Suit.DIAMOND, "Diamond"),
            (Suit.HEART, "Heart"),
            (Suit.CLUB, "Club"),
        )

        for suit, pretty in expected:
            self.assertEqual(Suit.PRETTY_NAME[suit], pretty)

        self.assertEqual(len(Suit.PRETTY_NAME), 4)


class TestCard(unittest.TestCase):
    """ Test cases for the Card class """

    def test_card_suits_positive(self):
        """
        Test creating cards with all the suits
        """
        for suit in Suit.ALL_SUITS:
            card = Card(suit, 2)
            self.assertEqual(card.suit, suit)

    def test_card_values_positive(self):
        """
        Test creating cards with all the valid values
        """
        for i in range(2, 15):
            card = Card(Suit.SPADE, i)
            self.assertEqual(card.value, i)

    def test_card_not_equal_other(self):
        """
        Tests that cards are not equal to other types of objects
        """
        card = Card(Suit.SPADE, 2)
        for bad_value in ("a", "1", "2", 2, 20.0, Card):
            self.assertNotEqual(card, bad_value)

    def test_bad_card_suit(self):
        """
        Test creating a card with an invalid suit
        """
        for bad_suit in ("bad", -1, 0, 5, 100):
            with self.assertRaises(AssertionError):
                Card(bad_suit, 2)

    def test_bad_card_value(self):
        """
        Test creating a card with an invalid value
        """
        for bad_val in ("bad", -1, 0, 1, 15, 100):
            with self.assertRaises(AssertionError):
                Card(Suit.SPADE, bad_val)

    def test_card_value_ordering(self):
        """
        Tests that cards are ordered correctly when suits match
        """
        card3 = Card(Suit.SPADE, 3)
        card2 = Card(Suit.SPADE, 2)
        card10 = Card(Suit.SPADE, 10)

        pairs = ((card2, card3), (card2, card10), (card3, card10))

        for less, greater in pairs:
            self.assertLess(less, greater)
            self.assertLessEqual(less, greater)

            self.assertGreater(greater, less)
            self.assertGreaterEqual(greater, less)

        card2_2 = Card(Suit.SPADE, 2)
        self.assertEqual(card2, card2_2)
        self.assertLessEqual(card2, card2_2)
        self.assertGreaterEqual(card2, card2_2)

    def test_card_suit_ordering(self):
        """
        Tests that Cards are ordered correctly by suit when value is the same
        """

        spade2 = Card(Suit.SPADE, 2)
        diamond2 = Card(Suit.DIAMOND, 2)
        heart2 = Card(Suit.HEART, 2)
        club2 = Card(Suit.CLUB, 2)

        pairs = (
            (spade2, diamond2),
            (spade2, heart2),
            (spade2, club2),
            (diamond2, heart2),
            (diamond2, club2),
            (heart2, club2),
        )

        for less, greater in pairs:
            self.assertLess(less, greater)
            self.assertLessEqual(less, greater)

            self.assertGreater(greater, less)
            self.assertGreaterEqual(greater, less)

    def test_card_overall_ordering(self):
        """
        Tests that Cards are ordered correctly by suit and value

        To get maximal coverage while still making this readable, the
        code structure is to have a list of known-good ordering of a full
        set of cards. Then we will iterate the list and check that every
        card lower in the list is ordered "less than" and every card higher
        in the list is ordered "greater than". (Note: this may make other
        ordering tests superfluous. They may still serve some use, as they
        are inexpensive to run, and would help us narrow down potential
        code issues if something in here were to regress.
        """

        all_cards = [
            Card(suit, value)
            for suit in (Suit.SPADE, Suit.DIAMOND, Suit.HEART, Suit.CLUB)
            for value in range(2, 15)
        ]

        for i, test_card in enumerate(all_cards):
            for j, check_card in enumerate(all_cards):
                if j < i:
                    self.assertLess(check_card, test_card)
                    self.assertLessEqual(check_card, test_card)
                elif j > i:
                    self.assertGreater(check_card, test_card)
                    self.assertGreaterEqual(check_card, test_card)
                else:
                    self.assertEqual(test_card, check_card)
                    self.assertLessEqual(test_card, check_card)
                    self.assertGreaterEqual(test_card, check_card)

    def test_pretty_values(self):
        """
        Tests that values are pretty printed correctly
        """
        expected = (
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            (6, 6),
            (7, 7),
            (8, 8),
            (9, 9),
            (10, 10),
            (11, "Jack"),
            (12, "Queen"),
            (13, "King"),
            (14, "Ace"),
        )

        for value, pretty in expected:
            self.assertEqual(pretty, Card(Suit.HEART, value).pretty_value)

    def test_str(self):
        """
        Tests that cards print nicely when str'd
        """
        card1 = Card(Suit.SPADE, 2)
        card2 = Card(Suit.DIAMOND, 12)
        card3 = Card(Suit.HEART, 14)
        card4 = Card(Suit.CLUB, 11)

        self.assertEqual(str(card1), "2 of Spades")
        self.assertEqual(str(card2), "Queen of Diamonds")
        self.assertEqual(str(card3), "Ace of Hearts")
        self.assertEqual(str(card4), "Jack of Clubs")

    def test_repr(self):
        """
        Tests that the repr of cards prints nicely
        """
        card1 = Card(Suit.SPADE, 2)
        card2 = Card(Suit.DIAMOND, 12)
        card3 = Card(Suit.HEART, 14)
        card4 = Card(Suit.CLUB, 11)

        self.assertEqual(repr(card1), "(Spade, 2)")
        self.assertEqual(repr(card2), "(Diamond, Queen)")
        self.assertEqual(repr(card3), "(Heart, Ace)")
        self.assertEqual(repr(card4), "(Club, Jack)")

    def test_points(self):
        """
        Tests that the points are calculated correctly
        """
        for card in TestDeck.ALL_CARDS:
            self.assertEqual(card.points, card.value * card.suit)


class TestDeck(unittest.TestCase):
    """
    Tests for the Deck class
    """

    # We will often be using this set of all valid cards for validation, and
    # it's better not to keep creating and destroying the objects.
    ALL_CARDS = [
        Card(a, b)
        for a in (Suit.SPADE, Suit.DIAMOND, Suit.HEART, Suit.CLUB)
        for b in range(2, 15)
    ]

    @staticmethod
    def _sanity_check(deck):
        """
        Common validations that check the overall integrity of our deck after
        various operations.
        """
        # Do we have the right number of cards
        assert len(deck.cards) + len(deck.pile) == 52

        # Do we have all of the cards we're supposed to (combined with above,
        # we should have exactly the right cards, all the necessary ones and
        # no extras)
        for card in TestDeck.ALL_CARDS:
            assert card in deck.cards or card in deck.pile

    def test_simple_creation(self):
        """
        Check that a deck gets created correctly
        """
        deck = Deck()
        self._sanity_check(deck)

    def test_initial_sorted_deck(self):
        """
        Tests that the initial form of the deck is sorted. This isn't strictly
        a requirement, but it is true now, and some tests will depend on this
        behavior. So if this test starts failing, we'll need to sort the decks
        before relying on that.
        """
        deck = Deck()
        self.assertEqual(deck.pile, [])
        for i in range(len(TestDeck.ALL_CARDS)):
            self.assertEqual(TestDeck.ALL_CARDS[i], deck.cards[i])

    def test_shuffle(self):
        """
        Tests that the shuffle method does, in fact, shuffle.

        This turns out to be somewhat tricky, as I don't believe that there is
        a good way to measure randomness. We can check that the ordering is not
        identical, but this doesn't tell us if it does something silly like
        move the top card to the bottom and return. But a truly random shuffle
        could (with odds around 1:10^67) produce an identical deck.

        We can check that at least N cards have moved position, but the more
        of these we insist on, the more likely we are to run into a situation
        where a "real" shuffle does put some cards in the same spot they were
        in before the shuffle.

        We can also ensure that they did not all move by the same number of
        places (i.e. some kind of rotation instead of a shuffle). We'll then
        create a few more fresh decks, and compare the shuffle of those to the
        shuffle of the others. They should all be unique. As mentioned above,
        a true shuffle COULD produce a failure here, however we can probably
        afford to investigate a CI test failure once every few billion years.

        (We could also enforce a known random seed, and validate exactly the
        result we expect. To me, this seems to be straying from reality and
        leaves a lot of room for bad behavior still, so I'm not intending to
        go this way.)
        """

        # Move threshold: We want to insist that at least this many cards moved
        move_threshold = 20
        deck_clean = Deck()
        total_shuffles = 10

        decks = [Deck() for _ in range(total_shuffles)]
        for deck in decks:
            deck.shuffle()

        for i, deck in enumerate(decks):

            # Iterate the shuffled deck and find cards that have different
            # indices than the clean deck. Once we reach the move_threshold, we
            # are satisfied.
            moved = 0
            deltas = []
            for card_index, card in enumerate(deck.cards):
                clean_index = deck_clean.cards.index(card)
                if clean_index == card_index:
                    continue
                moved += 1
                deltas.append(card_index - clean_index)
                if moved == move_threshold:
                    break
            else:
                self.fail(
                    f"Failed to find at least {move_threshold} cards"
                    " that changed position"
                )

            # Check that they didn't all move by the same amount (hard to be
            # confident beyond this that we won't accidentally give a false
            # negative.
            self.assertFalse(all((a == b for a in deltas for b in deltas)))

            # Finally, check that we don't have the same shuffle for any
            # of these decks.
            for j in range(i + 1, total_shuffles):
                deck2 = decks[j]
                for k in range(52):
                    if deck.cards[k] != deck2.cards[k]:
                        break
                else:
                    self.fail("Found two shuffles that were the same!")
            self._sanity_check(deck)

    def test_sort_shuffled(self):
        """
        Tests that shuffled decks get sorted correctly. This assumes that
        the shuffle method functions correctly (tested elsewhere)
        """

        # Test a few shuffles and decks, to make sure they all resolve to
        # a sorted deck
        deck1 = Deck()
        deck2 = Deck()
        deck3 = Deck()

        deck1.shuffle()

        deck2.shuffle()

        deck3.shuffle()
        deck3.shuffle()

        for deck in (deck1, deck2, deck3):
            deck.sort()
            for i in range(52):
                self.assertEqual(TestDeck.ALL_CARDS[i], deck.cards[i])
            self._sanity_check(deck)

    def test_draw_one(self):
        """
        Tests the draw one method
        """
        deck = Deck()
        deck.shuffle()

        for i in range(52):
            self.assertEqual(i, len(deck.pile))
            top_card = deck.cards[0]
            drawn = deck.draw_one()
            self.assertEqual(top_card, drawn)
            self.assertEqual(drawn, deck.pile[i])
            self._sanity_check(deck)

    def test_shuffle_combines(self):
        """
        Tests that shuffling a deck also recombines it with its pile
        """
        draws = 15
        deck = Deck()
        for _ in range(draws):
            deck.draw_one()

        self.assertEqual(len(deck.cards), 52 - draws)
        self.assertEqual(len(deck.pile), draws)

        deck.shuffle()

        self.assertEqual(len(deck.cards), 52)
        self.assertEqual(len(deck.pile), 0)
        self._sanity_check(deck)

    def test_sort_combines(self):
        """
        Tests that sorting a deck also recombines it with its pile
        """
        draws = 15
        deck = Deck()
        for _ in range(draws):
            deck.draw_one()

        self.assertEqual(len(deck.cards), 52 - draws)
        self.assertEqual(len(deck.pile), draws)

        deck.sort()

        self.assertEqual(len(deck.cards), 52)
        self.assertEqual(len(deck.pile), 0)
        self._sanity_check(deck)
