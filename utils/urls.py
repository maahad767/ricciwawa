from django.urls import path

from . import views

app_name = 'utils'

urlpatterns = [
    path('text-to-speech/', views.TextToSpeechView.as_view(), name='text_to_speech'),
    path('speech-to-text/', views.SpeechToTextView.as_view(), name='speech_to_text'),
    path('pronunciation-assessmet/', views.PronunciationAssessmentView.as_view(), name='pronunciation_assessment'),
]
