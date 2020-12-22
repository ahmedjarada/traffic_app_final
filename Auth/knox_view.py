from django.contrib.auth import logout
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.settings import knox_settings
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import DateTimeField
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from client.models import ClientToken as client
from static_methods.Json_Response import json_response
from user.models import User as SuperUser
from user.serializers import UserSerializer, LoginSerializer


class LoginView(generics.GenericAPIView):
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def get_context(self):
        return {'request': self.request, 'format': self.format_kwarg, 'view': self}

    def get_token_ttl(self):
        return knox_settings.TOKEN_TTL

    def get_token_limit_per_user(self):
        return knox_settings.TOKEN_LIMIT_PER_USER

    def get_user_serializer_class(self):
        return knox_settings.USER_SERIALIZER

    def get_expiry_datetime_format(self):
        return knox_settings.EXPIRY_DATETIME_FORMAT

    def format_expiry_datetime(self, expiry):
        datetime_format = self.get_expiry_datetime_format()
        date = DateTimeField(format=datetime_format).to_representation(expiry)
        return date

    def get_post_response_data(self, request, token, instance):

        user_id = request.user.id
        user = SuperUser.objects.get(pk=user_id)
        data = {
            "user": UserSerializer(user, many=False).data,
            "expiry": self.format_expiry_datetime(instance.expiry),
            "token": token,
        }

        return data

    def post(self, request, format=None):
        token_limit_per_user = self.get_token_limit_per_user()
        if token_limit_per_user is not None:
            now = timezone.now()
            token = request.user.auth_token_set.filter(expiry__gt=now)
            if token.count() >= token_limit_per_user:
                return json_response(data={}, status_http=403, status_data=False, errors=['FORBIDDEN'],
                                     msg='Invalid token')
        token_ttl = self.get_token_ttl()
        instance, token = AuthToken.objects.create(request.user, token_ttl)
        user_logged_in.send(sender=request.user.__class__,
                            request=request, user=request.user)
        data = self.get_post_response_data(request, token, instance)
        try:
            ClientToken = client.objects.get(user_id=request.user)
            if ClientToken.expired_at <= timezone.now():
                ClientToken.delete()
                new_token = AuthToken.objects.create(user=request.user)[1]
                ClientToken = client.objects.create(token=new_token, user_id_id=request.user.id)
                ClientToken.save()

        except ObjectDoesNotExist:
            token = AuthToken.objects.create(user=request.user)[1]
            ClientToken = client.objects.create(token=token, user_id_id=request.user.id)
            ClientToken.save()

        ClientToken.token = data['token']
        ClientToken.expired_at = data['expiry']

        ClientToken.updated_at = timezone.now()
        ClientToken.save()

        return json_response(data=data, status_http=200, status_data=True, errors=[], msg='Login account successfully')


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request._auth.delete()

        clienttoken = client.objects.filter(user_id_id=request.user.id).delete()
        authtoken = AuthToken.objects.filter(user_id=request.user.id).delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        logout(request)
        return json_response(data={}, status_http=200, status_data=True, errors=[], msg='Success logout')


class LogoutAllView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request.user.auth_token_set.all().delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return json_response(data={}, status_http=200, status_data=True, errors=[], msg='Success logout')
