from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import TextToSpeechSerializer, SpeechToTextSerializer, PronunciationAssessmentSerializer

"""
The file contains View Classes for utility APIs such as Text To Speech, Speech To Text, etc. 
Most of the classes contain some common terms which are briefly explained below.

serializer_class - it takes a serializer class which will be used to serialize from and to JSON data.
                   And it is also used to validate using data type, and restrictions.
                   It can also create, update data if it's a child of ModelSerializer.
                   
permission_class - it specifies which permission class/set of classes to use to manage accessibility of the 
                   View Class. For example, if IsAuthenticated is added as permission class, to call the API
                   the user must be authenticated first.
"""


class TextToSpeechView(generics.GenericAPIView):
    serializer_class = TextToSpeechSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request)
        if serializer.is_valid():
            pass
        return Response(serializer.errors)


class SpeechToTextView(generics.GenericAPIView):
    serializer_class = SpeechToTextSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request)
        if serializer.is_valid():
            pass
        return Response(serializer.errors)


class PronunciationAssessmentView(generics.GenericAPIView):
    serializer_class = PronunciationAssessmentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(request)
        if serializer.is_valid():
            pass
        return Response(serializer.errors)
