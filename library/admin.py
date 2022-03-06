from django.contrib import admin
from library.models import Book, Tags, TagsType

# Register your models here.

admin.site.register(Book)
admin.site.register(Tags)
admin.site.register(TagsType)