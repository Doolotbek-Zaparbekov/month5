from rest_framework import serializers
from .models import Category, Product, Review
from django.contrib.auth.models import User
from .models import UserConfirmation

class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']
        read_only_fields = ['products_count']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Имя категории не может быть пустым.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Название продукта не может быть пустым.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше 0.")
        return value

class ReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    stars = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Текст отзыва не может быть пустым.")
        return value



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, is_active=False)
        UserConfirmation.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ConfirmUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        username = attrs.get("username")
        code = attrs.get("code")
        try:
            user = User.objects.get(username=username)
            if not hasattr(user, 'confirmation'):
                raise serializers.ValidationError("Подтверждение не найдено.")
            if user.confirmation.code != code:
                raise serializers.ValidationError("Неверный код подтверждения.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")
        return attrs

    def save(self):
        username = self.validated_data["username"]
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        user.confirmation.is_confirmed = True
        user.confirmation.save()
        return user

class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews']
