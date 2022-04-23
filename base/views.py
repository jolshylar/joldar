from django.shortcuts import render


def home(request):
    context = {}
    return render(request, 'base/home.html', context)


def news(request):
    context = {}
    return render(request, 'base/news.html', context)


def about(request):
    context = {}
    return render(request, 'base/about.html', context)
