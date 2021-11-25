from attr.filters import exclude
from django.contrib.auth import get_user_model
from rest_framework import serializers

from account.fields import UsernameField, UserField
from .models import (Post, Comment, LikePost, LikeComment, Subscription, Category, Subscribe, Playlist, SavePlaylist,
                     ViewPost,
                     Favourite, Follow, FavouriteVocabulary, ReportPost, IgnorePost, SharePost, Notification)
from .utils import upload_get_signed_up, download_get_signed_up


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = UserField(source='owner', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    attachment_upload_url = serializers.SerializerMethodField(read_only=True)
    attachment_url = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    shares = serializers.SerializerMethodField(read_only=True)
    audio_simplified_chinese_url = serializers.SerializerMethodField(read_only=True)
    audio_traditional_chinese_url = serializers.SerializerMethodField(read_only=True)
    timing_simplified_chinese_url = serializers.SerializerMethodField(read_only=True)
    timing_traditional_chinese_url = serializers.SerializerMethodField(read_only=True)

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

    def get_audio_simplified_chinese_url(self, obj):
        if obj.audio_simplified_chinese:
            return download_get_signed_up(obj.audio_simplified_chinese)

    def get_audio_traditional_chinese_url(self, obj):
        if obj.audio_traditional_chinese:
            return download_get_signed_up(obj.audio_traditional_chinese)

    def get_timing_simplified_chinese_url(self, obj):
        if obj.timing_simplified_chinese:
            return download_get_signed_up(obj.timing_simplified_chinese)

    def get_timing_traditional_chinese_url(self, obj):
        if obj.timing_traditional_chinese:
            return download_get_signed_up(obj.timing_traditional_chinese)

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return LikePost.objects.filter(post=obj, liker=user).exists()
        return False

    def get_shares(self, obj):
        return obj.sharepost_set.all().count()

    class Meta:
        model = Post
        exclude = []


class UploadPostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('image',)


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = UserField(source='owner', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    def get_likes(self, obj):
        return obj.likecomment_set.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return LikeComment.objects.filter(comment=obj, liker=user).exists()
        return False

    class Meta:
        model = Comment
        fields = '__all__'


class SubscribeSerializer(serializers.ModelSerializer):
    subscriber = serializers.HiddenField(default=serializers.CurrentUserDefault())
    subscribed_by = UserField(source='subscriber', read_only=True)

    class Meta:
        model = Subscribe
        fields = '__all__'
        read_only_fields = ['is_approved']
        extra_kwargs = {
            'subscription': {'write_only': True}
        }


class CategorySerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=True, write_only=True, required=False)

    def create(self, validated_data):
        posts = validated_data.pop('posts') if 'posts' in validated_data else []
        category = super(CategorySerializer, self).create(validated_data)
        for post in posts:
            post.category = category
            post.save()

        return category

    class Meta:
        model = Category
        exclude = []
        extra_kwargs = {
            'subscription': {'write_only': True}
        }


class SubscriptionSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    subscribers = serializers.SerializerMethodField(read_only=True)
    subscriber_list = SubscribeSerializer(source='subscribe_set', many=True, read_only=True)
    category_list = CategorySerializer(source='category_set', many=True, read_only=True)
    posts = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=True, write_only=True, required=False)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscribe.objects.filter(subscription=obj, subscriber=user).exists()
        return False

    def get_subscribers(self, obj):
        return obj.subscribe_set.count()

    def create(self, validated_data):
        posts = validated_data.pop('posts') if 'posts' in validated_data else []
        subscription = super(SubscriptionSerializer, self).create(validated_data)
        for post in posts:
            post.subscription = subscription
            post.save()

        return subscription

    class Meta:
        model = Subscription
        exclude = []


class PlaylistSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    author = UserField(source='owner', read_only=True)
    stories = serializers.SerializerMethodField(read_only=True)
    posts = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=True, write_only=True, required=False)

    def get_stories(self, obj):
        return obj.post_set.all().count()

    def create(self, validated_data):
        posts = validated_data.pop('posts') if 'posts' in validated_data else []
        playlist = super(PlaylistSerializer, self).create(validated_data)
        for post in posts:
            post.playlist = playlist
            post.save()

        return playlist

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


class SharePostSerializer(serializers.ModelSerializer):
    sharer = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SharePost
        fields = '__all__'


class SavePlaylistSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SavePlaylist
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    followed_user = UserField(queryset=get_user_model().objects.all())
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


class AddPostsToSubscriptionSerializer(serializers.Serializer):
    subscription = serializers.PrimaryKeyRelatedField(queryset=Subscription.objects.all())
    posts = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=True)

    def save(self):
        subscription = self.validated_data['subscription']
        posts = self.validated_data['posts']
        for post in posts:
            post.subscription = subscription
            post.privacy = 0
            post.save()


class AddPostsToPlaylistSerializer(serializers.Serializer):
    playlist = serializers.PrimaryKeyRelatedField(queryset=Playlist.objects.all())
    posts = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=True)

    def save(self):
        playlist = self.validated_data['playlist']
        posts = self.validated_data['posts']
        for post in posts:
            post.playlist = playlist
            post.save()


class AddPostsToCategorySerializer(serializers.Serializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    posts = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), many=True)

    def save(self):
        category = self.validated_data['category']
        posts = self.validated_data['posts']
        for post in posts:
            post.category = category
            post.save()


class UserInfoSerializer(serializers.ModelSerializer):
    is_followed = serializers.SerializerMethodField()

    def get_is_followed(self, obj):
        followed_user = self.context['request'].query_params.get('username', None)
        if not followed_user:
            return False
        return obj.following.filter(followed_user=followed_user).exists()

    class Meta:
        model = get_user_model()
        fields = ['username', 'is_followed']
        read_only_fields = ['username']


class NotificationSerializer(serializers.ModelSerializer):
    from_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    to_user = UserField(queryset=get_user_model().objects.all())

    class Meta:
        model = Notification
        fields = '__all__'


class NotificationMarkSeenSerializer(serializers.ModelSerializer):
    to_user = UserField(queryset=get_user_model().objects.all())

    class Meta:
        model = Notification
        fields = ['id', 'to_user']
