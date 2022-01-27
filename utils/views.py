import timeit

from django.http import FileResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from .serializers import TextToSpeechSerializer, SpeechToTextSerializer, PronunciationAssessmentSerializer, \
    Mp3TaskHandlerSerializer, TranslateChineseSerializer, TranslateSimplifiedToTraditionalSerializer, \
    UIDToIdTokenSerializer, WordGroupingSerializer, STTSerializer, STTResultSerializer
from . import utils
from .utils import upload_get_signed_up, google_translate, check_file_successfully_uploaded, initiate_transcribing, \
    get_transcription_status, get_transcription_url

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


class TranslateChinese(generics.GenericAPIView):
    """
    Author: Kenneth Y.
    Just wrapped for django
    """
    serializer_class = TranslateChineseSerializer
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


class GroupWordsView(generics.GenericAPIView):
    """
    Word Grouping Endpoint for Testing Purpose
    """
    serializer_class = WordGroupingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            start = timeit.default_timer()
            grouped_words = utils.word_grouping(data['text'])
            stop = timeit.default_timer()
            execution_time = stop - start
            print(execution_time)
            resp = {
                'result': grouped_words,
                'exec_time': execution_time
            }
            return Response(resp)
        return Response(serializer.errors)


class InitiateSTTView(generics.GenericAPIView):
    """
    Initiate Speech to Text Task
    """
    serializer_class = STTSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            data['speech_file_upload_url'] = upload_get_signed_up(data['filename'], 'ricciwawa_mp3')
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StartSTTView(generics.GenericAPIView):
    serializer_class = STTSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_data = request.data
        if 'filename' in request_data:
            del request_data['filename']
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            upload_status = check_file_successfully_uploaded(data['filename'], data['size'], 'ricciwawa_mp3')
            if not upload_status:
                return Response({'errors': 'File not uploaded successfully'}, status=status.HTTP_400_BAD_REQUEST)

            data = initiate_transcribing(data['filename'], data['language_code'], 'ricciwawa_mp3')
            return Response(data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetSTTResultView(generics.GenericAPIView):
    serializer_class = STTResultSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            transcription_status = get_transcription_status(data['transcription_id'])
            if transcription_status.lower() != 'succeeded':
                return Response({'status': transcription_status}, status=status.HTTP_206_PARTIAL_CONTENT)
            data = get_transcription_url(data['transcription_id'])
            data['status'] = transcription_status
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
