from rest_framework import generics
from django.db.models import Count
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, ProductSerializer, ReviewSerializer,
    ProductWithReviewsSerializer
)
from common.validators import validate_user_is_adult
from users.permissions import IsModerator
from django.http import JsonResponse
from .tasks import add


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.annotate(products_count=Count('products'))

class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsModerator]

    def perform_create(self, serializer):
        validate_user_is_adult(self.request.user)
        serializer.save(author=self.request.user)


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    permission_classes = [IsModerator]

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

# Уже существующий класс для списка продуктов с отзывами
class ProductWithReviewsAPIView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('reviews').all()
    serializer_class = ProductWithReviewsSerializer

def run_task(request):
    result = add.delay(4, 6)  # отправляем задачу в Celery
    return JsonResponse({"task_id": result.id, "status": "started"})
