import unittest
from appweb.apprun import calculate_winrate, get_match_duration_distribution, get_games_per_game_mode

class TestAppFunctions(unittest.TestCase):

    def test_calculate_winrate(self):
        matches = [{"radiant_win": True}, {"radiant_win": False}, {"radiant_win": True}]
        radiant, dire = calculate_winrate(matches)
        self.assertAlmostEqual(radiant, 66.66666666666667, places=2)  # Allows small deviations
        self.assertAlmostEqual(dire, 33.33333333333333, places=2)


    def test_get_games_per_game_mode(self):
        matches = [{"game_mode": 22}, {"game_mode": 3}, {"game_mode": 22}]
        game_mode_distribution = get_games_per_game_mode(matches)
        expected = {"All Pick Ranked": 2, "Random Draft": 1}
        self.assertEqual(game_mode_distribution, expected)

if __name__ == "__main__":
    unittest.main()
