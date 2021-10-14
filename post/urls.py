from django.urls import path
from rest_framework import routers

from post.views import SubscriptionViewset, PlaylistViewset, PostViewset, CommentViewset, NewsfeedView, \
    FavouriteVocabularyViewset, LikePostView

"""
Router is used to route ViewSets. 
path() is used to route Views.
"""


app_name = 'post'

router = routers.SimpleRouter()
router.register(r'subscription', SubscriptionViewset, basename='post')
router.register(r'playlist', PlaylistViewset, basename='post')
router.register(r'post', PostViewset, basename='post')
router.register(r'comment', CommentViewset, basename='post')
router.register(r'fav-vocab', FavouriteVocabularyViewset, basename='post')

urlpatterns = [
    path('get-newsfeed-contents', NewsfeedView.as_view()),
    path('like-post/<int:id>', LikePostView.as_view()),


] + router.urls
