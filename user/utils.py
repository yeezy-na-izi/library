from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from six import text_type


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.username) + text_type(timestamp)


token_generator = AppTokenGenerator()


def send_email(email_subject, email_body, to):
    email = EmailMessage(email_subject, email_body, 'noreply@semycolon.com', to, )
    email.send(fail_silently=False)
