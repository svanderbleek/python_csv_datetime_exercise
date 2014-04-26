from parsers import parse_groups
from datetime_intervals import datetime_intervals, normalized_datetime

class DatetimeFilter:
  NORMALIZE = (1990, 1, 1)

  def __init__(self, datetime):
    day = datetime.weekday()
    hour = datetime.strftime('%I:%M%p')
    self.datetime = normalized_datetime(day, hour)

  def __call__(self, range_string):
    groups = parse_groups(range_string)
    intervals = datetime_intervals(groups)
    return any([interval.start <= self.datetime <= interval.end for interval in intervals])
