from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from fcm_django.models import FCMDevice

from django.template import loader
from django.http import HttpResponse




from . import models, serializers, permissions


def privacy(request):
    template = loader.get_template('user/privacy.html')
    context = { }
    return HttpResponse(template.render(context, request))


class UserRegistrationView(generics.CreateAPIView):

    serializer_class = serializers.UserProfileSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data.get('id'))
        status_code = status.HTTP_201_CREATED
        response = {
            'success': 'True',
            'status code': status_code,
            'message': 'User registered  successfully with id = '+str(serializer.data['id'])
        }

        return Response(response, status=status_code)



class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        registration_id = request.data.get("registration_id")
        device_id = request.data.get("device_id")
        device_type = request.data.get("device_type")
        if registration_id and device_id and device_type:
            fcm, created = FCMDevice.objects.get_or_create(
                user=user, registration_id=registration_id, device_id=device_id)
            fcm.type = device_type
            fcm.save()

        return Response({
            'token': token.key,
            'user_id': user.pk,
        })



class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserProfileUpdateSerializer
    queryset = models.User.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile, IsAuthenticated)



class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = serializers.ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # if using drf authtoken, create a new token 
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        # return new token
        # return Response({'token': token.key}, status=status.HTTP_200_OK)
        response = {
                    'user_id': user.id,
                    'token' : token.key
                }
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_200_OK)
