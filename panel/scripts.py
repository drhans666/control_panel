from datetime import timedelta, date
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
    start = date(start_date.tm_year, start_date.tm_mon, start_date.tm_mday)
    end = date(end_date.tm_year, end_date.tm_mon, end_date.tm_mday)
    free_days = 0
    delta = end - start
    for i in range(delta.days + 1):
        if Poland().is_working_day(start + timedelta(days=i)) is True:
            free_days = free_days + 1
    return free_days





