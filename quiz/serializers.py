from rest_framework import serializers

from .models import Quiz, MultipleChoiceQuestion, Choice, InputAnswerQuestion, AttemptQuiz, \
    AttemptMultipleChoiceQuestion, AttemptInputAnswerQuestion, AttemptChoice


class QuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = '__all__'


class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MultipleChoiceQuestion
        fields = '__all__'


class InputAnswerQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = InputAnswerQuestion
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = '__all__'


class AttemptQuizSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttemptQuiz
        fields = '__all__'


class AttemptMultipleChoiceQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttemptMultipleChoiceQuestion
        fields = '__all__'


class AttemptInputAnswerQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttemptInputAnswerQuestion
        fields = '__all__'


class AttemptChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = AttemptChoice
        fields = '__all__'
