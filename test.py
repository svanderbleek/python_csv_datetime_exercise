from unittest import TestCase, main
from datetime import datetime, timedelta
from filters import DatetimeFilter
from find_open import find_open_restaurants
import calendar

class DayHour:
  def __init__(self, day, hour):
    try:
      dayhour = datetime.strptime(hour, '%I:%M%p')
    except ValueError:
      dayhour = datetime.strptime(hour, '%I%p')
    weekday = getattr(calendar, day)
    while dayhour.weekday() != weekday:
      dayhour += timedelta(days=1)
    self.datetime = dayhour

  def __repr__(self):
    return self.datetime.strftime('%a %I%p')

class FilterTest(TestCase):
  def filter_test(self, range_string, day_hour, match_value):
    range_filter = DatetimeFilter(day_hour.datetime)
    filter_match = range_filter(range_string)
    self.assertEqual(filter_match, match_value)

  def run_test(self, range_string, assertions):
    print(range_string)
    for assertion in assertions:
      print(assertion)
      self.filter_test(range_string, *assertion)

  def test_simple_range(self):
    simple_range = 'Mon-Sat 11 am - 1 am'
    assertions = (
      (DayHour('MONDAY', '11AM'), True),
      (DayHour('TUESDAY', '12AM'), True),
      (DayHour('SATURDAY', '12PM'), True),
      (DayHour('SUNDAY', '1AM'), True),
      (DayHour('SUNDAY', '2AM'), False),
      (DayHour('MONDAY', '1AM'), False),
      (DayHour('TUESDAY', '2AM'), False)
    )
    self.run_test(simple_range, assertions)

  def test_complex_range(self):
    complex_range = 'Mon-Tue, Thu, Sat-Sun 11 am - 1 am'
    assertions = (
      (DayHour('MONDAY', '11AM'), True),
      (DayHour('TUESDAY', '12AM'), True),
      (DayHour('SATURDAY', '12PM'), True),
      (DayHour('THURSDAY', '11AM'), True),
      (DayHour('FRIDAY', '1AM'), True),
      (DayHour('WEDNESDAY', '11AM'), False)
    )
    self.run_test(complex_range, assertions)

  def test_multiple_range(self):
    multiple_range = 'Mon-Wed 5 pm - 12:30 am / Thu-Fri 5 pm - 1:30 am / Sat 3 pm - 1:30 am'
    assertions = (
      (DayHour('MONDAY', '5pm'), True),
      (DayHour('SATURDAY', '3PM'), True),
      (DayHour('THURSDAY', '1:30AM'), False),
      (DayHour('SATURDAY', '2AM'), False),
      (DayHour('SUNDAY', '11AM'), False)
    )
    self.run_test(multiple_range, assertions)

class OpenRestaurantsTest(TestCase):
  def test_sample_csv(self):
    datetime = DayHour('MONDAY', '10AM').datetime
    open_restaurants = find_open_restaurants('rest_hours.csv', datetime)
    print(open_restaurants)
    self.assertEqual(len(open_restaurants), 6)

main()
