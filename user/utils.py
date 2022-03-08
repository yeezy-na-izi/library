from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from six import text_type
from user.models import CustomUser


class MessagesStrings:
    notLogged = "Вы еще не вошли"
    alreadyLogged = "Вы уже авторизованны"
    userDoesNotExist = "Такого пользователя не найдено"
    passwordsDontMatch = "Пароли не совпадают"
    somethingWentWrong = "Что-то пошло не так, повторите попытку"
    userAlreadyActive = "Аккаунт уже активен"
    userActiveSuccess = "Аккаунт успешно активирован"
    userActiveFailure = "Аккаунт по каким-то причинам не был активирован"
    checkEmail = "Проверьте свою почту"
    loginSuccess = "Вход успешно выполнен"


class EmailMessages:
    class Registration:
        subject = 'Подтверждение почты'
        body = 'Привет, {}, это активация аккаунта, перейди по ссылке чтобы верефицировать свой аккаунт\n{}'

    class Restore:
        subject = 'Восстановление пароля'
        body = 'Привет, {}, чтобы восстановить пароль, перейди по ссылке: \n{}'

    class Login:
        subject = 'Вход через email'
        body = 'Привет, {}, чтобы войти на сайт, перейди по ссылке: \n{}'


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.username) + text_type(timestamp)


token_generator = AppTokenGenerator()


def send_email(email_subject, email_body, to):
    if not to:
        return
    email = EmailMessage(email_subject, email_body, 'noreply@semycolon.com', to)
    email.send(fail_silently=False)


def send_email_token(user, domain, url_part, email_subject, email_body):
    user_id = urlsafe_base64_encode(force_bytes(user.username))
    token = token_generator.make_token(user)
    relative = reverse(url_part, kwargs={'user_id': user_id,
                                         'token': token})
    activate_url = f'http://{domain}{relative}'

    send_email(email_subject, email_body.format(user.username, activate_url), [user.email])


def find_user_by_username_or_email(username_or_email):
    try:
        validate_email(username_or_email)
        return CustomUser.objects.get(email=username_or_email)
    except ValidationError:
        return CustomUser.objects.get(username=username_or_email)
