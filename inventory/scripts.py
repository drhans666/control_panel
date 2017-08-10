from .models import Item, Category, Section, ItemLocation
from itertools import chain


def assign_to_lists(matches, found_items, found_category, found_section, found_quantity):
    for match in matches:
        found_items.append(match)
        found_category.append(match.category.all()[0])
        found_section.append(match.section.all()[0])

        for i in match.itemlocation_set.all():
            found_quantity.append(i.quantity)


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


def search_items(item, manufacturer, cat, sect):
    found_items = []
    found_category = []
    found_section = []
    found_quantity = []

    # query when all items and manufacturers
    if item == 'ALL' and manufacturer == 'ALL':
        matches = Item.objects.filter(itemlocation__section__in=sect,
                                      category__id__in=cat).order_by('category')
        assign_to_lists(matches, found_items, found_category, found_section, found_quantity)


    # query when specified item, all manufacturers
    if item != 'ALL' and manufacturer == 'ALL':
        matches = Item.objects.filter(name__contains=item, itemlocation__section__in=sect,
                                      category__id__in=cat).order_by('category')
        assign_to_lists(matches, found_items, found_category, found_section, found_quantity)

    # query when specified manufacturer, all items
    if item == 'ALL' and manufacturer != 'ALL':
        matches = Item.objects.filter(manufacturer__name__contains=manufacturer,
                                      itemlocation__section__in=sect,
                                      category__id__in=cat).order_by('category')
        assign_to_lists(matches, found_items, found_category, found_section, found_quantity)

    # query when specified manufacturer and items
    if item != 'ALL' and manufacturer != 'ALL':
        matches = Item.objects.filter(name__contains=item,
                                      manufacturer__name__contains=manufacturer,
                                      itemlocation__section__in=sect,
                                      category__id__in=cat).order_by('category')
        assign_to_lists(matches, found_items, found_category, found_section, found_quantity)

    # creates zip from lists for 'for loop' that populates table template
    found_list = zip(found_items, found_category, found_section, found_quantity)

    return found_list