from collections import namedtuple
import re
from functools import reduce
from datetime_intervals import Interval

DAYS_HOURS = '(?P<days>\A\D*)(?P<hours>[\dapm\-:]*\Z)'
DAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
RANGE = '-'
GROUP = '/'
LIST = ','
REPLACE = (' ', '')

DaysHours = namedtuple('DaysHours', 'days hours')

def parse_groups(range_string):
  groups = range_string.replace(*REPLACE).split(GROUP)
  return [parse_days_hours(group) for group in groups]

def parse_days_hours(group_string):
  days, hours = parts(DAYS_HOURS, group_string)
  return DaysHours(parse_days(days), parse_hours(hours))

def parse_days(day_string):
  days = day_string.split(LIST)
  expanded = []
  for day in days:
    expanded += expand_range(day)
  return expanded

def expand_range(day):
  days = day.split(RANGE)
  return day_range(*days) if len(days) > 1 else map(day_map, days)

def day_map(day):
  return DAYS.index(day)

def day_range(start_day, end_day):
  start_range = day_map(start_day)
  end_range = day_map(end_day) + 1
  return range(start_range, end_range)

def parse_hours(hour_string):
  return Interval(*hour_string.split(RANGE))

def parts(regex, string):
  return re.search(regex, string).groups()
