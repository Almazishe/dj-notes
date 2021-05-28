from django.urls import path
from .views import RegisterView, VerifyEmail, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
]
