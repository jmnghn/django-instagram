from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import resolve_url
from django.template.loader import render_to_string


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = 'M', '남성'
        FEMALE = 'F', '여성'

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=13, blank=True, validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")])
    gender = models.CharField(max_length=1, blank=True, choices=GenderChoices.choices)
    avatar = models.ImageField(blank=True, upload_to='accounts/avatar/%Y/%m/%d', help_text='200kb 이하의 jpg/png를 올려주세요.')

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url('pydenticon_image', self.username)

    # def send_welcome_email(self):
    #     subject = "가입을 환영합니다."
    #     content = render_to_string('accounts/welcome_email_content.txt', {
    #         'user': self,
    #     })
    #     sender_email = "jeongmyeonghyeon@gmail.com"
    #     send_mail(subject, content, sender_email, [self.email], fail_silently=False)
