from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ConfirmUserAPIView, CustomTokenObtainPairView

urlpatterns = [
    path('users/register/', RegisterAPIView.as_view(), name='register'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/confirm/', ConfirmUserAPIView.as_view(), name='confirm'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),


]
