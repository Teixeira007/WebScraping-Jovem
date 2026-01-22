import unittest
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from monitor import Monitor

class TestMonitor(unittest.TestCase):
    def setUp(self):
        self.monitor = Monitor()

    def test_generate_dates_single_day(self):
        dates = self.monitor.generate_dates("2026-03-01", "2026-03-01")
        self.assertEqual(dates, ["2026-03-01"])

    def test_generate_dates_range(self):
        dates = self.monitor.generate_dates("2026-03-01", "2026-03-03")
        self.assertEqual(dates, ["2026-03-01", "2026-03-02", "2026-03-03"])
        self.assertEqual(len(dates), 3)

    def test_generate_dates_cross_month(self):
        dates = self.monitor.generate_dates("2026-02-28", "2026-03-02")
        # Assuming 2026 is not a leap year (it is not)
        expected = ["2026-02-28", "2026-03-01", "2026-03-02"]
        self.assertEqual(dates, expected)

if __name__ == '__main__':
    unittest.main()
