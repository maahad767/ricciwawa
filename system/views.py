from rest_framework import generics
from rest_framework.permissions import AllowAny

from system.models import VersionInfo
from system.serializers import VersionInfoSerializer


class VersionInfoView(generics.RetrieveAPIView):
    """
    API endpoint that allows version info to be viewed.
    """
    serializer_class = VersionInfoSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return VersionInfo.objects.first()
