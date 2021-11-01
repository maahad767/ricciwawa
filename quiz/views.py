from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Quiz
from .serializers import QuizSerializer, MultipleChoiceQuestionSerializer, ChoiceSerializer, \
    InputAnswerQuestionSerializer, AttemptQuizSerializer, AttemptInputAnswerQuestionSerializer, AttemptChoiceSerializer


class QuizViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(creator=self.request.user)


class MultipleChoiceQuestionViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MultipleChoiceQuestionSerializer

    def get_queryset(self):
        pass


class InputAnswerQuestionViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = InputAnswerQuestionSerializer

    def get_queryset(self):
        pass


class ChoiceViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        pass


class AttemptQuizViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AttemptQuizSerializer

    def get_queryset(self):
        pass


class AttemptInputAnswerQuestionViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AttemptInputAnswerQuestionSerializer

    def get_queryset(self):
        pass


class AttemptMultipleChoiceQuestionViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MultipleChoiceQuestionSerializer

    def get_queryset(self):
        pass


class AttemptChoiceViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AttemptChoiceSerializer

    def get_queryset(self):
        pass
