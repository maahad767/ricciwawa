from rest_framework import serializers

from post.models import HashTag


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


class HashTagPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    A PrimaryKeyRelatedField to Create and Return HashTag list
    """

    def to_representation(self, value):
        """
        Override to_representation to return a list of HashTag objects
        """
        return value.name

    def to_internal_value(self, data):
        """
        Override to_internal_value to return a list of HashTag objects
        """
        hashtag, created = HashTag.objects.get_or_create(name=data)
        return hashtag.id
