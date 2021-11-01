from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import Quiz, MultipleChoiceQuestion, Choice, InputAnswerQuestion, QuizAttempt, \
    MultipleChoiceQuestionAttempt, InputAnswerQuestionAttempt, ChoiceAttempt


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        exclude = []
        read_only_fields = ['question']


class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = MultipleChoiceQuestion
        exclude = []
        read_only_fields = ['quiz']


class InputAnswerQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = InputAnswerQuestion
        exclude = []
        read_only_fields = ['quiz']


class QuizSerializer(WritableNestedModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    mc_questions = MultipleChoiceQuestionSerializer(source='quiz_multiplechoicequestion_related',
                                                    default=None, many=True)
    ia_questions = InputAnswerQuestionSerializer(source='quiz_inputanswerquestion_related',
                                                 default=None, many=True)

    def create(self, validated_data):
        mc_questions = validated_data.pop('quiz_multiplechoicequestion_related')
        ia_questions = validated_data.pop('quiz_inputanswerquestion_related')
        quiz = Quiz.objects.create(**validated_data)

        for question in mc_questions:
            choices = question.pop('choices')
            question_instance = MultipleChoiceQuestion.objects.create(quiz=quiz, **question)
            choice_instances = [Choice(question=question_instance, **item) for item in choices]
            Choice.objects.bulk_create(choice_instances)

        ia_question_instance = [InputAnswerQuestion(quiz=quiz, **item) for item in ia_questions]
        InputAnswerQuestion.objects.bulk_create(ia_question_instance)
        return quiz

    class Meta:
        model = Quiz
        exclude = []


class AttemptChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChoiceAttempt
        fields = '__all__'


class AttemptMultipleChoiceQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MultipleChoiceQuestionAttempt
        fields = '__all__'


class AttemptInputAnswerQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = InputAnswerQuestionAttempt
        fields = '__all__'


class AttemptQuizSerializer(serializers.ModelSerializer):
    mcq_attempts = MultipleChoiceQuestionSerializer(source='quiz_multiplechoicequestion_related',
                                                    default=None, many=True)
    iaq_attempts = InputAnswerQuestionSerializer(source='quiz_inputanswerquestion_related',
                                                 default=None, many=True)

    class Meta:
        model = QuizAttempt
        fields = '__all__'
