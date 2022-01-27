from django.urls import path

from . import views

app_name = 'utils'

urlpatterns = [
    path('text-to-speech/', views.TextToSpeechView.as_view(), name='text_to_speech'),
    path('speech-to-text/', views.SpeechToTextView.as_view(), name='speech_to_text'),
    path('pronunciation-assessmet/', views.PronunciationAssessmentView.as_view(), name='pronunciation_assessment'),
    path('mp3-task-handler/', views.Mp3TaskHandler.as_view(), name='mp3_task_handler'),
    path('translate-chinese/', views.TranslateChinese.as_view(), name='translate_chinese'),
    path('translate-simplified-to-traditional/', views.TranslateSimplifiedToTraditional.as_view(),
         name='translate_simplified_to_traditional'),
    path('uid-to-idtoken/', views.UIDToIdTokenView.as_view(), name='uid_to_idtoken'),
    # temp file
    path('group-words/', views.GroupWordsView.as_view(), name='group_words'),
    path('stt-initiate/', views.InitiateSTTView.as_view(), name='initiate_stt'),
    path('stt-start/', views.StartSTTView.as_view(), name='start_stt'),
    path('stt-result/', views.GetSTTResultView.as_view(), name='stt_result'),
]
