import unittest
from cards import Card, Deck, Suit


class TestSuit(unittest.TestCase):

    def testSuitValues(self):
        """
        Test that suits have the correct value
        """
        self.assertEqual(Suit.SPADE, 1)
        self.assertEqual(Suit.DIAMOND, 2)
        self.assertEqual(Suit.HEART, 3)
        self.assertEqual(Suit.CLUB, 4)

    def testAllSuits(self):
        """
        Test that the set of all suits contains the expected
        suits (and no extra)
        """
        for suit in {Suit.SPADE, Suit.DIAMOND, Suit.HEART, Suit.CLUB}:
            self.assertIn(suit, Suit.ALL_SUITS,
                          f'{Suit.PRETTY_NAME[suit]} not found in ALL_SUITS')
        self.assertEqual(len(Suit.ALL_SUITS), 4, 'Incorrect number of suits found')


    def testPrettyNames(self):
        """
        Test that the pretty names are correct
        """
        self.assertEqual(Suit.PRETTY_NAME[Suit.SPADE], 'Spade')
        self.assertEqual(Suit.PRETTY_NAME[Suit.DIAMOND], 'Diamond')
        self.assertEqual(Suit.PRETTY_NAME[Suit.HEART], 'Heart')
        self.assertEqual(Suit.PRETTY_NAME[Suit.CLUB], 'Club')

        self.assertEqual(len(Suit.PRETTY_NAME), 4)


class TestCard(unittest.TestCase):

    def testCardSuitsPositive(self):
        """
        Test creating cards with all the suits
        """
        for suit in Suit.ALL_SUITS:
            card = Card(suit, 2)
            self.assertEqual(card.suit, suit)

    def testCardValuesPositive(self):
        """
        Test creating cards with all the valid values
        """
        for i in range(2, 15):
            card = Card(Suit.SPADE, i)
            self.assertEqual(card.value, i)

    def testBadCardSuit(self):
        """
        Test creating a card with an invalid suit
        """
        for bad_suit in ('bad', -1, 0, 5, 100):
            with self.assertRaises(AssertionError):
                Card(bad_suit, 2)

    def testBadCardValue(self):
        """
        Test creating a card with an invalid value
        """
        for bad_val in ('bad', -1, 0, 1, 15, 100):
            with self.assertRaises(AssertionError):
                Card(Suit.SPADE, bad_val)

    def testCardValueOrdering(self):
        """
        Tests that cards are ordered correctly when suits match
        """
        card3 = Card(Suit.SPADE, 3)
        card2 = Card(Suit.SPADE, 2)
        card10 = Card(Suit.SPADE, 10)

        self.assertLess(card2, card3)
        self.assertLess(card2, card10)
        self.assertLess(card3, card10)

        self.assertGreater(card3, card2)
        self.assertGreater(card10, card2)
        self.assertGreater(card10, card3)

        self.assertLessEqual(card2, card3)
        self.assertLessEqual(card2, card10)
        self.assertLessEqual(card3, card10)

        self.assertGreaterEqual(card3, card2)
        self.assertGreaterEqual(card10, card2)
        self.assertGreaterEqual(card10, card3)

        card2_2 = Card(Suit.SPADE, 2)
        self.assertEqual(card2, card2_2)
        self.assertLessEqual(card2, card2_2)
        self.assertGreaterEqual(card2, card2_2)

    def testCardSuitOrdering(self):
        """
        Tests that Cards are ordered correctly by suit
        """

        spade2 = Card(Suit.SPADE, 2)
        diamond2 = Card(Suit.DIAMOND, 2)
        heart2 = Card(Suit.HEART, 2)
        club2 = Card(Suit.CLUB, 2)

        for lt_pair in ((spade2, diamond2),
                        (spade2, heart2),
                        (spade2, club2),
                        (diamond2, heart2),
                        (diamond2, club2),
                        (heart2, club2)):
            self.assertLess(lt_pair[0], lt_pair[1]
            self.assertLessEqual(lt_pair[0], lt_pair[1]


