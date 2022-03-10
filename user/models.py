from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from library.models import Book

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    email = models.EmailField('email address', unique=True)
    username = models.CharField(verbose_name='Ник', max_length=32, unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=64, blank=True, null=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=64, blank=True, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    stared_books = models.ManyToManyField(verbose_name='Помеченные книги', to=Book, blank=True)
    added_books = models.ManyToManyField(verbose_name='Добавленные книги', to=Book, blank=True,
                                         related_name='book_from_mine')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
