from rest_framework import serializers


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
