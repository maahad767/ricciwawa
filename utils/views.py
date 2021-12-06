from django.http import FileResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from .serializers import TextToSpeechSerializer, SpeechToTextSerializer, PronunciationAssessmentSerializer, \
    Mp3TaskHandlerSerializer, TranslateToChineseSerializer, TranslateSimplifiedToTraditionalSerializer, \
    UIDToIdTokenSerializer
from . import utils
from .utils import speech_tts_msft, google_translate

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
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            speech_audio_content = utils.text_to_speech(data['text'])
            with open('outfile.mp3', 'wb') as outfile:
                outfile.write(speech_audio_content)
            outfile = open('outfile.mp3', 'rb')
            return FileResponse(outfile, filename='test.mp3', as_attachment=True)

        return Response(serializer.errors)


class SpeechToTextView(generics.GenericAPIView):
    serializer_class = SpeechToTextSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            transcript = utils.speech_to_text(speech_file=request.data['speech_file'],
                                              sample_rate=request.data['sample_rate'],
                                              language_code=data['language_code'],
                                              audio_channel_count=data['audio_channel_count'])
            return Response(transcript)
        return Response(serializer.errors)


class PronunciationAssessmentView(generics.GenericAPIView):
    serializer_class = PronunciationAssessmentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            assessment_report = utils.pronunciation_assessment(speech_file=data['speech_file'],
                                                               reference_text=data['reference_text'],
                                                               language_code=data['language_code'])
            return Response(assessment_report)
        return Response(serializer.errors)


class Mp3TaskHandler(generics.GenericAPIView):
    """
    Author: Kenneth Y.
    Just wrapped for django
    """
    permission_classes = [AllowAny]
    serializer_class = Mp3TaskHandlerSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            # print(data)
            temp = utils.speech_tts_msft(data['language_code'], data['text'], data['output_filename'])
            return Response({'success': True})
        return Response({'success': False, 'errors': serializer.errors})


class TranslateToChinese(generics.GenericAPIView):
    """
    Author: Kenneth Y.
    Just wrapped for django
    """
    serializer_class = TranslateToChineseSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        text = request.data.get("text")
        translated_text = google_translate(text, "zh-TW", "en")
        return Response({'data': translated_text})


class TranslateSimplifiedToTraditional(generics.GenericAPIView):
    serializer_class = TranslateSimplifiedToTraditionalSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        text = request.data.get("text")
        translated_text = google_translate(text, "zh-CN", "zh-TW")
        return Response({'data': translated_text})


class UIDToIdTokenView(generics.GenericAPIView):
    """
    This view is used to convert a UID to an ID Token.
    You must be logged in as an Admin User to use this API.
    So, you can only use Browsable API to call this API.
    This is to make sure that the Admin can only call this API, for security purpose.
    """

    serializer_class = UIDToIdTokenSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            id_token = utils.uid_to_id_token(data['uid'])
            return Response({'id_token': id_token})
        return Response(serializer.errors)
