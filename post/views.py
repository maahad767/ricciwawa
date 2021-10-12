from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Subscription, Playlist, Post
from .serializers import SubscriptionSerializer, PlaylistSerializer, PostSerializer


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
