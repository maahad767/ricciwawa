from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import ReportUser, BlockUser
from .fields import UserField


class CheckUsernameSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        if get_user_model().objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    """
    class Meta:
        model = get_user_model()
        fields = ('uid', 'username', 'picture', 'name')


class ReportUserSerializer(serializers.ModelSerializer):
    reported_user = UserField(queryset=get_user_model().objects.all())
    reported_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ReportUser
        fields = ['reported_user', 'reported_by', 'reasoning', 'attachment', 'status', 'comment']
        read_only_fields = ['status', 'comment']


class BlockUserSerializer(serializers.ModelSerializer):
    to_user = UserField(queryset=get_user_model().objects.all())
    by_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BlockUser
        fields = ['to_user', 'by_user']
