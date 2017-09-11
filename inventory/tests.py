from django.test import TestCase
from django.contrib.auth.models import User

from .models import ItemLocation, Item, Category, Manufacturer, Section
from .scripts import adv_search_items, check_category_section, simple_item_search


class AdvSearchTest(TestCase):

    def setUp(self):
        user1 = User.objects.create(username='tester')
        Category.objects.create(name='category1')
        Category.objects.create(name='category2')
        category1 = Category.objects.get(name__iexact='category1')
        category2 = Category.objects.get(name__iexact='category2')

        Manufacturer.objects.create(name='manufacturer1')
        Manufacturer.objects.create(name='manufacturer2')
        manufacturer1 = Manufacturer.objects.get(name__iexact='manufacturer1')
        manufacturer2 = Manufacturer.objects.get(name__iexact='manufacturer2')

        Section.objects.create(name='section1')
        Section.objects.create(name='section2')
        section1 = Section.objects.get(name__iexact='section1')
        section2 = Section.objects.get(name__iexact='section2')

        Item.objects.create(name='item1', manufacturer=manufacturer1)
        Item.objects.create(name='item2', manufacturer=manufacturer2)
        Item.objects.create(name='item3', manufacturer=manufacturer1)
        item1 = Item.objects.get(name__iexact='item1')
        item1.category.add(category1)
        item2 = Item.objects.get(name__iexact='item2')
        item2.category.add(category2)
        item3 = Item.objects.get(name__iexact='item3')
        item3.category.add(category1, category2)
        ItemLocation.objects.create(item=item1, section=section1, user=user1)
        ItemLocation.objects.create(item=item2, section=section2, user=user1)
        ItemLocation.objects.create(item=item3, section=section1, user=user1)

    def test_section_search(self):
        section2 = Section.objects.get(name__iexact='section2')
        item = 'ALL'
        manufacturer = 'ALL'
        category = []
        section = [section2, ]
        category, section = check_category_section(category, section)
        found_list= adv_search_items(item, manufacturer, category, section)
        for item, category in found_list:
            self.assertEqual(item.item.name, 'ITEM2')
            self.assertEqual(category.all()[0], 'CATEGORY2' )

    def test_item_search(self):
        item = Item.objects.get(name__iexact='item3')
        manufacturer = 'ALL'
        category = []
        section = []
        category, section = check_category_section(category, section)
        found_list = adv_search_items(item, manufacturer, category, section)
        for item, category in found_list:
            self.assertEqual(item.item.name, 'ITEM3')
            self.assertEqual(len(category), 2)

    def test_manufacturer_search(self):
        item_list = []
        item = 'ALL'
        manufacturer = Manufacturer.objects.get(name__iexact='manufacturer1')
        section = []
        category = []
        category, section = check_category_section(category, section)
        found_list = adv_search_items(item, manufacturer, category, section)
        for items, category in found_list:
            item_list.append(items)
            self.assertEqual(items.item.manufacturer.name, 'MANUFACTURER1')
        self.assertEqual(len(item_list), 2)

    def test_category_search(self):
        category_list = []
        item = 'ALL'
        manufacturer = 'ALL'
        section = []
        category = [Category.objects.get(name__iexact='category1'),]
        category, section = check_category_section(category, section)
        found_list = adv_search_items(item, manufacturer, category, section)
        for item, category in found_list:
            category_list.append(category)
        self.assertEqual(len(category_list[0].all()), 1)
        self.assertEqual(len(category_list[1].all()), 2)

    def test_all_search(self):
        item = Item.objects.get(name__iexact='item2')
        manufacturer = Manufacturer.objects.get(name__iexact='manufacturer2')
        category = [Category.objects.get(name__iexact='category2'),]
        section = [Section.objects.get(name__iexact='section2'),]
        category_list = []
        item_list = []
        category, section = check_category_section(category, section)
        found_list = adv_search_items(item, manufacturer, category, section)
        for item, category in found_list:
            item_list.append(item)
            category_list.append(category)

        self.assertEqual(len(category_list), 1)
        self.assertEqual(category_list[0].all()[0], 'CATEGORY2')

        self.assertEqual(len(item_list), 1)
        self.assertEqual(item_list[0].item.name, 'ITEM2')
        self.assertEqual(item_list[0].item.manufacturer.name, 'MANUFACTURER2')
        self.assertEqual(item_list[0].section.name, 'SECTION2')


class SimpleSearchTest(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='tester')
        Category.objects.create(name='category1')
        Category.objects.create(name='category2')
        category1 = Category.objects.get(name__iexact='category1')
        category2 = Category.objects.get(name__iexact='category2')

        Manufacturer.objects.create(name='manufacturer1')
        Manufacturer.objects.create(name='manufacturer2')
        manufacturer1 = Manufacturer.objects.get(name__iexact='manufacturer1')
        manufacturer2 = Manufacturer.objects.get(name__iexact='manufacturer2')

        Section.objects.create(name='section1')
        Section.objects.create(name='section2')
        section1 = Section.objects.get(name__iexact='section1')
        section2 = Section.objects.get(name__iexact='section2')

        Item.objects.create(name='item1', manufacturer=manufacturer1)
        Item.objects.create(name='item2', manufacturer=manufacturer2)
        Item.objects.create(name='item3', manufacturer=manufacturer1)
        item1 = Item.objects.get(name__iexact='item1')
        item1.category.add(category1)
        item2 = Item.objects.get(name__iexact='item2')
        item2.category.add(category2)
        item3 = Item.objects.get(name__iexact='item3')
        item3.category.add(category1, category2)
        ItemLocation.objects.create(item=item1, section=section1, user=user1, quantity=10)
        ItemLocation.objects.create(item=item2, section=section2, user=user1, quantity=52)
        ItemLocation.objects.create(item=item3, section=section1, user=user1, quantity=8)
        ItemLocation.objects.create(item=item3, section=section1, user=user1, quantity=15)

    # tests section query + quantity count
    def test_section_count_search(self):
        values_list = []
        item = 'ALL'
        manufacturer = 'ALL'
        section = Section.objects.get(name__iexact='section1')
        results = simple_item_search(item, manufacturer, section)

        for values in results[1].values():
            values_list.append(values)

        # checks if proper amount of results found
        self.assertEqual(len(results), 2)
        # checks if quantities of same kind are summed properly
        self.assertEqual((list(results[1].values())
                          [list(results[1].keys()).index('quantity_sum')]),23)

    # tests item query
    def test_item_search(self):

        item = Item.objects.get(name__iexact='item1')
        manufacturer = 'ALL'
        section = Section.objects.get(name__iexact='section1')
        results = simple_item_search(item, manufacturer, section)

        self.assertEqual(len(results), 1)
        self.assertEqual((list(results[0].values())
                          [list(results[0].keys()).index('item__name')]), 'ITEM1')

    # tests manufacturer query
    def test_manufacturer_search(self):
        item = 'ALL'
        manufacturer = Manufacturer.objects.get(name__iexact='manufacturer2')
        section = Section.objects.get(name__iexact='section1')
        results = simple_item_search(item, manufacturer, section)

        self.assertEqual(len(results), 0)

        # tests all inputs query
    def test_all_search(self):
        item = Item.objects.get(name__iexact='item2')
        manufacturer = Manufacturer.objects.get(name__iexact='manufacturer2')
        section = Section.objects.get(name__iexact='section2')
        results = simple_item_search(item, manufacturer, section)

        self.assertEqual(len(results), 1)
        self.assertEqual((list(results[0].values())
                          [list(results[0].keys()).index('quantity_sum')]), 52)