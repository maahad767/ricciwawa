from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .serializers import ReportUserSerializer, BlockUserSerializer, UserProfileSerializer, CheckUsernameSerializer


class CheckUsernameView(generics.GenericAPIView):
    """
    Check if username is available
    """
    permission_classes = (AllowAny,)
    serializer_class = CheckUsernameSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UpdateProfileView(generics.UpdateAPIView):
    """
    Update profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


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
