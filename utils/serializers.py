from rest_framework import serializers

from utils.utils import get_hashed_filename

"""
This is the module that contains the Serializer Classes which are used for Serializing and Deserializing JSON
data, validate data using validators such as Data Type, Uniqueness, etc. If a Serializer class is a model Serializer
then it can also be used to create and update actions as well. The feature comes from Django Rest Framework.   
"""


class TextToSpeechSerializer(serializers.Serializer):
    text = serializers.CharField(required=True)
    language_code = serializers.CharField(required=False)


class SpeechToTextSerializer(serializers.Serializer):
    speech_file = serializers.FileField(allow_empty_file=False, required=True)
    sample_rate = serializers.IntegerField(min_value=8000, max_value=48000, default=16000)
    audio_channel_count = serializers.IntegerField(min_value=1, max_value=8, default=1)
    language_code = serializers.CharField(max_length=255)


class PronunciationAssessmentSerializer(serializers.Serializer):
    reference_text = serializers.CharField(required=True)
    speech_file = serializers.FileField(allow_empty_file=False, required=True)
    language_code = serializers.CharField(required=False)

###################
# refactor needed #
###################
class Mp3TaskHandlerSerializer(serializers.Serializer):
    language_code = serializers.CharField(max_length=50)
    text = serializers.CharField(max_length=5000)
    output_filename = serializers.CharField(max_length=200)


class TranslateChineseSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=5000)


class TranslateSimplifiedToTraditionalSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=5000)

###################

class UIDToIdTokenSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=200)


class WordGroupingSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=5000)
    language_code = serializers.CharField(max_length=50, default='zh')


class STTSerializer(serializers.Serializer):
    language_code = serializers.CharField(max_length=50, default='zh-CN')
    filename = serializers.CharField(max_length=200, default=get_hashed_filename)
    size = serializers.IntegerField(min_value=0)
    duration = serializers.IntegerField(min_value=0)


class STTResultSerializer(serializers.Serializer):
    transcription_id = serializers.CharField(max_length=200)
