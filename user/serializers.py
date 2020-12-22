from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'roles', 'is_superuser', 'is_staff', 'is_active', 'is_verified')


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'state', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data["email"].lower(),
                                        username=validated_data["username"].lower(),
                                        first_name=validated_data["first_name"],
                                        last_name=validated_data["last_name"],
                                        state=validated_data["state"],
                                        password=validated_data["password"])
        return user

    def validate(self, attrs):
        filter_email = User.objects.filter(email=attrs.get('email'))
        if filter_email:
            raise serializers.ValidationError(_("Email is exist"))
        return attrs
