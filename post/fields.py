from rest_framework import serializers

from post.models import HashTag, LikeHashTag


class AuthoredPostsPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    A PrimaryKeyRelatedField that only allows authors to access their own posts.
    """

    def get_queryset(self):
        """
        Override queryset to only return posts that are authored by the requesting user.
        """
        queryset = super().get_queryset()
        return queryset.filter(owner=self.context['request'].user)


class HashTagSerializer(serializers.ModelSerializer):
    """
    Serializer for HashTag model.
    """
    posts_count = serializers.SerializerMethodField()
    s_followed = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def get_posts_count(self, obj):
        return obj.post_set.count()

    def get_is_followed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.followhashtag_set.count() > 0

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return LikeHashTag.objects.filter(hashtag=obj, liker=user).exists()

    class Meta:
        model = HashTag
        fields = '__all__'


class HashTagPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    A PrimaryKeyRelatedField to Create and Return HashTag list
    """

    def to_representation(self, value):
        """
        Override to_representation to return a list of HashTag objects
        """
        return HashTagSerializer(value).data
        # return value.name

    def to_internal_value(self, data):
        """
        Override to_internal_value to return a list of HashTag objects
        """
        hashtag, created = HashTag.objects.get_or_create(name=data)
        return hashtag.id
