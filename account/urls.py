from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('report-user/', views.ReportUserView.as_view(), name='report_user'),
    path('ignore-block-user/', views.IgnoreBlockUserCreateView.as_view(), name='ignore_block_user'),
    path('un-ignore-block-user/<int:id>/', views.IgnoreBlockUserDestroyView.as_view(), name='un_ignore_view'),
    path('ignore-blocked-user-list/',
         views.IgnoreBlockUserListView.as_view(), name='ignore_blocked_user_list'),
]
