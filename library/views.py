from django.contrib import messages
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.http import HttpResponseNotFound
from django.shortcuts import redirect
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
        else:  # request.POST['type'] == 'sidebar'
            post = list(request.POST.dict().values())[2:]
            ids = []
            for i in post:
                if i.isdigit():
                    ids.append(int(i))
            tags = Tags.objects.filter(pk__in=ids)
            books_obj = Book.objects.all()
            for i in tags:
                books_obj = books_obj.filter(tags=i)
    else:
        books_obj = Book.objects.all()
    books_obj = books_obj.filter(visibility=True)
    context = {
        'books': books_obj,
        'tags': TagsType.objects.all()
    }
    return render(request, 'library/books/index.html', context)


def book_page(request, slug):
    book = Book.objects.get(slug=slug)
    context = {'book': book}
    return render(request, 'library/book/index.html', context)


def book_star(request, slug):
    if request.method != 'POST':
        return HttpResponseNotFound()
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    book = Book.objects.get(slug=slug)
    request.user.stared_books.add(book)
    request.user.save()
    return redirect(f'/book/{slug}')
