import unittest
from main import date_to_day
from main import format_time
from main import get_weather_condition


class TestFileName(unittest.TestCase):
    def test_date_to_day_valid_date(self):
        result = date_to_day("2023-06-29T00:00:00Z")
        self.assertEqual(result, "Thursday")

    def test_date_to_day_invalid_date(self):
        result = date_to_day("BLAHASDASDGJG")
        self.assertEqual(result, "Invalid date format. Please use YYYY-MM-DD.")

    def test_format_time(self):
        result = format_time("2023-06-30T23:00:00Z")
        self.assertEqual(result, "2023-06-30 18:00:00")

    def test_get_weather_condition(self):
        result = get_weather_condition("1100")
        self.assertEqual(result, "Mostly Clear")

if __name__ == '__main__':
    unittest.main()
