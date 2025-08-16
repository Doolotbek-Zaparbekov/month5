from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ConfirmUserAPIView, CustomTokenObtainPairView
from .views import GoogleLoginAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('confirm/', ConfirmUserAPIView.as_view(), name='confirm'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("google-login/", GoogleLoginAPIView.as_view(), name="google-login"),


]
