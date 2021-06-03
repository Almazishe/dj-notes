from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, VerifyEmail, LoginView, \
    ConfirmPasswordChangeView, RequestPasswordResetView, \
    LogoutView, UserMeView

urlpatterns = [
    path('social/', include('src.accounts.social_auth.urls')),

    path('me/', UserMeView.as_view(), name='me-user'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('password-reset/request/',
         RequestPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/confirm/',
         ConfirmPasswordChangeView.as_view(), name='confirm-password-reset'),
]
