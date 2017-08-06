from django.shortcuts import render
from .forms import ItemForm, ItemLocationForm


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
            form.save()
            text = 'Item added'
            context = {'form': form, 'text': text}
            return render(request, 'inventory/add_to_section.html', context)
        else:
            text = 'Item added'
            context = {'form': form, 'text': text}
            return render(request, 'inventory/add_to_section.html', context)


def new_item(request):
    if request.method == 'GET':
        form = ItemForm()
        context = {'form': form}
        return render(request, 'inventory/new_item.html', context)
    else:
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            text = 'New item saved successfully'
            form = ItemForm()
            context = {'form': form, 'text': text}
            return render(request, 'inventory/new_item.html', context)
        else:
            text = 'Form Error'
            context = {'form': form, 'text': text}
            return render(request, 'inventory/new_item.html', context)

