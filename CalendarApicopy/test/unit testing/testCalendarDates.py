import unittest
from unittest import mock
from datetime import date, datetime, timedelta
from freezegun import freeze_time
import CalendarDates
from gCalendarApi import Calendar


class TestCalendar(unittest.TestCase):
    @freeze_time("2023-07-09")
    def test_dates_07_09(self):
        calendar = CalendarDates.get_days()
        print(calendar)
        assert calendar[0] == '06-26' and calendar[-1] == '07-23'

    @freeze_time("2023-09-30")
    def test_dates_09_30(self):
        calendar = CalendarDates.get_days()
        print(calendar)
        assert calendar[0] == '09-18' and calendar[-1] == '10-15'

    @freeze_time("2023-07-10")
    def test_event_boundary_07_10(self):
        print("now: " + str(datetime.now()))
        email = 'hanxiaoyu0628@googlemail.com'
        password = 'lxjldcndhfogsrml'

        calendar = Calendar()
        calendar.login(email, password)
        events = calendar.get()
        print(events.keys())
        print(events['07-29'])
        assert('07-03' in events.keys()) and '07-30' in events.keys()


    @freeze_time("2023-07-9")
    def test_event_boundary_07_09(self):
        print("now: " + str(datetime.now()))
        email = 'hanxiaoyu0628@googlemail.com'
        password = 'lxjldcndhfogsrml'

        calendar = Calendar()
        calendar.login(email, password)
        events = calendar.get()

        print(events.keys())
        assert('06-25' in events.keys()) and ('07-23' in events.keys())



'''

@freeze_time("2012-01-01")
def test_something():

    from datetime import datetime
    print(datetime.now()) #  2012-01-01 00:00:00

    from datetime import date
    print(date.today()) #  2012-01-01

test_something()
'''