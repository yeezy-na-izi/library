from django.shortcuts import render


def home_page(request):
    context = {}
    return render(request, 'library/home_page/index.html', context)
