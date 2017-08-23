import numpy as np
import datetime as dt
import time
from workalendar.europe import Poland

from .models import Vacation


def vac_search(accepted, search_from, search_to, query_user):
    found_list = []
    if query_user == '':
        # filters without user parameter
        if accepted == 'all':
            found = Vacation.objects.filter(add_date__range=[search_from, search_to]).order_by('-id')
        else:
            found = Vacation.objects.filter(accepted=accepted,
                                            add_date__range=[search_from, search_to]).order_by('-id')
    else:
        # filters with user parameter
        if accepted == 'all':
            found = Vacation.objects.filter(user__contains=query_user,
                                            add_date__range=[search_from, search_to]).order_by('-id')
        else:
            found = Vacation.objects.filter(user__contains=query_user, accepted=accepted,
                                            add_date__range=[search_from, search_to]).order_by('-id')

    for f in found:
        found_list.append(f)
    return found_list


def apply_dec(vac_edit_obj, decision):
    if decision == 'True':
        vac_edit_obj.accepted = True
        vac_edit_obj.save()
    else:
        if decision == 'False':
            vac_edit_obj.accepted = False
            vac_edit_obj.save()
        else:
            vac_edit_obj.delete()
            return 'deleted'


def count_vac_days(start_date, end_date):
    holidays = []
    start_date_obj = time.strptime(start_date, '%Y-%m-%d')
    end_date_obj = time.strptime(end_date, '%Y-%m-%d')
    start = dt.date(start_date_obj.tm_year, start_date_obj.tm_mon, start_date_obj.tm_mday)
    end = dt.date(end_date_obj.tm_year, end_date_obj.tm_mon, end_date_obj.tm_mday)
    free_days = np.busday_count(start, end) + 1

    # if start and end of vacation in same year
    if start_date_obj.tm_year == end_date_obj.tm_year:
        for i in Poland().holidays(end_date_obj.tm_year):
            # if holiday is not saturday or sunday than its's additional free day
            if i[0].weekday() not in [5, 6]:
                holidays.append(i[0])
    # if vacation start day is in different year than end day
    else:
        for i in Poland().holidays(start_date_obj.tm_year):
            if i[0].weekday() not in [5, 6]:
                holidays.append(i[0])
        for i in Poland().holidays(end_date_obj.tm_year):
            if i[0].weekday() not in [5, 6]:
                holidays.append(i[0])

    delta = end - start
    for i in range(delta.days + 1):
        if (start + dt.timedelta(days=i)) in holidays:
            free_days = free_days - 1
    return free_days



