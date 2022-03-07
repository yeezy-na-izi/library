import os

from django.contrib.sites.shortcuts import get_current_site
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
    return render(request, 'user/profile.html')


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
            user.is_active = True
            user.save()
            return redirect('/login')
            #
            # user_id = urlsafe_base64_encode(force_bytes(user.username))
            # domain = get_current_site(request).domain
            # relative = reverse('activate', kwargs={'user_id': user_id,
            #                                        'token': token_generator.make_token(user)})
            # activate_url = f'http://{domain}{relative}'
            #
            # email_subject = 'Подтверждение почты'
            # email_body = f'Привет, {user.username}, это активация аккаунта, перейди по ссылке чтобы ' \
            #              f'верефицировать свой аккаунт\n{activate_url}'
            # email = EmailMessage(email_subject, email_body, 'noreply@semycolon.com', [user.email], )
            # email.send(fail_silently=False)
            #
            # messages.success(request, 'Подтвердите свою почту и войдите')
            # return redirect('/login')
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
