from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


from .forms import ItemForm, ItemLocationForm, QueryForm, ManufacturerForm,\
    CategoryForm, SectionForm, SimpleSearch
from .scripts import search_items, check_category_section, simple_item_search


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def add_to_section(request):
    form = ItemLocationForm(request.POST or None)
    context = {'form': form, 'text': ''}

    if not form.is_valid():
        return render(request, 'inventory/add_to_section.html', context)

    model = form.save(commit=False)
    model.user = request.user
    model.save()

    context = {'form': ItemLocationForm(), 'text': 'Item added to section'}
    return render(request, 'inventory/add_to_section.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def new_item(request):
    form = ItemForm(request.POST or None)
    context = {'form': form, 'text': ''}

    if request.method == 'GET':
        return render(request, 'inventory/new_item.html', context)

    if not form.is_valid():
        context['text'] = 'Form Error'
        return render(request, 'inventory/new_item.html', context)

    form.save()
    context = {'form': ItemForm(), 'text': '%s saved successfully' % request.POST.get('name').capitalize()}
    return render(request, 'inventory/new_item.html', context)


@login_required()
def simple_search(request):
    form = SimpleSearch(request.POST or None)
    context = {'form': form}

    if request.method == 'GET' or not form.is_valid():
        return render(request, 'inventory/simple_search.html', context)

    item = str(request.POST.get('item')).upper()
    manufacturer = str(request.POST.get('manufacturer')).upper()
    section = request.POST.getlist('section')
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
    cat = request.POST.getlist('category')
    sect = request.POST.getlist('section')
    cat, sect = check_category_section(cat, sect)
    context = {'form': QueryForm(), 'found_list': search_items(item, manufacturer, cat, sect)}

    return render(request, 'inventory/show_items_adv.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def add_category(request):
    form = CategoryForm(request.POST or None)
    context = {'form': form, 'text': ''}
    if request.method == 'GET':
        return render(request, 'inventory/add_category.html', context)

    if not form.is_valid():
        context['text'] = 'Form Error'
        return render(request, 'inventory/add_category.html', context)

    name = request.POST.get('name').capitalize()
    form.save()
    context['text'] = '%s category added' % name
    return render(request, 'inventory/add_category.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def add_manufacturer(request):
    form = ManufacturerForm(request.POST or None)
    context = {'form': form, 'text': ''}

    if request.method == 'GET':
        return render(request, 'inventory/add_manufacturer.html', context)

    if not form.is_valid():
        context['text'] = 'Form Error'
        return render(request, 'inventory/add_manufacturer.html', context)

    name = request.POST.get('name').capitalize()
    form.save()
    context['text'] = '%s manufacturer added' % name
    return render(request, 'inventory/add_manufacturer.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def new_section(request):
    form = SectionForm(request.POST or None)
    context = {'form': form, 'text': ''}

    if request.method == 'GET':
        return render(request, 'inventory/new_section.html', context)

    if not form.is_valid():
        context['text'] = 'Form Error'
        return render(request, 'inventory/new_section.html', context)

    name = request.POST.get('name').capitalize()
    form.save()
    context['text'] = '%s section added' % name
    return render(request, 'inventory/new_section.html', context)
