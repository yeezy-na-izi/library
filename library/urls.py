from django.urls import path
from library import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('books/', views.home_page, name='books'),
]
