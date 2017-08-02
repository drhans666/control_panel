from datetime import date
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import VacationForm, VacQuery, VacVerify
from .models import Vacation
from .scripts import vac_search, apply_dec





def index(request):
    text = 'hello costam'
    return render(request, 'panel/index.html', {'text': text})


@login_required()
def vacat_form(request):
    if request.method == 'GET':
        form = VacationForm()
        text = ''
    else:
        form = VacationForm(request.POST)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        if form.is_valid() and start_date <= end_date:
            user_overrid = form.save(commit=False)
            user_overrid.user = request.user
            user_overrid.save()
            text = 'Vacation submitted successfullyy'
            return render(request, 'panel/index.html', {'text': text})

        else:
            form = VacationForm()
            text = 'Form Error. Try Again'

    context = {'form': form, 'text': text}
    return render(request, 'panel/vacat_form.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def vac_query(request):
    if request.method == 'GET':
        form = VacQuery
    else:
        form = VacQuery(request.POST)
        if form.is_valid():
            accepted = request.POST.get('accepted')
            search_from = request.POST.get('search_from')
            search_to = request.POST.get('search_to')
            search_to = str(search_to) + ' 23:59:59'
            query_user = request.POST.get('query_user')
            found_list = vac_search(accepted, search_from, search_to, query_user)
            context = {'form': form, 'found_list': found_list}
            return render(request, 'panel/vac_query.html', context)

        else:
            form = VacQuery
    context = {'form': form}
    return render(request, 'panel/vac_query.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def vac_edit(request, vac_id):
    vac_edit_obj = Vacation.objects.get(id=vac_id)
    if request.method == 'GET':
        form = VacVerify()
        text = ''
        context = {'form': form, 'vac_edit_obj': vac_edit_obj, 'text': text}
        return render(request, 'panel/vac_edit.html', context)

    else:
        form = VacVerify(request.POST)
        if not form.is_valid():
            form = VacVerify()
            text = 'Form error'
            context = {'form': form, 'vac_edit_obj': vac_edit_obj, 'text': text}
            return render(request, 'panel/vac_edit.html', context)

        decision = request.POST.get('decision')
        return_dec = apply_dec(vac_edit_obj, decision)
        if return_dec == 'deleted':
            form = VacQuery
            context = {'form': form}
            return render(request, 'panel/vac_query.html', context)

        return HttpResponseRedirect(reverse('panel:vac_edit', args=[vac_id]))

@login_required()
def vac_now(request):
    days_list = []
    found = Vacation.objects.filter(accepted=True, end_date__gte=date.today() ).order_by('end_date')
    for f in found:
        days = f.end_date - date.today()
        days_list.append(str(days)[:-9])
    lists = zip(found, days_list)

    context = {'lists':lists}
    return render(request, 'panel/vac_now.html', context)
