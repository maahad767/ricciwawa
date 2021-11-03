from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Quiz, QuizAttempt, MultipleChoiceQuestionAttempt, MultipleChoiceQuestion, InputAnswerQuestion, \
    Choice, InputAnswerQuestionAttempt
from .serializers import QuizSerializer, MultipleChoiceQuestionSerializer, ChoiceSerializer, \
    InputAnswerQuestionSerializer, AttemptQuizSerializer, AttemptInputAnswerQuestionSerializer


class QuizViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(creator=self.request.user)


class MultipleChoiceQuestionViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MultipleChoiceQuestionSerializer

    def get_queryset(self):
        MultipleChoiceQuestion.objects.filter(creator=self.request.user)


class InputAnswerQuestionViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InputAnswerQuestionSerializer

    def get_queryset(self):
        return InputAnswerQuestion.objects.filter(creator=self.request.user)


class ChoiceViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        return Choice.objects.filter(creator=self.request.user)


class AttemptQuizViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AttemptQuizSerializer

    def get_queryset(self):
        return QuizAttempt.objects.filter(examinee=self.request.user)


class AttemptInputAnswerQuestionViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AttemptInputAnswerQuestionSerializer

    def get_queryset(self):
        return InputAnswerQuestionAttempt.objects.filter(examinee=self.request.user)


class AttemptMultipleChoiceQuestionViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MultipleChoiceQuestionSerializer

    def get_queryset(self):
        return MultipleChoiceQuestionAttempt.objects.filter(examinee=self.request.user)
