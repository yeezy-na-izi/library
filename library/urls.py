from django.urls import path
from library import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('books/', views.books, name='books'),
    path('book/<slug>/approve', views.book_approve, name='book_page'),
    path('book/<slug>/delete', views.book_delete, name='book_page'),
    path('book/<slug>', views.book_page, name='book_page'),
    path('api/', views.json_home_page, name='test_json'),
    path('api/books', views.json_books, name='json_for_book'),
]
