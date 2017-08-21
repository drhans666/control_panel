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
