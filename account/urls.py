from django.urls import path

from . import views
from .views import UpdateProfileView, CheckUsernameView, SearchUserView

app_name = 'account'

urlpatterns = [
    path('check-username/', CheckUsernameView.as_view()),
    path('search-user/<str:qs>/', SearchUserView.as_view()),
    path('update-profile/', UpdateProfileView.as_view()),
    path('report-user/', views.ReportUserView.as_view()),
    path('block-user/', views.BlockUserCreateView.as_view()),
    path('unblock-user/<str:uid>/', views.BlockUserDestroyView.as_view()),
    path('blocked-user-list/', views.BlockUserListView.as_view()),
]
