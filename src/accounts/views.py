import jwt
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, \
    RequestResetPasswordSerializer, SetNewPasswordSerializer
from .utils import Util
from .renderers import UserRender

User = get_user_model()


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRender,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = 'http://' + current_site + relative_link + "?token=" + str(token)
        email_body = render_to_string('email/request-password-reset.html',
                                      {'absurl': absurl,
                                       'username': user.username})

        data = {
            'email_body': email_body,
            'email_subject': 'Verify email',
            'to_email': user.email
        }

        Util.send_email(data)
        return Response(data=user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Token from email', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response(data={'email': 'Successfully activated.'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response(data={'error': 'Activation link is expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            print(identifier)
            return Response(data={'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetView(generics.GenericAPIView):
    serializer_class = RequestResetPasswordSerializer

    def post(self, request):
        context = {'request': request}
        serializer = self.serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relative_link = f'/password-rest-confirm/{uidb64}/{token}/'
            absurl = f'http://{current_site}{relative_link}'
            email_body = render_to_string('email/request-password-reset.html',
                                          {'absurl': absurl,
                                           'username': user.username})

            data = {
                'email_body': email_body,
                'email_subject': 'Verify email',
                'to_email': user.email
            }
            Util.send_email(data)
            return Response({'success': 'Link sent to you email.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Nobody with that email found.'}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmPasswordChangeView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    pagination_class = None

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': 'Password reset successfully.'}, status=status.HTTP_200_OK)
