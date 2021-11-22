from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('report-user/', views.ReportUserView.as_view()),
    path('block-user/', views.BlockUserCreateView.as_view()),
    path('unblock-user/<str:username>/', views.BlockUserDestroyView.as_view()),
    path('blocked-user-list/', views.BlockUserListView.as_view()),
]
