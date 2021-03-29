import unittest
from unittest import mock
from io import StringIO
from cards import Card, Deck, Suit
from game import Game, Player


class TestPlayer(unittest.TestCase):
    """ Tests for the Player class """

    def testSimpleCreation(self):
        """
        Tests that players get initialized in a sane way
        """
        deck = Deck()
        player = Player(deck)
        self.assertEqual(player.hand, [])
        self.assertEqual(id(deck), id(player.deck))
        self.assertEqual(player.hand_value, 0)

    def testPlayersShareDeck(self):
        """
        Tests that players created with the same deck are sharing it between
        them. We are validating IDs here, which may be implementation dependent
        """
        deck = Deck()
        player1 = Player(deck)
        player2 = Player(deck)

        self.assertEqual(id(player1.deck), id(player2.deck))
        player1.draw_one()
        self.assertEqual(len(player2.deck.cards), 51)
        self.assertEqual(player1.hand[0], player2.deck.pile[0])

    def testReset(self):
        """
        Tests that reset works correctly
        """
        deck = Deck()
        player = Player(deck)

        previous_score = player.hand_value

        for i in range(10):
            player.draw_one()
            self.assertEqual(len(player.hand), i + 1)
            self.assertGreater(player.hand_value, previous_score)
            previous_score = player.hand_value

        player.reset()
        self.assertEqual(player.hand, [])
        self.assertEqual(player.hand_value, 0)

    def testHandValue(self):
        """
        Tests that the hand value is calculated as the sum of individual cards
        """
        deck = Deck()
        player = Player(deck)
        card1 = Card(Suit.SPADE, 2)
        card2 = Card(Suit.DIAMOND, 6)
        card3 = Card(Suit.HEART, 13)

        player.hand = [card1]
        self.assertEqual(player.hand_value, card1.points)

        player.hand = [card1, card2]
        self.assertEqual(player.hand_value, card1.points + card2.points)

        player.hand = [card1, card2, card3]
        self.assertEqual(player.hand_value, card1.points +
                                            card2.points +
                                            card3.points)

class TestGame(unittest.TestCase):
    """ Tests for the Game class """

    def test_fairness(self):
        """
        Assume that on large data sets, we should be roughly even in win
        percentages, as the shuffle should be random, and players have equal
        expected values.
        """
        # Games to run and number of decimal places to look at the win ratio
        # We can increase iterations and tolerance for more confidence, at the
        # expense of execution time
        iterations = 10000
        tolerance = 1

        g = Game(quiet=True)
        win_count = {g.player1: 0, g.player2: 0}

        for i in range(iterations):
            winner = g.play()
            if winner != None:
                win_count[winner] += 1

        win_ratio = win_count[g.player1] / win_count[g.player2]

        self.assertAlmostEqual(1.0, win_ratio, tolerance)
        self.assertNotEqual(win_count[g.player1], 0)
        self.assertNotEqual(win_count[g.player2], 0)

    def testDrawCards(self):
        """
        Tests that drawing cards functions correctly
        """
        game = Game(quiet=True)
        game.draw_cards()
        self.assertEqual(len(game.player1.hand), 3)
        self.assertEqual(len(game.player2.hand), 3)

    def testComparePlayer1Wins(self):
        """
        Tests comparing hands and player1 has more points
        """
        game = Game()

        # 25 points
        game.player1.hand = [Card(Suit.SPADE, 2),
                             Card(Suit.SPADE, 3),
                             Card(Suit.CLUB, 5)]

        # 24 points
        game.player2.hand = [Card(Suit.SPADE, 4),
                             Card(Suit.SPADE, 5),
                             Card(Suit.HEART, 5)]
        with mock.patch('sys.stdout', new = StringIO()) as output:
            self.assertEqual(game.compare_hands(), game.player1)
            expected_output = ('Player 1 scores 25 points!\n'
                               'Player 2 scores 24 points!\n'
                               'Player 1 wins!\n')
            self.assertEqual(output.getvalue(), expected_output)

    def testComparePlayer2Wins(self):
        """
        Tests comparing hands and player2 has more points
        """
        game = Game()

        # 24 points
        game.player1.hand = [Card(Suit.SPADE, 4),
                             Card(Suit.SPADE, 5),
                             Card(Suit.HEART, 5)]

        # 25 points
        game.player2.hand = [Card(Suit.SPADE, 2),
                             Card(Suit.SPADE, 3),
                             Card(Suit.CLUB, 5)]
        with mock.patch('sys.stdout', new = StringIO()) as output:
            self.assertEqual(game.compare_hands(), game.player2)
            expected_output = ('Player 1 scores 24 points!\n'
                               'Player 2 scores 25 points!\n'
                               'Player 2 wins!\n')
            self.assertEqual(output.getvalue(), expected_output)

    def testCompareNeitherPlayerWins(self):
        """
        Tests comparing hands and players tie
        """
        game = Game()

        # 25 points
        game.player1.hand = [Card(Suit.SPADE, 4),
                             Card(Suit.SPADE, 6),
                             Card(Suit.HEART, 5)]

        # 25 points
        game.player2.hand = [Card(Suit.SPADE, 2),
                             Card(Suit.SPADE, 3),
                             Card(Suit.CLUB, 5)]
        with mock.patch('sys.stdout', new = StringIO()) as output:
            self.assertIsNone(game.compare_hands())
            expected_output = ('Player 1 scores 25 points!\n'
                               'Player 2 scores 25 points!\n'
                               'Players tie and there is no winner!\n')
            self.assertEqual(output.getvalue(), expected_output)

    def testPlay(self):
        """
        Test playing a full game and then repeating with the same players
        (elsewhere we test that outcomes are different).
        """
        game = Game(quiet=True)
        games = 20

        for _ in range(games):
            winner = game.play()

            self.assertEqual(len(game.player1.hand), 3)
            self.assertEqual(len(game.player2.hand), 3)

            if game.player1.hand_value > game.player2.hand_value:
                self.assertEqual(winner, game.player1)
            elif game.player1.hand_value < game.player2.hand_value:
                self.assertEqual(winner, game.player2)
            else:
                self.assertIsNone(winner)

    def testPrintedMessagesDrawCards(self):
        """
        Tests that friendly messages are printed for game conditions
        """
        game = Game()
        with mock.patch('sys.stdout', new = StringIO()) as output:
            expected_output = ('Player 1 draws 2 of Spades\n'
                               'Player 2 draws 3 of Spades\n'
                               '--------\n'
                               'Player 1 draws 4 of Spades\n'
                               'Player 2 draws 5 of Spades\n'
                               '--------\n'
                               'Player 1 draws 6 of Spades\n'
                               'Player 2 draws 7 of Spades\n'
                               '--------\n')
            game.draw_cards()
            self.assertEqual(output.getvalue(), expected_output)


