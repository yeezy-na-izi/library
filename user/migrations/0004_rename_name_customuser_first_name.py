# Generated by Django 4.0.3 on 2022-03-06 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_customuser_stared_books'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='name',
            new_name='first_name',
        ),
    ]
