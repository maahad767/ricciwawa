from django.urls import path
from rest_framework import routers

from post.views import SubscriptionViewset, PlaylistViewset, PostViewset, CommentViewset, NewsfeedView, \
    FavouriteVocabularyViewset, LikePostView, UnlikePostView, ViewPostView, FollowView, AddFavouriteView, \
    RemoveFavouriteView, SavePlaylistView, UnsavePlaylistView, SubscribeView, UnfollowView, IgnorePostView, \
    UnignorePostView, UserPostListView, WebHome, GetContentsListView, CategoryViewset, UploadPostImageView, \
    AddPostsToSubscriptionsView, AddPostsToPlaylistView, AddPostsToCategoryView, GetCommentsByPostIDView, \
    GetCommentsByParentIDView

"""
Router is used to route ViewSets. 
path() is used to route Views.
"""


app_name = 'post'

router = routers.SimpleRouter()
router.register(r'subscriptions', SubscriptionViewset, basename='post')
router.register(r'playlists', PlaylistViewset, basename='post')
router.register(r'posts', PostViewset, basename='post')
router.register(r'comments', CommentViewset, basename='post')
router.register(r'fav-vocabs', FavouriteVocabularyViewset, basename='post')
router.register(r'category', CategoryViewset, basename='category')

urlpatterns = [
    path('', WebHome.as_view()),
    path('newsfeed-contents/', NewsfeedView.as_view()),
    path('contents/<str:content_type>/<int:id>/', GetContentsListView.as_view()),
    path('user-posts/<str:username>', UserPostListView.as_view()),
    path('like-post/', LikePostView.as_view()),
    path('unlike-post/<int:pk>/', UnlikePostView.as_view()),
    path('mark-post-viewd/', ViewPostView.as_view()),
    path('follow-user/', FollowView.as_view()),
    path('unfollow-user/<int:pk>/', UnfollowView.as_view()),
    path('add-to-favrourite-post/', AddFavouriteView.as_view()),
    path('remove-from-favrourite-post/<int:pk>/', RemoveFavouriteView.as_view()),
    path('save-playlist/', SavePlaylistView.as_view()),
    path('unsave-playlist/<int:pk>/', UnsavePlaylistView.as_view()),
    path('subscribe-plan/', SubscribeView.as_view()),
    path('unsubscribe-plan/<int:pk>/', SubscribeView.as_view()),
    path('ignore-post/<int:pk>/', IgnorePostView.as_view()),
    path('unignore-post/<int:pk>/', UnignorePostView.as_view()),

    # temporary url
    path('post/upload-image/<post_id>', UploadPostImageView.as_view()),

    # add posts to playlist, subscriptions, category etc
    path('add-posts-to-subscriptions/', AddPostsToSubscriptionsView.as_view()),
    path('add-posts-to-playlist/', AddPostsToPlaylistView.as_view()),
    path('add-posts-to-category/', AddPostsToCategoryView.as_view()),

    # get comments by post_id
    path('get-comments/post/<post_id>', GetCommentsByPostIDView.as_view()),
    path('get-comments/parent/<parent_id>/', GetCommentsByParentIDView.as_view())
 ] + router.urls
