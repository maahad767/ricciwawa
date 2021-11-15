from django.views import generic
from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from account.models import IgnoreBlockUser
from .models import Subscription, Playlist, Post, Comment, FavouriteVocabulary, Category
from .serializers import SubscriptionSerializer, PlaylistSerializer, PostSerializer, CommentSerializer, \
    LikePostSerializer, ViewPostSerializer, FollowSerializer, FavouriteSerializer, FavouriteVocabularySerializer, \
    SavePlaylistSerializer, SubscribeSerializer, ReportPostSerializer, IgnorePostSerializer, UploadPostImageSerializer, \
    AddPostsToSubscriptionSerializer, AddPostsToPlaylistSerializer, AddPostsToCategorySerializer


class WebHome(generic.RedirectView):
    pattern_name = 'web:home'


class NewsfeedView(generics.ListAPIView):
    """
    Returns posts for newsfeed. If the user is logged in, then it returns both the public and subscribed plan's posts.
    If the user is not logged in, then it returns only public posts.
    """
    serializer_class = PostSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(Q(privacy=1)
                                       | (Q(privacy=0) &
                                          Q(subscription__in=self.request.user.subscriptions.all().values(
                                              'subscription'))))
        else:
            return Post.objects.filter(privacy=1)


class GetContentsListView(generics.ListAPIView):
    """
    Returns posts for a specific playlist or subscription.
    For Playlist's Posts : /contents/playlist/<playlist_id>/
    For Subscription's Posts : /contents/subscription/<subscription_id>/
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        content_type = self.kwargs['content_type']
        content_id = self.kwargs['id']
        if content_type == 'playlist':
            print(content_type)
            print(content_id)
            contents = Post.objects.filter(playlist=content_id)
            return contents
        elif content_type == 'subscription':
            return Post.objects.filter(subscription=content_id)
        elif content_type == 'category':
            return Post.objects.filter(category=content_id)
        else:
            return Post.objects.none()


class SubscriptionViewset(viewsets.ModelViewSet):
    """
    states: (0, 'closed'), (1, 'open')
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Subscription.objects.filter(owner=self.request.user)


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)


class PlaylistViewset(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)


class PostViewset(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)


class UserPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        owner = self.request.user
        user = get_user_model().objects.get(username=self.kwargs['username'])
        self_blocked_ignored_users = IgnoreBlockUser.objects.filter(to=user, by=owner).first()
        if self_blocked_ignored_users:
            response = {
                'error': 'you have blocked/ignored the user'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        blocked_by_target_user = IgnoreBlockUser.objects.filter(to=owner, by=user).first()
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(owner=self.request.user)


class FavouriteVocabularyViewset(viewsets.ModelViewSet):
    serializer_class = FavouriteVocabularySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavouriteVocabulary.objects.filter(user=self.request.user)


class LikePostView(generics.CreateAPIView):
    serializer_class = LikePostSerializer
    permission_classes = [IsAuthenticated]


class UnlikePostView(generics.DestroyAPIView):
    serializer_class = LikePostSerializer
    permission_classes = [IsAuthenticated]


class ViewPostView(generics.CreateAPIView):
    """
    View/Controller class for adding views to a post.
    """
    serializer_class = ViewPostSerializer
    permission_classes = [IsAuthenticated]


class FollowView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]


class UnfollowView(generics.DestroyAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]


class AddFavouriteView(generics.CreateAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]


class RemoveFavouriteView(generics.DestroyAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [IsAuthenticated]


class SavePlaylistView(generics.CreateAPIView):
    serializer_class = SavePlaylistSerializer
    permission_classes = [IsAuthenticated]


class UnsavePlaylistView(generics.DestroyAPIView):
    serializer_class = SavePlaylistSerializer
    permission_classes = [IsAuthenticated]


class SubscribeView(generics.CreateAPIView):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]


class UnsubscribeView(generics.DestroyAPIView):
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]


class ReportPostView(generics.CreateAPIView):
    serializer_class = ReportPostSerializer
    permission_classes = [IsAuthenticated]


class IgnorePostView(generics.CreateAPIView):
    serializer_class = IgnorePostSerializer
    permission_classes = [IsAuthenticated]


class UnignorePostView(generics.DestroyAPIView):
    serializer_class = IgnorePostSerializer
    permission_classes = [IsAuthenticated]


# Temporary APIs
class UploadPostImageView(generics.UpdateAPIView):
    serializer_class = UploadPostImageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Post.objects.get(id=self.kwargs['post_id'])


class AddPostsToSubscriptionsView(generics.GenericAPIView):
    serializer_class = AddPostsToSubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPostsToPlaylistView(generics.GenericAPIView):
    serializer_class = AddPostsToPlaylistSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddPostsToCategoryView(generics.GenericAPIView):
    serializer_class = AddPostsToCategorySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
