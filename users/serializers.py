from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from users.fields import PasswordField
from users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'password_repeat',
        ]

    def validate(self, attrs: dict) -> dict:
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError(
                {'password_repeat': 'Пароли должны совпадать.'}
            )
        return attrs

    def create(self, validated_data: dict) -> User:
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
        ]

    def create(self, validated_data) -> User:
        if not(user := authenticate(
            username=validated_data["username"],
            password=validated_data["password"],
        )):
            raise AuthenticationFailed
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name',]


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True)
    new_password = PasswordField(required=True)

    def validate_new_password(self, value):
        if not self.instance.check_password(value):
            raise ValidationError('password is incorrect')
        return value

    def update(self, instance: User, validated_data: dict):
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=('password', ))
        return instance

    def create(self, validated_data):
        raise NotImplementedError
