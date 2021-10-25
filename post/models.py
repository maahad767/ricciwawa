from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class Subscription(models.Model):
    """
    Model for Subscription Plans
    """
    STATE_CHOICES = ((0, 'closed'), (1, 'open'),)

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Playlist(models.Model):
    """
    Model for playlist
    """
    PRIVACY_CHOICES = [(0, 'private'), (1, 'public')]
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE,
                                     related_name='posts', null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True)
    privacy = models.SmallIntegerField(choices=PRIVACY_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    """
    Model for storing Post/Story contents.
    """
    PRIVACY_CHOICES = [(0, 'private'), (1, 'public')]
    ATTACHMENT_TYPE_CHOICES = [(0, 'none'), (1, 'image'), (2, 'audio'), (3, 'video')]

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=512)
    text = models.TextField(null=True)
    language = models.CharField(max_length=20, default='en')
    # store both spaced and not-spaced
    privacy = models.SmallIntegerField(choices=PRIVACY_CHOICES, default=1)
    attachment_type = models.SmallIntegerField(choices=ATTACHMENT_TYPE_CHOICES, default=0)
    attachment = models.FileField(null=True, blank=True)
    text_chinese = models.TextField(null=True, blank=True)
    text_simplified_chinese = models.JSONField(null=True, blank=True)
    text_traditional_chinese = models.JSONField(null=True, blank=True)
    audio_simplified_chinese = models.FilePathField(null=True, blank=True)
    timing_simplified_chinese = models.FilePathField(null=True, blank=True)
    audio_traditional_chinese = models.FilePathField(null=True, blank=True)
    timing_traditional_chinese = models.FilePathField(null=True, blank=True)
    # no idea about these fields
    pin_yin_words = models.JSONField(null=True, blank=True)
    meaning_words = models.JSONField(null=True, blank=True)
    english_meaning_article = models.JSONField(null=True, blank=True)
    story_difficulty = models.CharField(max_length=500, null=True, blank=True)
    story_tags = models.JSONField(null=True, blank=True)
    story_category = models.CharField(max_length=500, null=True, blank=True)
    story_source = models.CharField(max_length=500, null=True, blank=True)
    sim_spaced_datastore_text = models.TextField(null=True, blank=True)
    trad_spaced_datastore_text = models.TextField(null=True, blank=True)

    # line-6750, 6765-6767, there are a lot of string operations that
    # because text to speech in azure and google are different, they
    # expect different formats, which are similar but different
    # 6769, 6770: create mp3 for simplified chinese and traditional text_chinese
    # don't change
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # I'll create a utility function in a utils.py and call it from here
    # and will upload the created file to google cloud storage and
    # then will store the file location in a model field(will be created).

    @property
    def likes(self):
        return self.users_liked.count()


class Comment(models.Model):
    """
    Model for Comments
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
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
    liker = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class LikeComment(models.Model):
    """
    Model to track likes in a comment
    """
    liker = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class ViewPost(models.Model):
    """
    Model to track views in a post
    """
    viewer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Follow(models.Model):
    """
    Model for Follow a User
    """
    followed_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='following')
    followed_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='followers')


class Favourite(models.Model):
    """
    Model for making a Post favorite
    """
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='favorites')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorite_by')


class Subscribe(models.Model):
    """
    Model to track who subscribes which subscription plan
    """
    subscriber = models.ForeignKey(get_user_model(),  related_name='subscriptions', on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)


class SavePlaylist(models.Model):
    """
    Model to save playlist by a user
    """
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)


class FavouriteVocabulary(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    word = models.CharField(max_length=50)


class IgnorePost(models.Model):
    ignored_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ignored_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)


class ReportPost(models.Model):
    """
    Model for tracking and storing post reports.
    """
    STATUS = (
        (0, 'pending'),
        (1, 'reviewed'),
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reasoning = models.TextField(_('comments/reasoning'))
    comment = models.TextField(_('comment by reviewer'), null=True, blank=True)
    status = models.SmallIntegerField(choices=STATUS, default=0)
    attachment = models.FileField(upload_to='reports/', null=True, blank=True)

    def __str__(self):
        return f'{self.reported_by} reported {self.post.title[:50]}'


class Notification(models.Model):
    """
    Model to send notification and store them
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()
    attachment = models.FileField(null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
