from abc import ABC

from rest_framework import serializers

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
    language_code = serializers.CharField()


class PronunciationAssessmentSerializer(serializers.Serializer):
    reference_text = serializers.CharField(required=True)
    speech_file = serializers.FileField(allow_empty_file=False, required=True)
    language_code = serializers.CharField(required=False)
