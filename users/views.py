from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, LoginSerializer, ConfirmUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import status
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user and user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Неверные учетные данные или пользователь не подтвержден.'}, status=400)


class ConfirmUserAPIView(APIView):
    def post(self, request):
        serializer = ConfirmUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Пользователь успешно подтвержден"})
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




class GoogleLoginAPIView(APIView):
    def post(self, request):
        token = request.data.get("id_token")

        if not token:
            return Response({"error": "id_token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)

            email = idinfo["email"]
            given_name = idinfo.get("given_name", "")

            family_name = idinfo.get("family_name", "")
            user, created = CustomUser.objects.get_or_create(
                username=email,
                defaults={"email": email}
            )
            user.first_name = given_name
            user.last_name = family_name
            user.save()

            
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            })

        except ValueError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
