from django.urls import path

from . import views

app_name = 'system'

urlpatterns = [
    path('version-info/', views.VersionInfoView.as_view(), name='index'),
]
