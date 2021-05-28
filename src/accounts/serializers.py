from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

User = auth.get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=70, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                'Username must only contain alphanumeric chars.')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ('token',)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=70, min_length=8, write_only=True)
    username = serializers.CharField(read_only=True)
    tokens = serializers.DictField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'tokens')

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials.')
        if not user.is_active:
            raise AuthenticationFailed('Account is disabled.')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified.')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }
