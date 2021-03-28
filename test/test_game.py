import unittest
from game import Game


class TestGame(unittest.TestCase):
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
