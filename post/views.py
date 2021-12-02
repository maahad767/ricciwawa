from django.views import generic
from django.contrib.auth import get_user_model
from django.db.models import Q
from dry_rest_permissions.generics import DRYPermissions

from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from account.models import BlockUser
from .documents import PostDocument
from .models import Subscription, Playlist, Post, Comment, FavouriteVocabulary, Category, LikePost, Follow, Notification
from .serializers import SubscriptionSerializer, PlaylistSerializer, PostSerializer, CommentSerializer, \
    LikePostSerializer, ViewPostSerializer, FollowSerializer, FavouriteSerializer, FavouriteVocabularySerializer, \
    SavePlaylistSerializer, SubscribeSerializer, ReportPostSerializer, IgnorePostSerializer, \
    UploadPostImageSerializer, AddPostsToSubscriptionSerializer, AddPostsToPlaylistSerializer, \
    AddPostsToCategorySerializer, SharePostSerializer, UserInfoSerializer, NotificationSerializer, \
    NotificationMarkSeenSerializer, CategorySerializer


class WebHome(generic.RedirectView):
    pattern_name = 'web:home'


class NewsfeedView(generics.ListAPIView):
    """
    Returns posts for newsfeed. If the user is logged in, then it returns both the public and subscribed plan's posts.
    If the user is not logged in, then it returns only public posts.
    privacy: 0-private, 1-public
    attachment_type: 0-none, 1-image, 2-audio, 3-video
    """
    serializer_class = PostSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        myself = self.request.user
        if myself.is_authenticated:
            my_posts = Post.objects.filter(owner=self.request.user)
            my_subscriptions = myself.subscriptions.all().values('subscription')
            my_blocked_lists = myself.ignore_blocked_users.all().values('to_user__id')
            my_ignored_posts = myself.ignorepost_set.all().values('ignored_post')
            return (Post.objects.filter(Q(privacy=1) | (Q(privacy=0) & Q(subscription__in=my_subscriptions))).filter(
                ~Q(owner__in=my_blocked_lists)).filter(~Q(id__in=my_ignored_posts)) | my_posts).distinct()
        else:
            return Post.objects.filter(privacy=1)


class GetContentsListView(generics.ListAPIView):
    """
    Returns posts for a specific playlist or subscription.
    For Playlist's Posts : /contents/playlist/<playlist_id>/
    For Subscription's Posts : /contents/subscription/<subscription_id>/
    privacy: 0-private, 1-public
    attachment_type: 0-none, 1-image, 2-audio, 3-video
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]

    def get_queryset(self):
        content_type = self.kwargs['content_type']
        content_id = self.kwargs['id']
        if content_type == 'playlist':
            return Post.objects.filter(playlist__id=content_id)
        elif content_type == 'subscription':
            return Post.objects.filter(subscription__id=content_id)
        elif content_type == 'category':
            return Post.objects.filter(category__id=content_id)
        else:
            return Post.objects.none()


class SubscriptionViewset(viewsets.ModelViewSet):
    """
    states: (0, 'closed'), (1, 'open')
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny, DRYPermissions]

    def get_queryset(self):
        return Subscription.objects.filter(owner=self.request.user)


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, DRYPermissions]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)


class CategoryListCreateView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, DRYPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PlaylistViewset(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)


class PostViewset(viewsets.ModelViewSet):
    """
    privacy = (0, 'private'), (1, 'public')
    attachment_type: 0-none, 1-image, 2-audio, 3-video
    """
    serializer_class = PostSerializer
    permission_classes = [AllowAny, DRYPermissions]

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)


class UserPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, DRYPermissions]

    def get_queryset(self):
        owner = self.request.user
        user = get_user_model().objects.get(uid=self.kwargs['uid'])

        if not owner.is_authenticated:
            return Post.objects.filter(owner=user, privacy=1)

        # if the user is logged in, then it returns both the public and subscribed plan's posts.
        # if the user is blocked by the user or blocked by the profile owner,
        # then it returns HTTP_400_BAD_REQUEST response,
        self_blocked_ignored_users = BlockUser.objects.filter(to=user, by=owner).first()
        if self_blocked_ignored_users:
            response = {
                'error': 'you have blocked/ignored the user'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        blocked_by_target_user = BlockUser.objects.filter(to_user=owner, by_user=user).first()
        if blocked_by_target_user:
            response = {
                'error': 'you are blocked/ignored by the user'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        return Post.objects.filter(owner=user).filter(Q(privacy=1)
                                                      | (Q(privacy=0)
                                                         & Q(subscription__in=owner.subscriptions.values(
                                                                  'subscription'))))


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]

    def get_queryset(self):
        return Comment.objects.filter(owner=self.request.user)


class FavouriteVocabularyViewset(viewsets.ModelViewSet):
    serializer_class = FavouriteVocabularySerializer
    permission_classes = [IsAuthenticated, DRYPermissions]

    def get_queryset(self):
        return FavouriteVocabulary.objects.filter(user=self.request.user)


class LikePostView(generics.CreateAPIView):
    serializer_class = LikePostSerializer
    permission_classes = [IsAuthenticated]


class UnlikePostView(generics.DestroyAPIView):
    serializer_class = LikePostSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        post_id = self.kwargs['post_id']
        user = self.request.user
        return LikePost.objects.get(post__id=post_id, liker=user)


class ViewPostView(generics.CreateAPIView):
    """
    View/Controller class for adding views to a post.
    """
    serializer_class = ViewPostSerializer
    permission_classes = [IsAuthenticated]


class SharePostView(generics.CreateAPIView):
    """
    Creates a share to count how many share a post has.
    """
    serializer_class = SharePostSerializer
    permission_classes = [AllowAny]


class FollowView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]


class UnfollowView(generics.DestroyAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]

    def get_object(self):
        user_id = self.kwargs.get('uid')
        follower = self.request.user
        return Follow.objects.get(followed_by=follower, followed_user__username=user_id)


class AddFavouriteView(generics.CreateAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]


class RemoveFavouriteView(generics.DestroyAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]


class SavePlaylistView(generics.CreateAPIView):
    serializer_class = SavePlaylistSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]


class UnsavePlaylistView(generics.DestroyAPIView):
    serializer_class = SavePlaylistSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]


class SubscribeView(generics.CreateAPIView):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]


class UnsubscribeView(generics.DestroyAPIView):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]


class ReportPostView(generics.CreateAPIView):
    serializer_class = ReportPostSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]


class IgnorePostView(generics.CreateAPIView):
    serializer_class = IgnorePostSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]


class UnignorePostView(generics.DestroyAPIView):
    serializer_class = IgnorePostSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]


# Temporary APIs
class UploadPostImageView(generics.UpdateAPIView):
    serializer_class = UploadPostImageSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]

    def get_object(self):
        return Post.objects.get(id=self.kwargs['post_id'])


class AddPostsToSubscriptionsView(generics.GenericAPIView):
    serializer_class = AddPostsToSubscriptionSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPostsToPlaylistView(generics.GenericAPIView):
    serializer_class = AddPostsToPlaylistSerializer
    permission_classes = [IsAuthenticated, DRYPermissions]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPostsToCategoryView(generics.GenericAPIView):
    serializer_class = AddPostsToCategorySerializer
    permission_classes = [IsAuthenticated, DRYPermissions]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCommentsByParentIDView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(parent__id=self.kwargs['parent_id'])


class GetCommentsByPostIDView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Comment.objects.filter(post__id=self.kwargs['post_id'])


class GetSubscriptionsByUserView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Subscription.objects.filter(owner__uid=self.kwargs['uid'])


class GetPlaylistsByUserView(generics.ListAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Playlist.objects.filter(owner__uid=self.kwargs['uid'])


class GetUserInfoView(generics.RetrieveAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        uid = self.request.query_params.get('uid')
        if uid:
            return get_user_model().objects.get(uid=uid)
        return self.request.user


class NotificationViewset(viewsets.ModelViewSet):
    """
    Use only Create Notification(method POST) and Get Notification(method GET, returns list)
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notifications_received.all()


class MarkNotificationSeenView(generics.GenericAPIView):
    serializer_class = NotificationMarkSeenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        notification_ids = self.request.kwargs['notifications']
        return Notification.objects.filter(id__in=notification_ids, to_user=user)

    def post(self, request, *args, **kwargs):
        notifications = self.get_queryset()

        notifications.bulk_update(is_seen=True)
        notifications.save()


class SearchPostView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        search_result = PostDocument.search().query("multi_match", query=self.kwargs['qs'])
        return search_result.to_queryset()
