from attr.filters import exclude
from django.contrib.auth import get_user_model
from rest_framework import serializers

from account.fields import UsernameField
from .models import (Post, Comment, LikePost, LikeComment, Subscription, Subscribe, Playlist, SavePlaylist, ViewPost,
                     Favourite, Follow, FavouriteVocabulary, ReportPost, IgnorePost)
from .utils import upload_get_signed_up, download_get_signed_up


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = serializers.CharField(source='owner.username', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    attachment_upload_url = serializers.SerializerMethodField(read_only=True)
    attachment_url = serializers.SerializerMethodField(read_only=True)

    def get_likes(self, obj):
        return obj.likepost_set.count()

    def get_comments(self, obj):
        return obj.comments.all().count()

    def get_attachment_upload_url(self, obj):
        if obj.attachment:
            return upload_get_signed_up(obj.attachment)

    def get_attachment_url(self, obj):
        if obj.attachment:
            return download_get_signed_up(obj.attachment)

    class Meta:
        model = Post
        exclude = []


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    subscribers = serializers.SerializerMethodField(read_only=True)

    def get_subscribers(self, obj):
        return obj.subscribe_set.count()

    class Meta:
        model = Subscription
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    stories = serializers.SerializerMethodField(read_only=True)

    def get_stories(self, obj):
        return obj.post_set.all().count()

    class Meta:
        model = Playlist
        fields = '__all__'


class LikePostSerializer(serializers.ModelSerializer):
    liker = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LikePost
        fields = '__all__'


class LikeCommentSerializer(serializers.ModelSerializer):
    liker = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LikeComment
        fields = '__all__'


class ViewPostSerializer(serializers.ModelSerializer):
    viewer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ViewPost
        fields = '__all__'


class SavePlaylistSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SavePlaylist
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):
    subscriber = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscribe
        fields = '__all__'
        read_only_fields = ['is_approved']


class FollowSerializer(serializers.ModelSerializer):
    followed_user = UsernameField(queryset=get_user_model().objects.all())
    followed_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Follow
        fields = '__all__'


class FavouriteSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favourite
        fields = '__all__'


class FavouriteVocabularySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = FavouriteVocabulary
        fields = '__all__'


class IgnorePostSerializer(serializers.ModelSerializer):
    ignored_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = IgnorePost
        fields = '__all__'


class ReportPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportPost
        fields = '__all__'
