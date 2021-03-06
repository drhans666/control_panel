import time
from datetime import date, timedelta
from django.contrib.auth.models import User
from django.test import TestCase

from .scripts import count_vac_days, vacnow_search_append, vac_search
from .models import Vacation


class CountVacDaysTest(TestCase):

    def test_all_free_days(self):
        start_date = time.strptime('2017-9-4', '%Y-%m-%d')
        end_date = time.strptime('2017-9-8', '%Y-%m-%d')
        freedays = count_vac_days(start_date, end_date)

        self.assertEqual(freedays, 5)

    def test_weekend_days(self):
        start_date = time.strptime('2017-9-8', '%Y-%m-%d')
        end_date = time.strptime('2017-9-11', '%Y-%m-%d')
        freedays = count_vac_days(start_date, end_date)

        self.assertEqual(freedays, 2)

    def test_holidays(self):
        start_date = time.strptime('2017-8-14', '%Y-%m-%d')
        end_date = time.strptime('2017-8-18', '%Y-%m-%d')
        freedays = count_vac_days(start_date, end_date)

        self.assertEqual(freedays, 4)

    def test_years(self):
        start_date = time.strptime('2017-12-31', '%Y-%m-%d')
        end_date = time.strptime('2018-1-4', '%Y-%m-%d')
        freedays = count_vac_days(start_date, end_date)

        self.assertEqual(freedays, 3)


class OnVacationTest(TestCase):

    def setUp(self):
        User.objects.create(username='tester')
        User.objects.create(username='tester2')

    def test_one_on_vacation(self):
        user1 = User.objects.get(username='tester')
        user2 = User.objects.get(username='tester2')
        Vacation.objects.create(accepted=True, user=user1)
        Vacation.objects.create(accepted=False, user=user2)

        found, days_list = vacnow_search_append()
        self.assertEqual(len(found), 1)
        self.assertEqual(days_list[0], '1 day')

    def test_none_on_vacation(self):
        user1 = User.objects.get(username='tester')
        user2 = User.objects.get(username='tester2')
        Vacation.objects.create(accepted=False, user=user1)
        Vacation.objects.create(accepted=False, user=user2)

        found, days_list = vacnow_search_append()
        self.assertEqual(len(found), 0)
        self.assertEqual(days_list, [])

    def test_border_dates(self):
        user1 = User.objects.get(username='tester')
        user2 = User.objects.get(username='tester2')
        start_date = (date.today() - timedelta(days=10))
        end_date = date.today() + timedelta(days=10)

        Vacation.objects.create(accepted=True, user=user1,
                                start_date=date.today(),
                                end_date=end_date)
        Vacation.objects.create(accepted=True, user=user2,
                                start_date=start_date,
                                end_date=date.today())

        found, days_list = vacnow_search_append()
        self.assertEqual(len(found), 2)
        self.assertEqual(days_list[0], '1 day')
        self.assertEqual(days_list[1], '11 days')


class VacationSearchTest(TestCase):

    def setUp(self):
        user1 = User.objects.create(username='tester')
        user2 = User.objects.create(username='tester2')
        Vacation.objects.create(accepted=True, user=user1,
                                add_date=date.today() + timedelta(days=3),
                                start_date=date.today() - timedelta(days=5),
                                end_date=date.today() - timedelta(days=3))
        Vacation.objects.create(accepted=False, user=user2,
                                start_date=date.today(),
                                end_date=date.today())

    def test_date_search(self):
        autodate_override = date.today() - timedelta(days=7)
        Vacation.objects.filter(user__username='tester').update(add_date=autodate_override)
        accepted = 'All'
        query_user = None
        search_from = date.today() - timedelta(days=5)
        search_to = str(date.today()) + ' 23:59:59'
        found_list = vac_search(accepted, search_from, search_to, query_user)

        self.assertEqual(len(found_list), 1)

    def test_accept_search(self):
        accepted = True
        query_user = None
        search_from = date.today()
        search_to = str(date.today()) + ' 23:59:59'
        found_list = vac_search(accepted, search_from, search_to, query_user)

        self.assertEqual(len(found_list), 1)
        self.assertEqual(found_list[0].user.username, 'tester')

    def test_user_search(self):
        accepted = 'All'
        query_user = User.objects.filter(username='tester2')
        search_from = date.today()
        search_to = str(date.today()) + ' 23:59:59'
        found_list = vac_search(accepted, search_from, search_to, query_user)

        self.assertEqual(len(found_list), 1)
        self.assertEqual(found_list[0].user.username, 'tester2')