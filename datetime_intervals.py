from collections import namedtuple
from datetime import datetime, timedelta

SHIFT_DAY = timedelta(days=1)

Interval = namedtuple('Interval', 'start end')

def datetime_intervals(groups):
  intervals = []
  for group in groups:
    intervals += group_intervals(*group)
  return intervals

def group_intervals(days, hours):
  return [interval(day, hours) for day in days]

def interval(day, hours):
  interval = datetime_interval(day, hours)
  return shift_day(interval) if interval.end <= interval.start else interval

def shift_day(interval):
  end = interval.end + SHIFT_DAY
  return Interval(interval.start, end)

def datetime_interval(day, hours):
  start = normalized_datetime(day, hours.start)
  end = normalized_datetime(day, hours.end)
  return Interval(start, end)

def normalized_datetime(day, hour):
  try:
    normalized = datetime.strptime(hour, '%I:%M%p')
  except ValueError:
    normalized = datetime.strptime(hour, '%I%p')
  while normalized.weekday() != day:
    normalized += SHIFT_DAY
  return normalized
