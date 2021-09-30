import os
from firebase_admin import credentials, auth, initialize_app
from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication

from .exceptions import FirebaseError, InvalidAuthToken, NoAuthToken

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
    "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.environ.get('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_CERT_URL')
})

default_app = initialize_app(cred)


class FirebaseAuthentication(BaseAuthentication):
    """
    The class creates implements authentication using Firebase Auth.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("FirebaseAuthorization")
        if not auth_header:
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
        except Exception:
            raise FirebaseError()

        user, created = settings.AUTH_USER_MODEL.objects.get_or_create(username=uid)
        user.last_login = timezone.localtime()

        return user, None
