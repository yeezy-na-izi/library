# Generated by Django 4.0.3 on 2022-03-06 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_alter_tags_tags_type'),
        ('user', '0002_alter_customuser_options_customuser_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='stared_books',
            field=models.ManyToManyField(blank=True, null=True, to='library.book', verbose_name='Помеченные книги'),
        ),
    ]
