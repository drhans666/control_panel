from .models import Category, Section, ItemLocation
from django.db.models import Count, Sum


def found_list_appender(matches, found_items, found_category):
    item_idlist = []
    for match in matches:
        found_items.append(match)
        found_category.append(match.item.category.all().values_list('name', flat=True))
        #item_idlist.append(match.get('item__id'))



def check_category_section(category, section):
    # if category/section are empty, they are populated with all id's
    if category == []:
        cat_objects = Category.objects.all()
        for i in cat_objects:
            category.append(i.id)

    if section == []:
        sec_objects = Section.objects.all()
        for i in sec_objects:
            section.append(i.id)

    return category, section


def simple_item_search(item, manufacturer, section):
    matches = []
    results = []

    # query when all items and manufacturers
    if item == 'ALL' and manufacturer == 'ALL':
        matches = ItemLocation.objects.filter(section__in=section) \
            .order_by('item__name', 'item__manufacturer__name')

    # query when specified item, all manufacturers
    if item != 'ALL' and manufacturer == 'ALL':
        matches = ItemLocation.objects.filter(item__name__contains=item, section__in=section)\
            .order_by('item__name', 'item__manufacturer__name')


    # query when specified manufacturer, all items
    if item == 'ALL' and manufacturer != 'ALL':
        matches = ItemLocation.objects.filter(item__manufacturer__name__contains=manufacturer,
                                              section__in=section)\
            .order_by('item__name', 'item__manufacturer__name')

    # query when specified manufacturer and items
    if item != 'ALL' and manufacturer != 'ALL':
        matches = ItemLocation.objects.filter(item__name__contains=item,
                                              item__manufacturer__name__contains=manufacturer,
                                              section__in=section)\
            .order_by('item__name', 'item__manufacturer__name')

    for match in matches.values('section', 'item__name',
                                'item__manufacturer__name') \
            .annotate(quantity_sum=Sum('quantity')):
        results.append(match)

    return results

def search_items(item, manufacturer, cat, sect):
    found_items = []
    found_category = []

    # query when all items and manufacturers
    if item == 'ALL' and manufacturer == 'ALL':
        matches = ItemLocation.objects.filter(section__in=sect,
                                      item__category__id__in=cat)\
            .order_by('section__name', 'item__name').distinct()


        found_list_appender(matches, found_items, found_category)

    # query when specified item, all manufacturers
    if item != 'ALL' and manufacturer == 'ALL':
        matches = ItemLocation.objects.filter(item__name__contains=item, section__in=sect,
                                      item__category__id__in=cat).order_by('section__name',
                                                                           'item__name').distinct()

        found_list_appender(matches, found_items, found_category)

    # query when specified manufacturer, all items
    if item == 'ALL' and manufacturer != 'ALL':
        matches = ItemLocation.objects.filter(item__manufacturer__name__contains=manufacturer,
                                      section__in=sect,
                                      item__category__id__in=cat).order_by('section__name',
                                                                           'item__name').distinct()

        found_list_appender(matches, found_items, found_category)

    # query when specified manufacturer and items
    if item != 'ALL' and manufacturer != 'ALL':
        matches = ItemLocation.objects.filter(item__name__contains=item,
                                      item__manufacturer__name__contains=manufacturer,
                                      section__in=sect,
                                      item__category__id__in=cat).order_by('section__name',
                                                                           'item__name').distinct()

        found_list_appender(matches, found_items, found_category)

    # creates zip from lists for 'for loop' that populates table template
    found_list = zip(found_items, found_category)

    return found_list