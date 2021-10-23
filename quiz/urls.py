from rest_framework import routers
from rest_framework.routers import SimpleRouter

from quiz.views import QuizViewset, MultipleChoiceQuestionViewset, ChoiceViewset

router = SimpleRouter()

router.register(r'quiz', QuizViewset, basename='quiz')
router.register(r'question/multiple-choice', MultipleChoiceQuestionViewset, basename='quiz')
router.register(r'choice', ChoiceViewset, basename='quiz')

urlpatterns = [
] + router.urls
