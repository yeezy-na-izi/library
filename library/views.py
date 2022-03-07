from django.shortcuts import render
from library.models import Book
from library.models import TagsType
from library.models import Tags


def home_page(request):
    context = {}
    return render(request, 'library/home_page/index.html', context)


def books(request):
    if request.method == 'POST':
        if request.POST['type'] == 'search':
            books_obj = Book.objects.filter(name__icontains=request.POST['search'])
        elif request.POST['type'] == 'sidebar':
            books_obj = Book.objects.filter(tags=Tags.objects.get(pk=int(request.POST['first'])))
    else:
        books_obj = Book.objects.all()
    context = {
        'books': books_obj,
        'tags': TagsType.objects.all()
    }
    return render(request, 'library/books/index.html', context)
