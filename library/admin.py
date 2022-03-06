from django.contrib import admin
from library.models import Book, BookTags

# Register your models here.

admin.site.register(Book)
admin.site.register(BookTags)
