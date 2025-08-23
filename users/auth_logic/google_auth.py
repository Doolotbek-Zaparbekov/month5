from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import CustomUser


def authenticate_with_google(id_token_str: str):


    try:
        idinfo = id_token.verify_oauth2_token(
            id_token_str,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )
    except ValueError:
        return None, {"error": "Invalid token"}

    email = idinfo["email"]
    given_name = idinfo.get("given_name", "")
    family_name = idinfo.get("family_name", "")

    user, created = CustomUser.objects.get_or_create(
        username=email,
        defaults={"email": email}
    )
    user.first_name = given_name
    user.last_name = family_name
    user.is_active = True  
    user.save()

    refresh = RefreshToken.for_user(user)

    return user, {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    }
