import time

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import VacationForm, VacQuery, VacVerify
from .models import Vacation
from .scripts import vac_search, apply_dec, count_vac_days, vacnow_search_append


def index(request):
    user = request.user
    text = 'Hello ' + str(user)
    return render(request, 'panel/index.html', {'text': text})


@login_required()
def vacat_form(request):
    form = VacationForm(request.POST or None)
    context = {'form': form}

    if request.method == 'GET':
        return render(request, 'panel/vacat_form.html', context)

    if not form.is_valid():
        messages.error(request, 'Form error')
        return render(request, 'panel/vacat_form.html', context)

    start_date = time.strptime(request.POST.get('start_date'), '%Y-%m-%d')
    end_date = time.strptime(request.POST.get('end_date'), '%Y-%m-%d')
    model = form.save(commit=False)
    model.vac_days = count_vac_days(start_date, end_date)
    model.user = request.user
    model.save()
    messages.success(request, 'Form sent successfully')
    return HttpResponseRedirect(reverse('panel:vacat_form'))


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def vac_query(request):
    form = VacQuery(request.POST or None)
    context = {'form': form}

    if request.method == 'GET' or not form.is_valid():
        return render(request, 'panel/vac_query.html', context)

    accepted = request.POST.get('accepted')
    search_from = request.POST.get('search_from')
    search_to = request.POST.get('search_to')
    search_to = str(search_to) + ' 23:59:59'
    query_user = request.POST.get('query_user')
    context['found_list'] = vac_search(accepted, search_from, search_to, query_user)
    return render(request, 'panel/vac_query.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def vac_edit(request, vac_id):
    vac_edit_obj = Vacation.objects.get(id=vac_id)
    form = VacVerify(request.POST or None)
    context = {'form': form, 'vac_edit_obj': vac_edit_obj}

    if request.method == 'GET':
        return render(request, 'panel/vac_edit.html', context)

    if not form.is_valid():
        messages.error(request, 'Form error')
        return render(request, 'panel/vac_edit.html', context)

    decision = request.POST.get('decision')
    return_dec = apply_dec(vac_edit_obj, decision)
    if return_dec == 'deleted':
        context = {'form': VacQuery()}
        messages.success(request, 'Vacation request deleted')
        return render(request, 'panel/vac_query.html', context)

    messages.success(request, 'Vacation status changed')
    return HttpResponseRedirect(reverse('panel:vac_edit', args=[vac_id]))


@login_required()
def vac_now(request):
    found, days_list = vacnow_search_append()
    lists = zip(found, days_list)
    context = {'lists': lists}
    return render(request, 'panel/vac_now.html', context)
