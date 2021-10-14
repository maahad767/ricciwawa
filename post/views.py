from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Subscription, Playlist, Post, Comment, FavouriteVocabulary
from .serializers import SubscriptionSerializer, PlaylistSerializer, PostSerializer, CommentSerializer, \
    LikePostSerializer, ViewPostSerializer, FollowSerializer, FavouriteSerializer, FavouriteVocabularySerializer, \
    SavePlaylistSerializer, SubscribeSerializer


class SubscriptionViewset(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Subscription.objects.filter(owner=self.request.user)


class PlaylistViewset(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)


class PostViewset(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


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
