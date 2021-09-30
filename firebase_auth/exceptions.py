from rest_framework import status
from rest_framework.exceptions import APIException


class NoAuthToken(APIException):
    """
    Exception class to raise exception when no authorization token is provided
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "No authentication token provided"
    default_code = "no_auth_token"


class InvalidAuthToken(APIException):
    """
    Exception class to raise exception when invalid authentication token is provided
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid authentication token provided"
    default_code = "invalid_token"


class FirebaseError(APIException):
    """
    Exception class to raise exception when the auth token is not a valid firebase user, has no firebase uid.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "The user provided with the auth token is not a valid Firebase user, it has no Firebase UID"
    default_code = "no_firebase_uid"
