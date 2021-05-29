import os
import random
from slugify import slugify
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .providers.google import Google
from ..serializers import LoginSerializer

User = get_user_model()


class BaseProviderSerializer(serializers.Serializer):

    def generate_username(self, name):
        username = slugify(name, separator='_')
        print(username)
        if not User.objects.filter(username=username).exists():
            return username
        else:
            random_username = username + str(random.randint(0, 1000))
            return self.generate_username(random_username)

    def register_user(self, user_id, email, name):
        users_by_email = User.objects.filter(email=email)

        if not users_by_email.exists():
            new_user = User.objects.create(
                email=email,
                username=self.generate_username(name),
                is_verified=True,
            )
            new_user.set_password(os.environ.get('SOCIAL_SECRET'))
            new_user.save()
        user = authenticate(email=email, password=os.environ.get('SOCIAL_SECRET'))
        serializer = LoginSerializer(instance=user)
        print(serializer.data)
        return serializer.data


class GoogleAuthSerializer(BaseProviderSerializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Google.validate(auth_token)

        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('No google account with such id.')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']

        return self.register_user(user_id=user_id, email=email, name=name)
