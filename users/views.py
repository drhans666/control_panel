from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import EmployeeForm


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('panel:index'))


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def register(request):
    form = UserCreationForm(request.POST or None)
    context = {'form': form}

    if request.method == 'GET' or not form.is_valid():
        return render(request, 'users/register.html', context)

    model = form.save()
    model.groups.set([1])
    context['text'] = 'User added successfully'
    return render(request, 'panel/index.html', context)


def access_denied(request):
    return render(request, 'users/access_denied.html')


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def assign_user(request):
    form = EmployeeForm(request.POST or None)
    context = {'form': form, 'text': ''}

    if request.method == 'GET' or not form.is_valid():
        return render(request, 'users/assign_user.html', context)

    form.save()
    context['text'] = 'User assigned'

    return render(request, 'users/assign_user.html', context)
