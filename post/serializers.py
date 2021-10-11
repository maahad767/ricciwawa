from rest_framework import serializers

from .models import (Post, Comment, LikePost, LikeComment, Subscription, Subscribe, Playlist, SavePlaylist, ViewPost,
                     Favourite, Follow)


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription


class PlaylistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Playlist


class LikePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikePost


class LikeCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikeComment


class ViewPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ViewPost


class SavePlaylistSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavePlaylist


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
