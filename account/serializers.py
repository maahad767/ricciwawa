from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from post.fields import HashTagPrimaryKeyRelatedField
from post.models import HashTag
from .models import ReportUser, BlockUser
from .fields import UserField


class CheckUsernameSerializer(serializers.Serializer):
    username_validator = UnicodeUsernameValidator()
    username = serializers.CharField(max_length=150, validators=[username_validator],
                                     error_messages={
                                         'unique': "A user with that username already exists.",
                                     })

    def validate_username(self, value):
        if get_user_model().objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists')
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model.
    """
    hashtags = HashTagPrimaryKeyRelatedField(many=True, queryset=HashTag.objects.all())

    class Meta:
        model = get_user_model()
        fields = ('uid', 'username', 'picture', 'name', 'description', 'background_image', 'birthday',
                  'gender', 'country', 'language', 'hashtags')
        read_only_fields = ['uid']


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
