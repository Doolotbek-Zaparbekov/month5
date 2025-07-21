from django.urls import path
from .views import (
    CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView,
    ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView,
    ReviewListCreateAPIView, ReviewRetrieveUpdateDestroyAPIView,
    ProductWithReviewsAPIView
)

urlpatterns = [
    # Категории
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:id>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-rud'),

    # Продукты
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:id>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-rud'),

    # Отзывы
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('reviews/<int:id>/', ReviewRetrieveUpdateDestroyAPIView.as_view(), name='review-rud'),

    # Продукты с отзывами и рейтингом
    path('products/reviews/', ProductWithReviewsAPIView.as_view(), name='product-with-reviews'),
]
