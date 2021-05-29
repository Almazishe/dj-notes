from django.urls import path
from .views import GoogleAuthView, FacebookAuthView

urlpatterns = [
    path('google/', GoogleAuthView.as_view(), name='google-auth'),
    path('facebook/', FacebookAuthView.as_view(), name='facebook-auth')
]
