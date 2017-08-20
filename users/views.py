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
    if request.method == 'GET':
        form = UserCreationForm
    else:
        form = UserCreationForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            new_user.groups.set([1])
            text = 'User added successfully'
            return render(request, 'panel/index.html', {'text': text})

    context = {'form': form}
    return render(request, 'users/register.html', context)


def access_denied(request):
    return render(request, 'users/access_denied.html')


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def assign_user(request):
    if request == 'GET':
        form = EmployeeForm()
        text = ''
        context = {'form': form, 'text':text}
    else:
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            text = 'User assigned'
            context = {'form': form, 'text':text}
        else:
            form = EmployeeForm()
            text = ''
            context = {'form': form, 'text':text}

    return render(request, 'users/assign_user.html', context)


