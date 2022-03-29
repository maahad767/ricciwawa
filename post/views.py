from django.views import generic
from django.contrib.auth import get_user_model
from django.db.models import Q
from dry_rest_permissions.generics import DRYPermissions

from rest_framework import viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .documents import PostDocument
from .models import Subscription, Playlist, Post, Comment, FavouriteVocabulary, Category, LikePost, Follow, \
    Notification, Subscribe, HashTag, LikeHashTag, FollowHashTag
from .serializers import SubscriptionSerializer, PlaylistSerializer, PostSerializer, CommentSerializer, \
    LikePostSerializer, ViewPostSerializer, FollowSerializer, FavouriteSerializer, FavouriteVocabularySerializer, \
    SavePlaylistSerializer, SubscribeSerializer, ReportPostSerializer, IgnorePostSerializer, \
    UploadPostImageSerializer, SharePostSerializer, UserInfoSerializer, NotificationSerializer, \
    NotificationMarkSeenSerializer, CategorySerializer, ResourcesSerializer, HashTagSerializer, PostListSerializer, \
    LikeHashTagSerializer, FollowHashTagSerializer


class WebHome(generic.RedirectView):
    pattern_name = 'web:home'


class NewsfeedView(generics.ListAPIView):
    """
    Returns posts for newsfeed. If the user is logged in, then it returns both the public and subscribed plan's posts.
    If the user is not logged in, then it returns only public posts.
    privacy: 0-private, 1-public
    attachment_type: 0-none, 1-image, 2-audio, 3-video
    """
    serializer_class = PostListSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        myself = self.request.user
        if myself.is_authenticated:
            my_posts = Post.objects.filter(owner=self.request.user)
            my_subscriptions = myself.subscriptions.all().values('subscription')
            my_blocked_lists = myself.blocked_users.all().values('to_user__id')
            my_ignored_posts = myself.ignorepost_set.all().values('ignored_post')
            qs = (Post.objects.filter(Q(privacy=1) | (Q(privacy=0) & Q(subscription__in=my_subscriptions))).filter(
                ~Q(owner__in=my_blocked_lists)).filter(~Q(id__in=my_ignored_posts)) | my_posts).distinct().order_by()
        else:
            qs = Post.objects.filter(privacy=1)
        return qs.order_by('?')


class GetContentsListView(generics.ListAPIView):
    """
    Returns posts for a specific playlist or subscription.
    For Playlist's Posts : /contents/playlist/<playlist_id>/
    For Subscription's Posts : /contents/subscription/<subscription_id>/
    For Category's Posts : /contents/category/<category_id>/
    For HashTag's Posts : /contents/hashtag/<hashtag_id>/
    privacy: 0-private, 1-public
    attachment_type: 0-none, 1-image, 2-audio, 3-video
    """
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        content_type = self.kwargs['content_type']
        content_id = self.kwargs['id']
        if content_type == 'playlist':
            return Post.objects.filter(playlist__id=content_id).order_by('position')
        elif content_type == 'subscription':
            return Post.objects.filter(subscription__id=content_id).order_by('position')
        elif content_type == 'category':
            return Post.objects.filter(category__id=content_id).order_by('position')
        elif content_type == 'hashtag':
            return Post.objects.filter(hashtags__id=content_id).order_by('position')
        else:
            return Post.objects.none()


class LikedPostsView(generics.ListAPIView):
    """
    Returns posts liked by the user.
    """
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        myself = self.request.user
        return Post.objects.filter(id__in=myself.likepost_set.values('post'))


class SubscriptionViewset(viewsets.ModelViewSet):
    """
    states: (0, 'closed'), (1, 'open')
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [DRYPermissions]

    def get_queryset(self):
        return Subscription.objects.filter(owner=self.request.user)

    def get_object(self):
        return Subscription.objects.get(id=self.kwargs['pk'])


class SubscribedPlansView(generics.ListAPIView):
    """
    Returns all the subscribed plans.
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(
            id__in=self.request.user.subscriptions.values_list('subscription', flat=True))


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, DRYPermissions]

    def get_queryset(self):
        return Category.objects.filter(subscription__owner=self.request.user)


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
    permission_classes = [DRYPermissions]

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer

        return PostSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(owner=self.request.user)
        return Post.objects.none()


class ResourcesView(generics.RetrieveAPIView):
    serializer_class = ResourcesSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return Post.objects.get(id=self.kwargs['id'])


class UserPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [AllowAny, DRYPermissions]

    def get_queryset(self):
        myself = self.request.user
        uid = self.kwargs['uid'].strip()
        if uid == 'self':
            return Post.objects.filter(owner=myself)
        user = get_user_model().objects.get(uid=uid)
        if myself.is_authenticated:
            my_subscriptions = myself.subscriptions.all().values('subscription')
            my_blocked_lists = myself.blocked_users.all().values('to_user__id')
            return (Post.objects.filter(owner=user).filter(Q(privacy=1) |
                                                           (Q(privacy=0) & Q(subscription__in=my_subscriptions)))
                    .filter(~Q(owner__in=my_blocked_lists))).distinct()
        else:
            return Post.objects.filter(owner=user, privacy=1)


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny, DRYPermissions]

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
        return get_object_or_404(LikePost, post__id=post_id, liker=user)


class ViewPostView(generics.CreateAPIView):
    """
    View/Controller class for adding views to a post.
    """
    serializer_class = ViewPostSerializer
    permission_classes = [AllowAny]


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
        return Follow.objects.filter(followed_by=follower, followed_user__uid=user_id).first()


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

    def get_object(self):
        subscription_id = self.kwargs.get('subscription_id')
        return Subscribe.objects.filter(subscription=subscription_id, subscriber=self.request.user).first()


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


class NotificationView(generics.ListAPIView):
    """
    Use only Create Notification(method POST) and Get Notification(method GET, returns list)
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.notifications_received.all()


class MarkNotificationSeenView(generics.GenericAPIView):
    """
    Notification Types:
        (0, 'announcement'),
        (10, 'like'),
        (20, 'comment'),
        (30, 'follow'),
        (40, 'subscribe')
    """

    serializer_class = NotificationMarkSeenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        notification_ids = self.request.body['notifications']
        return Notification.objects.filter(id__in=notification_ids, to_user=user)

    def post(self, request, *args, **kwargs):
        notifications = self.get_queryset()

        notifications.update(is_seen=True)
        notifications.save()


class SearchPostView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        myself = self.request.user
        search_result = PostDocument.search()\
            .query("multi_match", query=f'{self.kwargs["qs"]}', fields=['title', 'description', 'text'])\
            .to_queryset()

        if myself.is_authenticated:
            my_subscriptions = myself.subscriptions.all().values('subscription')
            my_blocked_lists = myself.blocked_users.all().values('to_user__id')
            my_ignored_posts = myself.ignorepost_set.all().values('ignored_post')
            return search_result.filter(Q(privacy=1) | (Q(privacy=0) & Q(subscription__in=my_subscriptions))).filter(
                ~Q(owner__in=my_blocked_lists)).filter(~Q(id__in=my_ignored_posts))
        else:
            return search_result.filter(privacy=1)


class SearchHashTagView(generics.ListAPIView):
    serializer_class = HashTagSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return HashTag.objects.filter(name__icontains=self.kwargs['qs'].strip())


class LikeHashTagView(generics.CreateAPIView, generics.DestroyAPIView, viewsets.GenericViewSet):
    serializer_class = LikeHashTagSerializer
    permission_classes = [DRYPermissions]

    def get_object(self):
        return get_object_or_404(LikeHashTag, user=self.request.user, hashtag__id=self.kwargs['pk'])


class FollowHashTagView(generics.CreateAPIView, generics.DestroyAPIView, viewsets.GenericViewSet):
    serializer_class = FollowHashTagSerializer
    permission_classes = [DRYPermissions]

    def get_object(self):
        return get_object_or_404(FollowHashTag, user=self.request.user, hashtag__id=self.kwargs['pk'])


class HashTagViewSet(viewsets.ModelViewSet):
    serializer_class = HashTagSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return HashTag.objects.all()
