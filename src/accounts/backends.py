import os
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class UserAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, email=None, **kwargs):
        password = kwargs['password']

        try:
            if email:
                user = User.objects.get(email=email)
            elif username:
                user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
