from rest_framework import serializers

from .models import (Post, Comment, LikePost, LikeComment, Subscription, Subscribe, Playlist, SavePlaylist, ViewPost,
                     Favourite, Follow, FavouriteVocabulary)


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Playlist
        fields = '__all__'


class LikePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikePost
        fields = '__all__'


class LikeCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikeComment
        fields = '__all__'


class ViewPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ViewPost
        fields = '__all__'


class SavePlaylistSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavePlaylist
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourite
        fields = '__all__'


class FavouriteVocabularySerializer(serializers.ModelSerializer):

    class Meta:
        model = FavouriteVocabulary
        fields = '__all__'
