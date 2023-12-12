import unittest
from unittest import mock
from datetime import date, datetime, timedelta
from freezegun import freeze_time
import CalendarDates
import note

class TestKeep(unittest.TestCase):

    def test_keep_data(self):
        keep = note.login()
        keep_result = note.get_note(keep)
        print(keep_result)