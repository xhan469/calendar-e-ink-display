import unittest
from unittest import mock
from datetime import date, datetime, timedelta
from freezegun import freeze_time
import CalendarDates
from gCalendarApi import Calendar
import setup


class TestTime(unittest.TestCase):
    @freeze_time("2023-07-31")
    def test_time_07_10(self):
        email = 'hanxiaoyu0628@googlemail.com'
        password = 'lxjldcndhfogsrml'

        calendar = Calendar()
        calendar.login(email, password)
        events = calendar.get()


        event_dict = setup.check_time(events)
        for key in event_dict.keys():
            print(key, event_dict[key])


    @freeze_time("2023-07-10")
    def test_today_07_10(self):
        today = setup.check_today('07-11')
        assert today == False

    @freeze_time("2023-07-22")
    def test_today_07_10(self):
        today = setup.check_today('07-22')
        assert today == True



    def test_max_event(self):
        email = 'hanxiaoyu0628@googlemail.com'
        password = 'lxjldcndhfogsrml'

        calendar = Calendar()
        calendar.login(email, password)
        events = calendar.get()

        result = setup.max_four_event(events)

        for key in result.keys():
            print(result[key])
