import unittest
from flashScore import *

class TestFlashScore(unittest.TestCase):

    def test_get_daily_games(self):
        # Test for today
        games = getDailyGames("today")
        self.assertIsNotNone(games)
        self.assertIsInstance(games, list)

        # Test for tomorrow
        games = getDailyGames("tomorrow")
        self.assertIsNotNone(games)
        self.assertIsInstance(games, list)

if __name__ == "__main__":
    unittest.main()
