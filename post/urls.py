from django.urls import path
from rest_framework import routers

from post.views import SubscriptionViewset

app_name = 'post'

router = routers.SimpleRouter()
router.register(r'subscription', SubscriptionViewset, basename='post')
urlpatterns = [
] + router.urls
