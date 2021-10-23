from rest_framework import serializers

from .models import Quiz, MultipleChoiceQuestion, Choice


class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = '__all__'


class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MultipleChoiceQuestion
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = '__all__'
