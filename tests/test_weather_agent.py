import unittest
from src.weather_agent import recommend_activity


class TestWeatherAgent(unittest.TestCase):

    def test_sunny_weather(self):
        result = recommend_activity(28, "sunny", "low")
        self.assertIn("Outdoor activity", result)

    def test_rainy_weather(self):
        result = recommend_activity(25, "rainy", "moderate")
        self.assertIn("Indoor activity", result)

    def test_high_temperature(self):
        result = recommend_activity(36, "sunny", "low")
        self.assertIn("Indoor activity", result)

    def test_high_wind(self):
        result = recommend_activity(20, "cloudy", "high")
        self.assertIn("Indoor activity", result)

    def test_unknown_weather(self):
        result = recommend_activity(22, "foggy", "low")
        self.assertIn("Indoor activity", result)


if __name__ == "__main__":
    unittest.main()