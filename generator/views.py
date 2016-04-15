from django.shortcuts import render

from .forms import DataSetForm


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
