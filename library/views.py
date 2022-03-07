from django.shortcuts import render
from library.models import Book
from library.models import TagsType


def home_page(request):
    context = {}
    return render(request, 'library/home_page/index.html', context)


def books(request):
    if request.method == 'POST':
        if request.POST['search']:
            books_obj = Book.objects.filter(name__icontains=request.POST['search'])
        else:
            books_obj = Book.objects.all()
    else:
        books_obj = Book.objects.all()
    context = {
        'books': books_obj,
        'tags': TagsType.objects.all()
    }
    return render(request, 'library/books/index.html', context)
