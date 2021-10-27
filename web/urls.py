from django.urls import path

from . import views

app_name = 'web'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('resources/', views.Resources.as_view(), name='resources'),
    path('blog/', views.Blog.as_view(), name='blog'),
    path('blog/<str:blog_number>', views.BlogSingle.as_view(), name='blog_single'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('edit-content/', views.EditContent.as_view(), name='edit_content'),
    path('qna/', views.QuestionAnswer.as_view(), name='qna'),
    path('subscription/', views.Subscription.as_view(), name='subscription'),
    path('terms-of-service', views.TermsOfService.as_view(), name='terms_of_service'),
    path('privacy-policy/', views.PrivacyPolicy.as_view(), name='privacy_policy'),
]
