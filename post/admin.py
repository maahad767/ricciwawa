from django.contrib import admin

from .models import (Post, Comment, Subscription, Playlist, LikeComment, LikePost, SavePlaylist, ViewPost,
                     Favourite, Follow, Subscribe)


"""
The following classes registers a model in the admin panel.
However, it can be replaced with admin.site.register(ModelName)
But the style I've followed will provides easy to modify the admin site.
"""


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentSerializer(admin.ModelAdmin):
    pass


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    pass


@admin.register(SavePlaylist)
class SavePlaylistAdmin(admin.ModelAdmin):
    pass


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    pass


@admin.register(ViewPost)
class ViewPostAdmin(admin.ModelAdmin):
    pass


@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):
    pass


@admin.register(LikeComment)
class LikeCommentAdmin(admin.ModelAdmin):
    pass
