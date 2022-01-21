from rest_framework import serializers

from system.models import VersionInfo


class VersionInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for the VersionInfo model.
    """

    class Meta:
        model = VersionInfo
        exclude = ['id']
