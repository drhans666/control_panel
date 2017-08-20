from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User



from .models import Stocktaking, Item, Section
from .forms import ItemForm, ItemLocationForm, QueryForm, ManufacturerForm,\
    CategoryForm, SectionForm, SimpleSearch, StocktakingForm
from .scripts import search_items, check_category_section, simple_item_search,\
    stocktaking_items


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
def simple_search(request):
    if request.method == 'GET':
        form = SimpleSearch()
        context = {'form': form}
        return render(request, 'inventory/simple_search.html', context)
    else:
        form = SimpleSearch(request.POST)
        if not form.is_valid():
            form = SimpleSearch()
            context = {'form': form}
        else:
            item = request.POST.get('item')
            item = str(item).upper()
            manufacturer = request.POST.get('manufacturer')
            manufacturer = str(manufacturer).upper()
            section = request.POST.getlist('section')
            results = simple_item_search(item, manufacturer, section)
            context = {'form': form, 'results': results}

        return render(request, 'inventory/simple_search.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def show_items_adv(request):
    if request.method == 'GET':
        form = QueryForm()

        return render(request, 'inventory/show_items_adv.html', {'form': form})
    else:
        form = QueryForm(request.POST)
        if not form.is_valid():
            form = QueryForm()
            found_list = []
            context = {'found_list': found_list, 'form': form}
            return render(request, 'inventory/show_items_adv.html', context)
        else:
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

            return render(request, 'inventory/show_items_adv.html', context)


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


def stock_section(request):
    section_ids = []
    section_names = []
    user = request.user
    u = User.objects.get(username=user.username)
    for i in u.employee.section.all().values('id', 'name'):
        section_ids.append(i.get('id'))
        section_names.append(i.get('name'))
    sections = zip(section_ids, section_names)
    context = {'sections': sections}
    return render(request, 'inventory/stock_section.html', context)




@login_required()
def stocktaking(request, section):
    results = stocktaking_items(section)

    if request.method == 'GET':
        form = StocktakingForm()
        text = 'Stocktaking form for section: %s' % Section.objects.get(id=section).name
        context = {'results': results, 'form': form, 'text': text, 'section':section}
        return render(request, 'inventory/stocktaking.html', context)

    else:
        form = StocktakingForm(request.POST)
        if not form.is_valid():
            form = StocktakingForm()
            text = 'Form Error'
            context = {'form': form, 'text': text, 'section':section}
            return render(request, 'inventory/stocktaking.html', context)
        else:
            counted = request.POST.getlist('counted')
            text = 'Form Sent Successfully'

            stock_values = zip(counted, results)
            try:
                latest_stock = Stocktaking.objects.latest('stock_id')
            except ObjectDoesNotExist:
                latest_stock = 0
            current_stock = int(latest_stock.stock_id) +1
            for counted, results in stock_values:
                Stocktaking.objects.create(item=Item.objects.get(id=results.get('item')),
                                           section=Section.objects.get(id=results.get('section')),
                                           stock_quantity=(results.get('quantity_sum')),
                                           counted=counted,
                                           user=request.user,
                                           stock_id=current_stock)

        context = {'results': results, 'form': form, 'text': text, 'section':section}
        return render(request, 'inventory/stocktaking.html', context)


def show_stocktaking(request):
    return render(request, 'inventory/show_stocktaking.html')
