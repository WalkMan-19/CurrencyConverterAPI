from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db import transaction
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
                {'password_repeat': 'Пароли не совпадают.'}
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
            raise AuthenticationFailed("Ошибка авторизации.", )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name',]

    def validate_username(self, value):
        request = self.context.get('request')
        with transaction.atomic():
            if User.objects.exclude(id=request.user.id).filter(username=value).exists():
                raise serializers.ValidationError("Имя пользователя уже занято.")
            return value


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True)
    new_password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError('Старый пароль неверен.')
        return value

    def update(self, instance: User, validated_data: dict):
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=('password',))
        return instance
