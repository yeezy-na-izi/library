# Generated by Django 4.0.3 on 2022-03-07 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_alter_tags_tags_type'),
        ('user', '0005_rename_surname_customuser_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='stared_books',
            field=models.ManyToManyField(to='library.book', verbose_name='Помеченные книги'),
        ),
    ]
