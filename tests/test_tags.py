import unittest
import datetime
from crm_api.templatetags import date_extras


class TagTestCase(unittest.TestCase):
    def test_last_year(self):
        now = datetime.date.today()
        self.assertIsInstance(date_extras.last_year(), str)
        self.assertEqual(str(now.year - 1), date_extras.last_year())

    def test_last_month(self):
        now = datetime.date.today()
        self.assertIsInstance(date_extras.last_month(now.month), str)
        month = now.month - 1 if now.month > 1 else 12
        self.assertEqual(str(month), date_extras.last_month())
        first = now.replace(day=1)
        last_month = first - datetime.timedelta(days=1)
        self.assertEqual(f'{last_month.month}/{last_month.year}', date_extras.last_month(True))

    def test_deadline_day(self):
        self.assertIsInstance(date_extras._get_deadline_day(1), int)
        for month in range(1, 13):
            self.assertIn(date_extras._get_deadline_day(month), range(25, 30))


if __name__ == '__main__':
    unittest.main()
