from django.http import HttpResponseForbidden, HttpResponseNotFound

from django.shortcuts import redirect, render

from library.models import Book, TagsType, Tags

from django.core.serializers import serialize
from django.http import JsonResponse

import json


def get_user_dict(user):
    context = {
        'is_superuser': user.is_superuser,
        'email': user.email,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }

    return context


def home_page(request):
    context = {}
    return render(request, 'library/home_page/index.html', context)


def json_home_page(request):
    if request.user.is_authenticated:
        context = {'user': get_user_dict(request.user)}
    else:
        context = {}
    return JsonResponse(context)


def json_books(request):
    context = {}
    all_books = json.loads(serialize('json', Book.objects.all()))
    all_tags = json.loads(serialize('json', Tags.objects.all(), fields=['name']))
    tags = []
    for i in all_tags:
        tags.append(i['fields']['name'])
    context['books'] = all_books
    context['tags'] = tags
    return JsonResponse(context)


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
                new_book.visibility = 'visibility' in post
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
