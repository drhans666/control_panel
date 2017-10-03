from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


from .forms import ItemForm, ItemLocationForm, QueryForm, ManufacturerForm,\
    CategoryForm, SectionForm, SimpleSearch
from .scripts import adv_search_items, check_category_section, simple_item_search



@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def add_to_section(request):
    form = ItemLocationForm(request.POST or None)
    context = {'form': form}

    if not form.is_valid():
        return render(request, 'inventory/add_to_section.html', context)

    model = form.save(commit=False)
    model.user = request.user
    model.save()
    messages.success(request, 'Item added to section.')
    return HttpResponseRedirect(reverse('inventory:add_to_section'))


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def new_item(request):
    form = ItemForm(request.POST or None)
    context = {'form': form}

    if request.method == 'GET':
        return render(request, 'inventory/new_item.html', context)

    if not form.is_valid():
        messages.error(request, 'Form error')
        return render(request, 'inventory/new_item.html', context)

    form.save()
    messages.success(request, 'New item: %s added.' % request.POST.get('name').capitalize())
    return HttpResponseRedirect(reverse('inventory:new_item'))


@login_required()
def simple_search(request):
    form = SimpleSearch(request.POST or None)
    context = {'form': form}

    if request.method == 'GET' or not form.is_valid():
        return render(request, 'inventory/simple_search.html', context)

    item = str(request.POST.get('item')).upper()
    manufacturer = str(request.POST.get('manufacturer')).upper()
    section = request.POST.get('section')
    context['results'] = simple_item_search(item, manufacturer, section)

    return render(request, 'inventory/simple_search.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def show_items_adv(request):
    form = QueryForm(request.POST or None)
    context = {'form': form, 'found_list': []}

    if request.method == 'GET' or not form.is_valid():
        return render(request, 'inventory/show_items_adv.html', context)

    item = str(request.POST.get('item')).upper()
    manufacturer = str(request.POST.get('manufacturer')).upper()
    category = request.POST.getlist('category')
    section = request.POST.getlist('section')
    category, section = check_category_section(category, section)
    context = {'form': QueryForm(), 'found_list': adv_search_items(item, manufacturer, category, section)}

    return render(request, 'inventory/show_items_adv.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def add_category(request):
    form = CategoryForm(request.POST or None)
    context = {'form': form}
    if request.method == 'GET':
        return render(request, 'inventory/add_category.html', context)

    if not form.is_valid():
        messages.error(request, 'Form Error')
        return render(request, 'inventory/add_category.html', context)

    form.save()
    messages.success(request, '%s category added' % request.POST.get('name').capitalize())
    return HttpResponseRedirect(reverse('inventory:add_category'))


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def add_manufacturer(request):
    form = ManufacturerForm(request.POST or None)
    context = {'form': form}

    if request.method == 'GET':
        return render(request, 'inventory/add_manufacturer.html', context)

    if not form.is_valid():
        messages.error(request, 'Form error')
        return render(request, 'inventory/add_manufacturer.html', context)

    form.save()
    messages.success(request, '%s manufacturer added' % request.POST.get('name').capitalize())
    return HttpResponseRedirect(reverse('inventory:add_manufacturer'))


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def new_section(request):
    form = SectionForm(request.POST or None)
    context = {'form': form}

    if request.method == 'GET':
        return render(request, 'inventory/new_section.html', context)

    if not form.is_valid():
        messages.error(request, 'Form error')
        return render(request, 'inventory/new_section.html', context)

    form.save()
    messages.success(request, '%s section added' % request.POST.get('name').capitalize())
    return HttpResponseRedirect(reverse('inventory:new_section'))




