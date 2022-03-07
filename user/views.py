import os

from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from user.forms import CreateUserForm, LoginUserForm
# Create your views here.


def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Вы еще не вошли')
        return redirect('/login')
    return HttpResponse('123')


def authorization(request):
    if request.user.is_authenticated:
        messages.success(request, 'Вы уже авторизованны')
        return redirect('/profile')
    form = LoginUserForm()
    context = {'form': form}
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(f'/profile')
        else:
            messages.error(request, 'Такого пользователя не найдено')
    return render(request, 'user/login.html', context)


def registration(request):
    if request.user.is_authenticated:
        messages.success(request, 'Вы уже авторизованны')
        return redirect(f'/profile/{request.user.username}')
    return HttpResponse('456')
