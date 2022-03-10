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
    all_books = Book.objects.all()
    if request.method == 'POST':
        if request.POST['type'] == 'search':
            books_obj = all_books.filter(name__icontains=request.POST['search'])
        elif request.POST['type'] == 'sidebar':
            post = list(request.POST.dict().values())[2:]
            ids = []
            for i in post:
                if i.isdigit():
                    ids.append(int(i))
            tags = Tags.objects.filter(pk__in=ids)
            for i in tags:
                books_obj = all_books.filter(tags=i)
        else:
            post = request.POST.dict()
            new_book = Book.objects.create(
                name=post['name'],
                year=post['year'],
                author_name=post['author_name'],
                description=post['description'],
            )
            for i in range(10):
                if str(i) in post:
                    if post[str(i)].isdigit():
                        new_book.tags.add(Tags.objects.get(pk=int(post[str(i)])))
            # new_book.sаve()
            request.user.added_books.add(new_book)
            books_obj = all_books
    else:
        books_obj = all_books
    books_obj = books_obj.filter(visibility=True)
    on_checking = []
    if request.user.is_authenticated:
        on_checking = request.user.added_books.filter(visibility=False)
    context = {
        'books': books_obj,
        'tags': TagsType.objects.all(),
        'on_checking': on_checking,
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
