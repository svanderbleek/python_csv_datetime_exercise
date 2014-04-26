from filters import DatetimeFilter
import csv
from collections import namedtuple

Restaurant = namedtuple('Restaurant', 'name hours')

def find_open_restaurants(csv_filename, datetime):
  open_filter = DatetimeFilter(datetime)
  with open(csv_filename) as csv_file:
    restaurants = restaurant_rows(csv_file)
    open_restaurants = [restaurant.name for restaurant in restaurants if open_filter(restaurant.hours)]
  return open_restaurants

def restaurant_rows(csv_file):
  rows = csv.reader(csv_file)
  return [Restaurant(*row) for row in rows]
