from django.urls import path
from .views import (
    CategoryListAPIView, CategoryDetailAPIView,
    ProductListAPIView, ProductDetailAPIView,
    ReviewListAPIView, ReviewDetailAPIView,
    ProductWithReviewsAPIView
)

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:id>/', CategoryDetailAPIView.as_view(), name='category-detail'),

    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/reviews/', ProductWithReviewsAPIView.as_view(), name='product-with-reviews'),

    path('reviews/', ReviewListAPIView.as_view(), name='review-list'),
    path('reviews/<int:id>/', ReviewDetailAPIView.as_view(), name='review-detail'),

]
