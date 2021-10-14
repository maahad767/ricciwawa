from django.urls import path
from rest_framework import routers

from post.views import SubscriptionViewset, PlaylistViewset, PostViewset, CommentViewset

app_name = 'post'

router = routers.SimpleRouter()
router.register(r'subscription', SubscriptionViewset, basename='post')
router.register(r'playlist', PlaylistViewset, basename='post')
router.register(r'post', PostViewset, basename='post')
router.register(r'comment', CommentViewset, basename='post')

urlpatterns = [
] + router.urls
