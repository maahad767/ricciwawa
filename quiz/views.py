from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Quiz
from .serializers import QuizSerializer, MultipleChoiceQuestionSerializer, ChoiceSerializer


class QuizViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.all()


class MultipleChoiceQuestionViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MultipleChoiceQuestionSerializer


class ChoiceViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChoiceSerializer
