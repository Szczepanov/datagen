from django.shortcuts import render

from .forms import DataSetForm, CountryForm


def generate(request):
    return render(request, 'generator/generate_new.html', {})


def generate_new(request):
    if request.method == "POST":
        form = DataSetForm(request.POST)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.save()
    else:
        form = DataSetForm()
    return render(request, 'generator/generate_new.html', {'form': form})


def set_variables(request):
    if request.method == "POST":
        form = CountryForm(request.POST)
        if form.is_valid():
            countryform = form.save(commit=False)
            countryform.save()
    else:
        form = CountryForm()
    return render(request, 'generator/set_variables.html', {'form': form})
