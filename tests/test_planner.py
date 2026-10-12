import unittest
from src.planner import assess, answer_question, plan_week

class PlannerTests(unittest.TestCase):
    def row(self, day="Monday", temp=28, rain=10, aqi=40, wind=10, available=True):
        return {
            "Day": day, "Temperature °C": temp, "Rain chance %": rain,
            "AQI": aqi, "Wind km/h": wind, "Available": available
        }

    def test_unavailable_day_is_rejected(self):
        status, score, warnings, explanation = assess(self.row(available=False), "Cycling")
        self.assertEqual(status, "Not recommended")

    def test_high_rain_warns_for_picnic(self):
        status, score, warnings, explanation = assess(self.row(rain=90), "Picnic")
        self.assertIn("High rain chance", warnings)

    def test_backward_chaining_returns_trace(self):
        result = answer_question(self.row(), "Cycling")
        self.assertTrue(len(result["trace"]) >= 3)

    def test_week_plan_has_seven_days(self):
        rows = [self.row(day=d) for d in
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]
        result = plan_week(rows, "Cycling")
        self.assertEqual(len(result["plan"]), 7)

if __name__ == "__main__":
    unittest.main()
