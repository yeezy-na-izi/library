from django.shortcuts import render


def home_page(request):
    context = {}
    print(request.user.is_superuser)
    return render(request, 'library/home_page/index.html', context)

