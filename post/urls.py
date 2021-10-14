from django.urls import path
from rest_framework import routers

from post.views import SubscriptionViewset, PlaylistViewset, PostViewset, CommentViewset, NewsfeedView, \
    FavouriteVocabularyViewset, LikePostView, UnlikePostView, ViewPostView, FollowView, AddFavouriteView, \
    RemoveFavouriteView, SavePlaylistView, UnsavePlaylistView, SubscribeView, UnfollowView

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
    path('get-newsfeed-contents/', NewsfeedView.as_view()),
    path('like-post/', LikePostView.as_view()),
    path('unlike-post/', UnlikePostView.as_view()),
    path('mark-post-viewd/', ViewPostView.as_view()),
    path('follow-user/', FollowView.as_view()),
    path('unfollow-user/', UnfollowView.as_view()),
    path('add-to-favrourite-post/', AddFavouriteView.as_view()),
    path('remove-from-favrourite-post/', RemoveFavouriteView.as_view()),
    path('save-playlist/', SavePlaylistView.as_view()),
    path('unsave-playlist/', UnsavePlaylistView.as_view()),
    path('subscribe-plan/', SubscribeView.as_view()),
    path('unsubscribe-plan/', SubscribeView.as_view()),
] + router.urls
