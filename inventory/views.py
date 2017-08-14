from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Item, Section
from .forms import ItemForm, ItemLocationForm, QueryForm, ManufacturerForm, CategoryForm, SectionForm
from .scripts import search_items, check_category_section


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def add_to_section(request):
    if request.method == 'GET':
        if request.method == 'GET':
            form = ItemLocationForm()
            text = ''
            context = {'form': form, 'text': text}
            return render(request, 'inventory/add_to_section.html', context)
    else:
        form = ItemLocationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            text = 'Item added to section'
            form = ItemLocationForm()
            context = {'form': form, 'text': text}
            return render(request, 'inventory/add_to_section.html', context)
        else:
            text = 'Item added'
            context = {'form': form, 'text': text}
            return render(request, 'inventory/add_to_section.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def new_item(request):
    if request.method == 'GET':
        form = ItemForm()
        context = {'form': form}
        return render(request, 'inventory/new_item.html', context)
    else:
        form = ItemForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name').capitalize()
            form.save()
            text = '%s saved successfully' % name
            form = ItemForm()
            context = {'form': form, 'text': text}
            return render(request, 'inventory/new_item.html', context)
        else:
            text = 'Form Error'
            context = {'form': form, 'text': text}
            return render(request, 'inventory/new_item.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def show_items(request):
    if request.method == 'GET':
        form = QueryForm()

        return render(request, 'inventory/show_items.html', {'form': form})
    else:
        form = QueryForm(request.POST)
        if form.is_valid():
            item = request.POST.get('item')
            item = str(item).upper()
            manufacturer = request.POST.get('manufacturer')
            manufacturer = str(manufacturer).upper()
            cat = request.POST.getlist('category')
            sect = request.POST.getlist('section')
            cat, sect = check_category_section(cat, sect)
            found_list = search_items(item, manufacturer, cat, sect)

            form = QueryForm()
            context = {'found_list': found_list, 'form': form}

            return render(request, 'inventory/show_items.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def add_category(request):
    if request.method == 'GET':
        form = CategoryForm()
        text = ''
        context = {'form': form, 'text': text}
        return render(request, 'inventory/add_category.html', context)
    else:
        form = CategoryForm(request.POST)
        if not form.is_valid():
            form = CategoryForm()
            text = 'Form error'
            context = {'form': form, 'text': text}
            return render(request, 'inventory/add_category.html', context)
        else:
            name = request.POST.get('name').capitalize()
            form.save()
            text = '%s category added' % name
            context = {'form': form, 'text': text}
            return render(request, 'inventory/add_category.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def add_manufacturer(request):
    if request.method == 'GET':
        form = ManufacturerForm()
        text = ''
        context = {'form': form, 'text': text}
        return render(request, 'inventory/add_manufacturer.html', context)
    else:
        form = ManufacturerForm(request.POST)
        if not form.is_valid():
            form = ManufacturerForm()
            text = 'Form error'
            context = {'form': form, 'text': text}
            return render(request, 'inventory/add_manufacturer.html', context)
        else:
            name = request.POST.get('name').capitalize()
            form.save()
            text = '%s manufacturer added' % name
            context = {'form': form, 'text': text}
            return render(request, 'inventory/add_manufacturer.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def new_section(request):
    if request.method == 'GET':
        form = SectionForm()
        text = ''
        context = {'form': form, 'text': text}
        return render(request, 'inventory/new_section.html', context)
    else:
        form = SectionForm(request.POST)
        if not form.is_valid():
            form = SectionForm()
            text = 'Form error'
            context = {'form': form, 'text': text}
            return render(request, 'inventory/new_section.html', context)
        else:
            name = request.POST.get('name').capitalize()
            form.save()
            text = '%s section added' % name
            context = {'form': form, 'text': text}
            return render(request, 'inventory/new_section.html', context)


def stocktaking(request):
    return render(request, 'inventory/stocktaking.html')