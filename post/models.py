from django.db import models
from django.contrib.auth import get_user_model


class Subscription(models.Model):
    """
    Model for Subscription Plans
    """
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    duration_type = models.CharField(max_length=20)  # choice field: monthly/yearly
    privacy = models.CharField(max_length=50)  # choice public/private
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Playlist(models.Model):
    """
    Model for playlist
    """
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE,
                                     related_name='posts', null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True)
    privacy = models.CharField(max_length=50)  # choice public/private
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    """
    Model for storing Post/Story contents.
    """
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="posts")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE,
                                     related_name='posts', null=True, blank=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE,
                                 related_name='posts', null=True, blank=True)
    title = models.CharField(max_length=512)  # post's title
    text = models.TextField(null=True)  # post description
    language = models.CharField(max_length=50)  # post's language in code format
    privacy = models.CharField(max_length=50)  # choice public/private
    attachment_type = models.CharField(max_length=50)  # choice field
    attachment = models.FileField(null=True, blank=True)  # image/video/audio attachment with the post
    text_chinese = models.TextField(null=True, blank=True)  # chinese text
    text_simplified_chinese = models.TextField(null=True, blank=True)  # chinese text simplified version
    text_traditional_chinese = models.TextField(null=True)  # chinese traditional version
    created_at = models.DateTimeField(auto_now_add=True)  # creation time
    updated_at = models.DateTimeField(auto_now=True)  # update time


class Comment(models.Model):
    """
    Model for Comments
    """
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(null=True, blank=True)
    attachment = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LikePost(models.Model):
    """
    Model to track likes in a post
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='liked_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='users_liked')


class LikeComment(models.Model):
    """
    Model to track likes in a comment
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='liked_comments')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class View(models.Model):
    """
    Model to track views in a post
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='viewed_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='users_viewed')


class Follow(models.Model):
    """
    Model for Follow a User
    """
    follower = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='following')
    followed_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='followers')


class Favourite(models.Model):
    """
    Model for making a Post favorite
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='favorites')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorite_by')


class Subscribe(models.Model):
    """
    Model to track who subscribes which subscription plan
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)


class SavePlaylist(models.Model):
    """
    Model to save playlist by a user
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)


class Notification(models.Model):
    """
    Model to send notification and store them
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    attachment = models.FileField(null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
