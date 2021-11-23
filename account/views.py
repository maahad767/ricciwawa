from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import ReportUserSerializer, BlockUserSerializer


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


class BlockUserCreateView(generics.CreateAPIView):
    """
    Block a User API

    """
    serializer_class = BlockUserSerializer
    permission_classes = [IsAuthenticated]


class BlockUserListView(generics.ListAPIView):
    """
    Blocked/Ignored User list API
    """
    serializer_class = BlockUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.ignore_blocked_users.all()


class BlockUserDestroyView(generics.DestroyAPIView):
    """
    Unblocks a user API
    """
    serializer_class = BlockUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.ignore_blocked_users.filter(to_user__username=self.kwargs['username']).first()
