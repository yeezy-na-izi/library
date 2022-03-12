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
        elif request.POST['type'] == 'sidebar':
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
            post = request.POST.dict()
            new_book = Book.objects.create(
                name=post['name'],
                year=post['year'],
                author_name=post['author_name'],
                description=post['description'],
                cover=post['cover'] or None,
                pdf=post['pdf'] or None,
            )
            for i in range(10):
                if str(i) in post:
                    if post[str(i)].isdigit():
                        new_book.tags.add(Tags.objects.get(pk=int(post[str(i)])))
            # new_book.sаve()
            if request.user.is_superuser:
                if 'on' == post['visibility']:
                    new_book.visibility = True
            request.user.added_books.add(new_book)
            return redirect('/books/')
    else:
        books_obj = Book.objects.all()
    books_obj = books_obj.filter(visibility=True)
    on_checking = []
    if request.user.is_authenticated:
        if request.user.is_superuser:
            on_checking = Book.objects.filter(visibility=False)
        else:
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


def book_delete(request, slug):
    if request.user.is_superuser:
        Book.objects.get(slug=slug).delete()
        return redirect('/books/')
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')


def book_approve(request, slug):
    if request.user.is_superuser:
        book = Book.objects.get(slug=slug)
        book.visibility = True
        book.save()
        return redirect('/books/')
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')
