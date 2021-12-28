from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .documents import UserDocument
from .serializers import ReportUserSerializer, BlockUserSerializer, UserProfileSerializer, CheckUsernameSerializer
from dry_rest_permissions.generics import DRYPermissions


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
    permission_classes = [DRYPermissions]

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
    permission_classes = [IsAuthenticated, DRYPermissions]


class BlockUserCreateView(generics.CreateAPIView):
    """
    Block a User API

    """
    serializer_class = BlockUserSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]


class BlockUserListView(generics.ListAPIView):
    """
    Blocked/Ignored User list API
    """
    serializer_class = BlockUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.blocked_users.all()


class BlockUserDestroyView(generics.DestroyAPIView):
    """
    Unblocks a user API
    """
    serializer_class = BlockUserSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]

    def get_object(self):
        return self.request.user.blocked_users.filter(to_user__uid=self.kwargs['uid']).first()


class SearchUserView(generics.ListAPIView):
    """
    Search for a user API
    """
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        search_result = UserDocument.search().query("multi_match", query=self.kwargs['qs']).to_queryset()
        if user.is_authenticated:
            my_blocked_lists = user.blocked_users.all().values('to_user__id')
            search_result = search_result.exclude(id__in=my_blocked_lists)
        return search_result
