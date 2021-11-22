from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import ReportUser, BlockUser
from .fields import UsernameField


class ReportUserSerializer(serializers.ModelSerializer):
    reported_user = UsernameField(queryset=get_user_model().objects.all())
    reported_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ReportUser
        fields = ['reported_user', 'reported_by', 'reasoning', 'attachment', 'status', 'comment']
        read_only_fields = ['status', 'comment']


class BlockUserSerializer(serializers.ModelSerializer):
    to_user = UsernameField(queryset=get_user_model().objects.all())
    by_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BlockUser
        fields = ['to_user', 'by_user']
