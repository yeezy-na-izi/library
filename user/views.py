import os

from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode

from user.forms import CreateUserForm, LoginUserForm
# Create your views here.
from user.models import CustomUser
from user.utils import token_generator


def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Вы еще не вошли')
        return redirect('/login')
    context = {
        "books": request.user.stared_books.all()
    }
    return render(request, 'user/profile.html', context)


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
        return redirect(f'/profile')
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.is_active = False
            user = user_form.save()
            user.is_active = False
            user.save()
            # return redirect('/login')
            user_id = urlsafe_base64_encode(force_bytes(user.username))
            domain = get_current_site(request).domain
            relative = reverse('activate', kwargs={'user_id': user_id,
                                                   'token': token_generator.make_token(user)})
            activate_url = f'http://{domain}{relative}'
            #
            email_subject = 'Подтверждение почты'
            email_body = f'Привет, {user.username}, это активация аккаунта, перейди по ссылке чтобы ' \
                         f'верефицировать свой аккаунт\n{activate_url}'
            email = EmailMessage(email_subject, email_body, 'noreply@semycolon.com', [user.email], )
            email.send(fail_silently=False)

            messages.success(request, 'Подтвердите свою почту и войдите')
            return redirect('/login')
        else:
            if 'password2' in user_form.errors:
                invalid = user_form.errors['password2'][0]
                messages.error(request, invalid)
                context = {'form': user_form}
                return render(request, 'user/registration.html', context)
            else:
                messages.error(request, 'Что-то пошло не так, повторите попытку')
                context = {'form': user_form}
                return render(request, 'user/registration.html', context)
    user_form = CreateUserForm()
    context = {'form': user_form}
    return render(request, 'user/registration.html', context)


def logout_def(request):
    logout(request)
    return redirect('/')


def verification_email(request, user_id, token):
    if request.user.is_authenticated:
        messages.success(request, 'Вы уже авторизованны')
        return redirect(f'/profile/{request.user.username}')
    try:
        username = force_str(urlsafe_base64_decode(user_id))
        user = CustomUser.objects.get(username=username)
        if token_generator.check_token(user, token) and not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, 'Аккаунт успешко активирован')
            return redirect('/login')
        messages.error(request, 'Аккаунт по каким-то причинам не был активирован')
        return redirect('/login')
    except CustomUser.DoesNotExist:
        # TODO: убрать на проде
        messages.error(request, 'Такого аккаунта не существует, куда вы перешли, Михаил Новиков?')
    return redirect('/login')
