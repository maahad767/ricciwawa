from email.policy import default
from operator import mod
from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class HashTag(models.Model):
    """
    HashTag Model
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """
    Model for Subscription Plans
    """
    STATE_CHOICES = ((0, 'closed'), (1, 'open'),)

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='subscription_thumbnails/', null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=1)
    hashtags = models.ManyToManyField(HashTag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user == self.owner

    class Meta:
        ordering = ['-created_at']


class Category(models.Model):
    """
    Model for Subscription Categories
    """
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to='category_thumbnails/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user == self.subscription.owner

    class Meta:
        ordering = ['-created_at']


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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True)
    privacy = models.SmallIntegerField(choices=PRIVACY_CHOICES, default=1)
    hashtags = models.ManyToManyField(HashTag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.owner

    class Meta:
        ordering = ['-created_at']


class Post(models.Model):
    """
    Model for storing Post/Story contents.
    privacy: 0-private, 1-public
    attachment_type: 0-none, 1-image, 2-audio, 3-video
    """
    PRIVACY_CHOICES = [(0, 'private'), (1, 'public')]
    ATTACHMENT_TYPE_CHOICES = [(0, 'none'), (1, 'image'), (2, 'audio'), (3, 'video')]
    VOICE_OVER_CHOICES = (
            (0, 'woman-woman'),
            (1, 'man-man'),
            (2, 'woman-child'),
            (3, 'custom-woman'),  # represents custom all
            (4, 'women-custom'),  # doesn't exist
            (5, 'custom-custom'),  # doesn't exist
        )

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.IntegerField(default=0)
    title = models.CharField(max_length=512)
    description = models.TextField(null=True, blank=True)
    text = models.TextField(null=True)
    image = models.ImageField(null=True, blank=True)
    language = models.CharField(max_length=20, default='en')
    privacy = models.SmallIntegerField(choices=PRIVACY_CHOICES, default=1)
    attachment_type = models.SmallIntegerField(choices=ATTACHMENT_TYPE_CHOICES, default=0)
    attachment = models.CharField(max_length=200, null=True, blank=True)
    text_chinese = models.TextField(null=True, blank=True)
    text_simplified_chinese = models.JSONField(null=True, blank=True)
    text_traditional_chinese = models.JSONField(null=True, blank=True)
    voice_over_type = models.PositiveSmallIntegerField(choices=VOICE_OVER_CHOICES, null=True, blank=True)
    generate_voiceovers = models.BooleanField(default=False)
    has_cantonese_audio = models.BooleanField(default=False)
    has_mandarin_audio = models.BooleanField(default=False)
    audio_simplified_chinese = models.CharField(max_length=1000, null=True, blank=True)
    timing_simplified_chinese = models.CharField(max_length=1000, null=True, blank=True)
    audio_traditional_chinese = models.CharField(max_length=1000, null=True, blank=True)
    timing_traditional_chinese = models.CharField(max_length=1000, null=True, blank=True)
    full_data = models.JSONField(null=True, blank=True)
    pin_yin_words = models.JSONField(null=True, blank=True)
    meaning_words = models.JSONField(null=True, blank=True)
    english_meaning_article = models.TextField(null=True, blank=True)
    korean_meaning_translation = models.TextField(null=True, blank=True)
    indonesian_meaning_translation = models.TextField(null=True, blank=True)
    tagalog_meaning_translation = models.TextField(null=True, blank=True)
    story_difficulty = models.CharField(max_length=500, null=True, blank=True)
    story_tags = models.JSONField(null=True, blank=True)
    story_category = models.CharField(max_length=500, null=True, blank=True)
    story_source = models.CharField(max_length=500, null=True, blank=True)
    sim_spaced_datastore_text = models.TextField(null=True, blank=True)
    trad_spaced_datastore_text = models.TextField(null=True, blank=True)
    filename = models.CharField(max_length=500, null=True, blank=True)
    hashtags = models.ManyToManyField(HashTag, blank=True)
    text_on_post = models.CharField(max_length=500, null=True, blank=True)
    text_position_x = models.IntegerField(null=True, blank=True)
    text_position_y = models.IntegerField(null=True, blank=True)
    sticker_url = models.URLField(null=True, blank=True)
    sticker_position_x = models.IntegerField(null=True, blank=True)
    sticker_position_y = models.IntegerField(null=True, blank=True)
    photo_ids = models.JSONField(null=True, blank=True)
    hsk_level = models.CharField(max_length=100, null=True, blank=True)

    # post creation and update datetime
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.owner

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    """
    Model for Comments
    """
    ATTACHMENT_TYPE_CHOICES = (
        (0, 'None'),
        (1, 'Image'),
        (2, 'Audio'),
        (3, 'Video'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(null=True, blank=True)
    attachment_type = models.SmallIntegerField(choices=ATTACHMENT_TYPE_CHOICES, default=0)
    attachment = models.FileField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.owner

    class Meta:
        ordering = ['-created_at']


class LikePost(models.Model):
    """
    Model to track likes in a post
    """
    liker = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.liker

    class Meta:
        unique_together = ('liker', 'post')


class LikeComment(models.Model):
    """
    Model to track likes in a comment
    """
    liker = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.liker

    class Meta:
        unique_together = ('liker', 'comment')


class ViewPost(models.Model):
    """
    Model to track views in a post
    """
    viewer = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('viewer', 'post')


class SharePost(models.Model):
    """
    Model to track shares in a post
    """
    sharer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Follow(models.Model):
    """
    Model for Follow a User
    """
    followed_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='followers')
    followed_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='following')

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.followed_by

    class Meta:
        unique_together = ('followed_user', 'followed_by')


class Favourite(models.Model):
    """
    Model for making a Post favorite
    """
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='favorites')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorite_by')

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.owner

    class Meta:
        unique_together = ('owner', 'post')


class Subscribe(models.Model):
    """
    Model to track who subscribes which subscription plan
    """
    subscriber = models.ForeignKey(get_user_model(),  related_name='subscriptions', on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.subscriber

    class Meta:
        unique_together = ('subscriber', 'subscription')


class SavePlaylist(models.Model):
    """
    Model to save playlist by a user
    """
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.owner

    class Meta:
        unique_together = ('owner', 'playlist')


class FavouriteVocabulary(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    word = models.CharField(max_length=2000)
    trad = models.CharField(max_length=2000)
    sim = models.CharField(max_length=2000)
    eng = models.CharField(max_length=2000)
    pinyin = models.CharField(max_length=2000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='vocabulary/', null=True, blank=True)
    is_liked = models.BooleanField(default=False)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user == self.user

    class Meta:
        unique_together = ('user', 'word')


class IgnorePost(models.Model):
    ignored_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    ignored_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.ignored_by

    class Meta:
        unique_together = ('ignored_post', 'ignored_by')


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

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.reported_by

    def __str__(self):
        return f'{self.reported_by} reported {self.post.title[:50]}'

    class Meta:
        unique_together = ('post', 'reported_by')


class Notification(models.Model):
    """
    Model to send notification and store them
    """
    TYPES = (
        (0, 'announcement'),
        (10, 'like'),
        (20, 'comment'),
        (30, 'follow'),
        (40, 'subscribe'),
    )
    to_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notifications_received')
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notifications_sent')
    content = models.TextField(null=True, blank=True)
    notification_type = models.PositiveSmallIntegerField(default=4, choices=TYPES)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    attachment = models.FileField(null=True, blank=True)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class LikeHashTag(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    hashtag = models.ForeignKey(HashTag, on_delete=models.CASCADE)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        if request.user.is_authenticated:
            return request.user == self.user
        return False

    class Meta:
        unique_together = ('user', 'hashtag')


class FollowHashTag(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    hashtag = models.ForeignKey(HashTag, on_delete=models.CASCADE)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        if request.user.is_authenticated:
            return request.user == self.user
        return False

    class Meta:
        unique_together = ('user', 'hashtag')
