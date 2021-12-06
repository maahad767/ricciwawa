from django.urls import path
from rest_framework import routers

from post.views import SubscriptionViewset, PlaylistViewset, PostViewset, CommentViewset, NewsfeedView, \
    FavouriteVocabularyViewset, LikePostView, UnlikePostView, ViewPostView, FollowView, AddFavouriteView, \
    RemoveFavouriteView, SavePlaylistView, UnsavePlaylistView, SubscribeView, UnfollowView, IgnorePostView, \
    UnignorePostView, UserPostListView, WebHome, GetContentsListView, CategoryViewset, UploadPostImageView, \
    AddPostsToSubscriptionsView, AddPostsToPlaylistView, AddPostsToCategoryView, GetCommentsByPostIDView, \
    GetCommentsByParentIDView, SharePostView, GetUserInfoView, GetSubscriptionsByUserView, GetPlaylistsByUserView, \
    NotificationViewset, CategoryListCreateView, SearchPostView, SubscribedPlansView, UnsubscribeView

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
router.register(r'notification', NotificationViewset, basename='notification')

urlpatterns = [
    path('', WebHome.as_view()),
    path('newsfeed-contents/', NewsfeedView.as_view()),
    path('contents/<str:content_type>/<int:id>/', GetContentsListView.as_view()),
    path('user-posts/<str:uid>', UserPostListView.as_view()),
    path('like-post/', LikePostView.as_view()),
    path('unlike-post/<int:post_id>/', UnlikePostView.as_view()),
    path('share-post/', SharePostView.as_view()),
    path('mark-post-viewd/', ViewPostView.as_view()),
    path('follow-user/', FollowView.as_view()),
    path('unfollow-user/<str:uid>/', UnfollowView.as_view()),
    path('add-to-favrourite-post/', AddFavouriteView.as_view()),
    path('remove-from-favrourite-post/<int:id>/', RemoveFavouriteView.as_view()),
    path('save-playlist/', SavePlaylistView.as_view()),
    path('unsave-playlist/<int:id>/', UnsavePlaylistView.as_view()),
    path('sibscribed_plans/', SubscribedPlansView.as_view()),
    path('subscribe-plan/', SubscribeView.as_view()),
    path('unsubscribe-plan/<int:subscription_id>/', UnsubscribeView.as_view()),
    path('ignore-post/', IgnorePostView.as_view()),
    path('unignore-post/<int:id>/', UnignorePostView.as_view()),

    # temporary url
    path('post/upload-image/<post_id>', UploadPostImageView.as_view()),

    # add posts to playlist, subscriptions, category etc
    path('add-posts-to-subscriptions/', AddPostsToSubscriptionsView.as_view()),
    path('add-posts-to-playlist/', AddPostsToPlaylistView.as_view()),
    path('add-posts-to-category/', AddPostsToCategoryView.as_view()),

    # get comments by post_id
    path('get-comments/post/<post_id>', GetCommentsByPostIDView.as_view()),
    path('get-comments/parent/<parent_id>/', GetCommentsByParentIDView.as_view()),

    # get user info
    path('get-user-info/', GetUserInfoView.as_view()),
    # get subscriptions by username
    # path('get-subscriptions/<str:username>', SubscriptionViewset.as_view({'get': 'get_subscriptions'})),
    path('get-subscriptions-by-user/<str:uid>/', GetSubscriptionsByUserView.as_view()),
    # get playlists by username
    path('get-playlists-by-user/<str:uid>/', GetPlaylistsByUserView.as_view()),
    # create multiple categories at once
    path('create-categories/', CategoryListCreateView.as_view()),
    path('search-post/<str:qs>/', SearchPostView.as_view()),
] + router.urls
