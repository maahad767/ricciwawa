from rest_framework import serializers

"""
This is the module that contains the Serializer Classes which are used for Serializing and Deserializing JSON
data, validate data using validators such as Data Type, Uniqueness, etc. If a Serializer class is a model Serializer
then it can also be used to create and update actions as well. The feature comes from Django Rest Framework.   
"""


class TextToSpeechSerializer(serializers.Serializer):
    pass


class SpeechToTextSerializer(serializers.Serializer):
    pass


class PronunciationAssessmentSerializer(serializers.Serializer):
    pass