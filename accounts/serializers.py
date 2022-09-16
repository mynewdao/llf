from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts.send_email import send_code_email

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(min_length=6, write_only=True)
    password2 = serializers.CharField(min_length=6, write_only=True)


    class Meta:
        model = User
        fields = ("email", "password1", "password2", "full_name")
        extra_kwargs = {
            "full_name": {"required": True}
        }


    def validate_email(self, data): #в дату попадет то что указали после валидэйт это mail
        result = User.objects.filter(email=data).exists
        if not result:
            raise serializers.ValidationError("already exists!")
        return data

    def validate(self, attrs):
        password = attrs.pop("password1")
        password2 = attrs.pop("password2")
        if password != password2:
            raise serializers.ValidationError("dont match")
        attrs['password'] = password
        return attrs

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.create_activation_code()
        user.save()
        send_code_email(user)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(min_length=6, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email is None:
            raise serializers.ValidationError("Email is required!")
        if password is None:
            raise serializers.ValidationError("Password is required!")
        return attrs

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.get(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('User not found')
        if not user.is_active:
            raise serializers.ValidationError('User not active')
        token_key, _ = Token.objects.get_or_create(user=user) #возвращает тапл, get_or_create возвращает нового пользлвателяя
                                                              # или еще булиан в _ приходит как в переменную тру или фолс
                                                              # исп всегда _ для передачи переменной

        return {
            "token": token_key
        }