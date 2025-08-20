from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils import generate_confirmation_code, set_confirmation_code, get_confirmation_code, delete_confirmation_code
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    birthday = serializers.DateField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'birthday']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Никнейм уже занят.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email уже используется.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            birthday=validated_data['birthday'],
            is_active=False
        )
        code = generate_confirmation_code()
        set_confirmation_code(user.id, code)
        print(f"Код для {user.username}: {code}")

        return user


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        from django.contrib.auth import authenticate
        identifier = data.get('identifier')
        password = data.get('password')

        User = get_user_model()
        user = None

        try:
            user_obj = User.objects.get(email=identifier)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = authenticate(username=identifier, password=password)

        if user is None:
            raise serializers.ValidationError("Неверные учетные данные.")
        if not user.is_active:
            raise serializers.ValidationError("Аккаунт не подтверждён.")
        data['user'] = user
        return data


class ConfirmUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        username = attrs.get("username")
        code = attrs.get("code")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")

        stored_code = get_confirmation_code(user.id)
        if not stored_code:
            raise serializers.ValidationError("Код истёк или не найден.")
        if stored_code != code:
            raise serializers.ValidationError("Неверный код подтверждения.")

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        user.is_active = True
        user.save()
        delete_confirmation_code(user.id)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['birthday'] = user.birthday.strftime('%Y-%m-%d') if user.birthday else None
        return token
