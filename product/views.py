from rest_framework import generics
from django.db.models import Count
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, ProductSerializer, ReviewSerializer,
    ProductWithReviewsSerializer
)

class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.annotate(products_count=Count('products'))

class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

class ProductWithReviewsAPIView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('reviews').all()
    serializer_class = ProductWithReviewsSerializer
