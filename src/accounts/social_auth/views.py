import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import GoogleAuthSerializer, FacebookAuthSerializer


class BaseSocialAuthView(GenericAPIView):
    pagination_class = None

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class GoogleAuthView(BaseSocialAuthView):
    serializer_class = GoogleAuthSerializer


class FacebookAuthView(BaseSocialAuthView):
    serializer_class = FacebookAuthSerializer
