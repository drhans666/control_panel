from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import Anon
from .forms import AnonForm


@login_required()
def all_anon(request):
    anon_list = Anon.objects.all().order_by('-id')

    return render(request, 'announcements/all_anon.html', {'anon_list': anon_list})


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def new_anon(request):
    form = AnonForm(request.POST or None)
    context = {'form': form}

    if request.method == 'GET' or not form.is_valid():
        return render(request, 'announcements/new_anon.html', context)

    model = form.save(commit=False)
    model.owner = request.user
    model.save()
    messages.success(request, 'Announcement posted.')

    return HttpResponseRedirect(reverse('announcements:new_anon'))


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def edit_anon(request, anon_id):
    model = Anon.objects.get(id=anon_id)
    form = AnonForm(instance=model, data=request.POST or None)
    context = {'form': form, 'anon_edit_obj': model}

    if request.method == 'GET' or not form.is_valid():
        return render(request, 'announcements/edit_anon.html', context)

    form.save()
    messages.success(request, 'Announcement edited successfully.')
    return HttpResponseRedirect(reverse('announcements:edit_anon', args=[anon_id]))
