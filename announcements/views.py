from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

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
    if request.method == 'GET':
        form = AnonForm
    else:
        form = AnonForm(request.POST)
        if form.is_valid():
            new_anon = form.save(commit=False)
            new_anon.owner = request.user
            new_anon.save()
            text = "Announcement Saved"
            return render(request, 'panel/index.html', {'text': text})
    return render(request, 'announcements/new_anon.html', {'form': form})


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def edit_anon(request, anon_id):
    anon_edit_obj = Anon.objects.get(id=anon_id)
    if request.method != 'POST':
        # pre-fill form with the current anon
        form = AnonForm(instance=anon_edit_obj)
    else:
        form = AnonForm(instance=anon_edit_obj, data=request.POST)
        if form.is_valid():
            form.save()
            text = "Announcement Edited Successfully"
            return render(request, 'panel/index.html', {'text': text})
    context = {'form': form, 'anon_edit_obj': anon_edit_obj}
    return render(request, 'announcements/edit_anon.html', context)
