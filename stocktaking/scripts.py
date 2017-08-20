from inventory.models import ItemLocation
from django.db.models import Count, Sum


def stocktaking_items(section):
    results = []

    matches = ItemLocation.objects.filter(section=section) \
        .order_by('item__name', 'item__manufacturer__name')

    for match in matches.values('section', 'item__name', 'item',
                                'item__manufacturer__name') \
            .annotate(quantity_sum=Sum('quantity')):
        results.append(match)

    return results