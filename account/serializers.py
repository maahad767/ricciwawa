from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import ReportUser, IgnoreBlockUser


# Custom Fields
class UsernameField(serializers.RelatedField):

    def to_representation(self, obj):
        return obj.username

    def to_internal_value(self, data):
        try:
            reported_user = get_user_model().objects.get(username=data)
            if reported_user == serializers.CurrentUserDefault():
                raise serializers.ValidationError(
                    'Can not report yourself!'
                )
            return reported_user

        except KeyError:
            raise serializers.ValidationError(
                'reported_user is a required field.'
            )

        except ValueError:
            raise serializers.ValidationError(
                'reported_user should be username'
            )

        except get_user_model().DoesNotExist:
            raise serializers.ValidationError(
                'User does not exist.'
            )


class ReportUserSerializer(serializers.ModelSerializer):
    reported_user = UsernameField(queryset=get_user_model().objects.all())
    reported_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ReportUser
        fields = ['reported_user', 'reported_by', 'reasoning', 'attachment', 'status', 'comment']
        read_only_fields = ['status', 'comment']


class IgnoreBlockUserSerializer(serializers.ModelSerializer):
    to = UsernameField(queryset=get_user_model().objects.all())
    by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = IgnoreBlockUser
        fields = ['to', 'by', '_type']
