from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import ReportUserSerializer, IgnoreBlockUserSerializer


class ReportUserView(generics.CreateAPIView):
    """
    Report a User API
    status = (
        (0, 'pending'),
        (1, 'reviewed'),
    )
    """
    serializer_class = ReportUserSerializer
    permission_classes = [IsAuthenticated]


class IgnoreBlockUserCreateView(generics.CreateAPIView):
    """
    Block a User API
    _type = (
        (0, 'ignored'),
        (1, 'blocked'),
    )
    """
    serializer_class = IgnoreBlockUserSerializer
    permission_classes = [IsAuthenticated]


class IgnoreBlockUserListView(generics.ListAPIView):
    """
    Blocked/Ignored User list API
    """
    serializer_class = IgnoreBlockUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.ignore_blocked_users.all()


class IgnoreBlockUserDestroyView(generics.DestroyAPIView):
    """
    Unblocks/Un-ignore a user API
    """
    serializer_class = IgnoreBlockUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.ignore_blocked_users.filter(username=self.kwargs['username']).first()
