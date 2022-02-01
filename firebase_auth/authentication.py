import os

from django.contrib.auth import get_user_model
from firebase_admin import credentials, auth, initialize_app
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.settings import api_settings

from .exceptions import FirebaseError, InvalidAuthToken, NoAuthToken


cred = credentials.Certificate(os.environ.get('SERVICE_ACCOUNT_KEY', 'ricciwawa-6e11b342c999.json'))
default_app = initialize_app(cred)


class FirebaseAuthentication(BaseAuthentication):
    """
    The class creates implements authentication using Firebase Auth.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("FirebaseAuthorization")
        if not auth_header:
            if AllowAny in api_settings.DEFAULT_PERMISSION_CLASSES:
                return None
            raise NoAuthToken("No auth token provided")

        id_token = auth_header.split(" ").pop()
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken("Invalid auth token")

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
            name = decoded_token.get("name")

        except Exception:
            raise FirebaseError()

        user, created = get_user_model().objects.get_or_create(uid=uid)
        if created:
            user.name = name
            user.save()

        user.last_login = timezone.localtime()

        return user, None
