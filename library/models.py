from django.db import models
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class TagsType(models.Model):
    class Meta:
        verbose_name = 'Тип категории'
        verbose_name_plural = 'Типы категории'

    colors = (
        ('bg-secondary', 'Серый'),
        ('bg-success', 'Зеленый'),
        ('bg-warning text-dark', 'Желтый'),
        ('bg-info text-dark', 'Голубой'),
        ('bg-dark', 'Черный'),
    )
    name = models.CharField(verbose_name='Название', max_length=128)
    color = models.CharField(verbose_name='Цвет', choices=colors, default='bg-secondary', max_length=32)

    def __str__(self):
        return self.name


class Tags(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(verbose_name='Название', max_length=128)
    tags_type = models.ForeignKey(verbose_name='Тип категории', to=TagsType, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tags_type}: {self.name}'


class Book(models.Model):
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    name = models.CharField(verbose_name='Название', max_length=1280)
    year = models.IntegerField(verbose_name='Год издания', )
    author_name = models.CharField(verbose_name='Имя Автора', max_length=200)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    cover = models.ImageField(verbose_name='Обложка', blank=True, default='', upload_to='static/book/img')
    tags = models.ManyToManyField(verbose_name='Категории', blank=True, to=Tags)
    visibility = models.BooleanField(verbose_name='Визибилити', default=False)
    slug = models.SlugField(null=True, blank=True)
    pdf = models.FileField(verbose_name='PDF', blank=True, upload_to='static/book/pdf')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = urlsafe_base64_encode(force_bytes(self))[:16]
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
