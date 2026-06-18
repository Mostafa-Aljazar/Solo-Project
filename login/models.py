import re
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def login_validator(self, postData):
        errors = {}
        email = postData.get('email', '').strip()
        password = postData.get('password', '')

        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors['email'] = 'يرجى إدخال بريد إلكتروني صحيح.'

        if not password:
            errors['password'] = 'كلمة المرور مطلوبة.'

        if not errors:
            if not self.filter(email=email).exists():
                errors['login'] = 'البريد الإلكتروني أو كلمة المرور غير صحيحة.'

        return errors


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
