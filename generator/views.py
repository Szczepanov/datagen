from django.shortcuts import render


def generate(request):
    return render(request, 'generator/generate.html', {})
