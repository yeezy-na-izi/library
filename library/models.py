from django.db import models


class BookTags(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    colors = (
        ('1', 'Голубой'),
        ('2', 'Розовый'),
        ('3', 'Фиолетовый'),
        ('4', 'Зеленый'),
        ('5', 'Розово-фиолетовый'),
    )
    name = models.CharField(verbose_name='Название', max_length=128)
    color = models.CharField(verbose_name='Цвет', choices=colors, default='1', max_length=2)

    def __str__(self):
        return self.name


class Book(models.Model):
    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    name = models.CharField(verbose_name='Название', max_length=1280)
    year = models.IntegerField(verbose_name='Год издания', )
    author_name = models.CharField(verbose_name='Имя Автора', max_length=48)
    author_surname = models.CharField(verbose_name='Фамилия Автора', max_length=128)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    cover = models.ImageField(verbose_name='Обложка', blank=True, default='', upload_to='static/book')
    tags = models.ManyToManyField(verbose_name='Категории', blank=True, to=BookTags)

    def __str__(self):
        return self.name
