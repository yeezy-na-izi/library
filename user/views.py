from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import login, logout

from django.shortcuts import render
from django.shortcuts import redirect

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from user.forms import CreateUserForm, LoginUserForm
from user.models import CustomUser
from user.utils import find_user_by_username_or_email
from user.utils import send_email_token
from user.utils import token_generator
from user.utils import MessagesStrings


def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, MessagesStrings.notLogged)
        return redirect('/login')
    context = {
        "books": request.user.stared_books.all()
    }
    return render(request, 'user/profile/index.html', context)


def authorization(request):
    if request.user.is_authenticated:
        messages.success(request, MessagesStrings.alreadyLogged)
        return redirect('/profile')
    form = LoginUserForm()
    context = {'form': form}
    if request.method == 'POST':
        form = LoginUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, MessagesStrings.loginSuccess)
            return redirect(f'/profile')
        else:
            messages.error(request, MessagesStrings.userDoesNotExist)
    return render(request, 'user/login.html', context)


def reset_password(request):
    if request.user.is_authenticated:
        messages.success(request, MessagesStrings.alreadyLogged)
        return redirect(f'/profile')
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = find_user_by_username_or_email(username)
        except CustomUser.DoesNotExist:
            messages.error(request, MessagesStrings.userDoesNotExist)
            return redirect('/email_login')

        domain = get_current_site(request).domain
        email_subject = 'Восстановление пароля'
        email_body = 'Привет, {}, чтобы восстановить пароль, перейди по ссылке: \n{}'

        send_email_token(user, email_subject, email_body, domain, 'restore')

        messages.success(request, MessagesStrings.checkEmail)
    return render(request, 'user/restore.html')


def restore(request, user_id, token):
    if request.user.is_authenticated:
        messages.success(request, MessagesStrings.alreadyLogged)
        return redirect(f'/profile')
    username = force_str(urlsafe_base64_decode(user_id))
    user = CustomUser.objects.get(username=username)
    if not token_generator.check_token(user, token):
        messages.error(request, MessagesStrings.somethingWentWrong)
        return redirect('/login')
    if request.method == 'POST':
        password1, password2 = request.POST['password1'], request.POST['password2']
        if password1 != password2:
            messages.error(request, MessagesStrings.passwordsDontMatch)
            return redirect('#')
        user.set_password(password1)
        user.save()
        login(request, user)
        return redirect('/profile')

    return render(request, 'user/restore_password.html')


def registration(request):
    if request.user.is_authenticated:
        messages.success(request, MessagesStrings.alreadyLogged)
        return redirect(f'/profile')
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.is_active = False
            user = user_form.save()
            user.is_active = False
            user.save()

            domain = get_current_site(request).domain
            email_subject = 'Подтверждение почты'
            email_body = 'Привет, {}, это активация аккаунта, перейди по ссылке чтобы ' \
                         'верефицировать свой аккаунт\n{}'
            send_email_token(user, email_subject, email_body, domain, 'activate')

            messages.success(request, MessagesStrings.checkEmail)
            return redirect('/login')
        else:
            if 'password2' in user_form.errors:
                invalid = user_form.errors['password2'][0]
                messages.error(request, invalid)
                context = {'form': user_form}
                return render(request, 'user/registration.html', context)
            else:
                messages.error(request, MessagesStrings.somethingWentWrong)
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
        messages.success(request, MessagesStrings.alreadyLogged)
        return redirect(f'/profile')
    try:
        username = force_str(urlsafe_base64_decode(user_id))
        user = CustomUser.objects.get(username=username)
        if user.is_active:
            messages.warning(request, MessagesStrings.userAlreadyActive)
            return redirect('/login')
        if token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, MessagesStrings.userActiveSuccess)
            return redirect('/login')
        messages.error(request, MessagesStrings.userActiveFailure)
        return redirect('/login')
    except CustomUser.DoesNotExist:
        messages.error(request, MessagesStrings.userDoesNotExist)
    return redirect('/login')


def email_login(request):
    if request.user.is_authenticated:
        messages.success(request, MessagesStrings.alreadyLogged)
        return redirect(f'/profile')
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = find_user_by_username_or_email(username)
        except CustomUser.DoesNotExist:
            messages.error(request, MessagesStrings.userDoesNotExist)
            return redirect('/email_login')

        domain = get_current_site(request).domain
        email_subject = 'Вход через email'
        email_body = 'Привет, {}, чтобы войти на сайт, перейди по ссылке: \n{}'

        send_email_token(user, email_subject, email_body, domain, 'email_login')
        messages.success(request, MessagesStrings.checkEmail)

    return render(request, 'user/email_login.html')


def email_login_ver(request, user_id, token):
    try:
        username = force_str(urlsafe_base64_decode(user_id))
        user = CustomUser.objects.get(username=username)

        if token_generator.check_token(user, token):
            login(request, user)
            user.save()
            messages.success(request, MessagesStrings.loginSuccess)
            return redirect('/profile')
        messages.error(request, MessagesStrings.somethingWentWrong)
        return redirect('/login')
    except CustomUser.DoesNotExist:
        messages.error(request, MessagesStrings.userDoesNotExist)
    return redirect('/login')
