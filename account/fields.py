from django.contrib.auth import get_user_model
from rest_framework import serializers


"""
Here we have defined custom serializer fields
"""


class UsernameField(serializers.RelatedField):

    def to_representation(self, obj):
        return obj.username

    def to_internal_value(self, data):
        try:
            username = get_user_model().objects.get(username=data)
            return username

        except KeyError:
            raise serializers.ValidationError(
                'target_username is a required field.'
            )

        except ValueError:
            raise serializers.ValidationError(
                'target_user should be username'
            )

        except get_user_model().DoesNotExist:
            raise serializers.ValidationError(
                'User does not exist.'
            )


class UserField(serializers.RelatedField):

    def to_representation(self, obj):
        user = {
            'username': obj.username,
            'name': obj.name,
            'picture': obj.picture,
        }
        return user

    def to_internal_value(self, data):
        try:
            user = get_user_model().objects.get(uid=data)
            return user

        except KeyError:
            raise serializers.ValidationError(
                'UID is a required field.'
            )

        except ValueError:
            raise serializers.ValidationError(
                'Field should be UID'
            )

        except get_user_model().DoesNotExist:
            raise serializers.ValidationError(
                'User does not exist.'
            )
