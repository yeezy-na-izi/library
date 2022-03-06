from django.shortcuts import render
from library.models import Book
from library.models import TagsType


def home_page(request):
    context = {}
    print(request.user.is_superuser)
    return render(request, 'library/home_page/index.html', context)


def books(request):
    context = {
        'books': Book.objects.all(),
        'Tags': Book.objects.all()
    }
    return render(request, 'library/books/index.html', context)
