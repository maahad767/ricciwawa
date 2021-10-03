from rest_framework import serializers

from .models import ReportUser, IgnoreBlockUser


class ReportUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportUser
        fields = ['reported_user', 'reasoning', 'attachment', 'status', 'comment']
        readonly_fields = ['status', 'comment']


class IgnoreBlockUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = IgnoreBlockUser
        fields = ['to_user', 'by', '_type']
