from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('report-user/', views.ReportUserView.as_view()),
    path('ignore-block-user/', views.BlockUserCreateView.as_view()),
    path('un-ignore-block-user/<str:username>/', views.BlockUserDestroyView.as_view()),
    path('ignore-blocked-user-list/', views.BlockUserListView.as_view()),
]
