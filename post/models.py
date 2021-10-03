from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    """
    Model for storing Post/Story contents.
    """
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=512)
    description = models.TextField()
    language = models.CharField(max_length=50)
    access_type = models.CharField(max_length=50)
    attachment = models.FileField()
    # text_chinese = ...
    # text_simplified_chinese = ...
    # text_traditional_chinese = ...
    view_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
