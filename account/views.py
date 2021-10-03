from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import ReportUserSerializer, IgnoreBlockUserSerializer


class ReportUserView(generics.CreateAPIView):
    """
    Report a User API
    """
    serializer_class = ReportUserSerializer
    permission_classes = [IsAuthenticated]


class IgnoreBlockUserCreateView(generics.CreateAPIView):
    """
    Block a User API
    """
    serializer_class = IgnoreBlockUserSerializer
    permission_classes = [IsAuthenticated]


class IgnoreBlockUserListView(generics.ListAPIView):
    """
    Blocked/Ignored User list API
    """
    serializer_class = IgnoreBlockUserSerializer
    permission_classes = [IsAuthenticated]


class IgnoreBlockUserDestroyView(generics.DestroyAPIView):
    """
    Unblocks/Un-ignore a user API
    """
    serializer_class = IgnoreBlockUserSerializer
    permission_classes = [IsAuthenticated]
