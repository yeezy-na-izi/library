# Generated by Django 4.0.3 on 2022-03-06 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('color', models.CharField(default='1', max_length=2, verbose_name='Цвет')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1280, verbose_name='Название')),
                ('year', models.IntegerField(verbose_name='Год издания')),
                ('author_name', models.CharField(max_length=48, verbose_name='Имя Автора')),
                ('author_surname', models.CharField(max_length=128, verbose_name='Фамилия Автора')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('cover', models.ImageField(blank=True, default='', upload_to='static/book', verbose_name='Обложка')),
                ('tags', models.ManyToManyField(blank=True, to='library.booktags', verbose_name='Категории')),
            ],
            options={
                'verbose_name': 'Книга',
                'verbose_name_plural': 'Книги',
            },
        ),
    ]
