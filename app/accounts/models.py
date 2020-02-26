from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string


class User(AbstractUser):
    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    # def send_welcome_email(self):
    #     subject = "가입을 환영합니다."
    #     content = render_to_string('accounts/welcome_email_content.txt', {
    #         'user': self,
    #     })
    #     sender_email = "jeongmyeonghyeon@gmail.com"
    #     send_mail(subject, content, sender_email, [self.email], fail_silently=False)
