from abc import ABC

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from user.models import User


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = None
        username = None
        user = None
        email = attrs.get('email').lower()
        password = attrs.get('password')

        if email is not None:
            if '@' in email:
                print("@@@")
                try:
                    username = User.objects.get(email=email).username
                except User.DoesNotExist as e:
                    # print()
                    raise serializers.ValidationError({'0':
                                                           'The email or username with password you\'ve is incorrect!'})
                if username is not None:
                    user = authenticate(request=self.context.get('request'),
                                        username=username, password=password)
            if '@' not in email:
                user = authenticate(request=self.context.get('request'),
                                    username=email, password=password)
        else:
            print("not username")
            if not user:
                print("not user")
                raise serializers.ValidationError({'0':
                                                       'The email or username with password you\'ve is incorrect!'})

            else:
                raise serializers.ValidationError({'0': 'Must include "email" and "password"'})

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
        attrs['user'] = user
        return attrs
