from rest_framework import serializers

from .models import Quiz, MultipleChoiceQuestion, Choice, InputAnswerQuestion, QuizAttempt, \
    MultipleChoiceQuestionAttempt, InputAnswerQuestionAttempt, ChoiceAttempt


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
        model = QuizAttempt
        fields = '__all__'


class AttemptMultipleChoiceQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MultipleChoiceQuestionAttempt
        fields = '__all__'


class AttemptInputAnswerQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = InputAnswerQuestionAttempt
        fields = '__all__'


class AttemptChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChoiceAttempt
        fields = '__all__'


class FullQuizSerializer(serializers.ModelSerializer):
    questions = serializers.StringRelatedField(many=True)

    class Meta:
        model = Quiz
        fields = '__all__'
