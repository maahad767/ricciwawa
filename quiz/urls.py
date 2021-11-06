from django.urls import path
from rest_framework.routers import SimpleRouter

from quiz.views import QuizViewset, MultipleChoiceQuestionViewset, ChoiceViewset, \
    AttemptMultipleChoiceQuestionViewset, AttemptQuizViewset, AttemptInputAnswerQuestionViewset, QuizExamineeView

app_name = 'quiz'

router = SimpleRouter()

router.register(r'quiz', QuizViewset, basename='quiz')
# router.register(r'mcq', MultipleChoiceQuestionViewset, basename='question')
# router.register(r'choice', ChoiceViewset, basename='quiz')
router.register(r'attempt', AttemptQuizViewset, basename='attempt_quiz')
# router.register(r'attempt-mcq', AttemptMultipleChoiceQuestionViewset, basename='attempt/mcq/')
# router.register(r'attempt-iaq', AttemptInputAnswerQuestionViewset, basename='attempt/iaq/')

urlpatterns = [
    path('post/<int:post_id>/', QuizExamineeView.as_view())
] + router.urls
