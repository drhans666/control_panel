from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


from .models import Stocktaking, Item, Section
from .forms import StocktakingForm, BrowseStockForm
from .scripts import stocktaking_items



@login_required()
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
    return render(request, 'stocktaking/stock_section.html', context)


@login_required()
def stocktaking(request, section):
    results = stocktaking_items(section)

    if request.method == 'GET':
        form = StocktakingForm()
        text = 'Stocktaking form for section: %s' % Section.objects.get(id=section).name
        context = {'results': results, 'form': form, 'text': text, 'section':section}
        return render(request, 'stocktaking/stocktaking.html', context)

    else:
        form = StocktakingForm(request.POST)
        if not form.is_valid():
            form = StocktakingForm()
            text = 'Form Error'
            context = {'form': form, 'text': text, 'section':section}
            return render(request, 'stocktaking/stocktaking.html', context)
        else:
            counted = request.POST.getlist('counted')
            text = 'Form Sent Successfully'

            stock_values = zip(counted, results)
            try:
                latest_stock = Stocktaking.objects.latest('stock_id')
                current_stock = int(latest_stock.stock_id) +1
            except ObjectDoesNotExist:
                current_stock = 1
            for counted, results in stock_values:
                Stocktaking.objects.create(item=Item.objects.get(id=results.get('item')),
                                           section=Section.objects.get(id=results.get('section')),
                                           stock_quantity=(results.get('quantity_sum')),
                                           counted=counted,
                                           user=request.user,
                                           stock_id=current_stock)

        context = {'results': results, 'form': form, 'text': text, 'section':section}
        return render(request, 'stocktaking/stocktaking.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def browse_stocktakings(request):
    if request.method == 'GET':
        form = BrowseStockForm()
        context = {'form': form}
        return render(request, 'stocktaking/browse_stocktakings.html', context)
    else:
        form = BrowseStockForm(request.POST)
        context = {'form': form}
        return render(request, 'stocktaking/browse_stocktakings.html', context)


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='low_user').count() == 0,
                  login_url='/users/access_denied.html')
def show_stocktaking(request):
    return render(request, 'stocktaking/show_stocktaking.html')

