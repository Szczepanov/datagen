from django.shortcuts import render

from .forms import TableForm


def generate(request):
    return render(request, 'generator/generate_new.html', {})


def generate_new(request):
    if request.method == "POST":
        form = TableForm(request.POST or None)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.save()
    else:
        form = TableForm()
    return render(request, 'generator/generate_new.html', {'form': form})


def display_data(request, data, **kwargs):
    return render(request, 'generator/posted-data.html', dict(data=data, **kwargs), )


def formset(request, formset_class, template):
    if request.method == 'POST':
        formset = formset_class(request.POST or None)
        if formset.is_valid():
            data = formset.cleaned_data
            return display_data(request, data)
    else:
        formset = formset_class()
    return render(request, template, {'formset': formset},)
