from datetime import datetime
from fileinput import filename
from hashlib import sha1

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Post, LikePost, Notification, Comment, Subscribe, Follow
from .tasks import create_mp3_task, add_full_data_translations
from utils.utils import get_hashed_filename, get_random_string

@receiver(pre_save, sender=Post)
def add_audio_filenames(instance, *args, **kwargs):
    if instance.filename:
        return
    filename = get_hashed_filename(ext="")
    prefix_cant = "cantonese_"
    prefix_mand = "mandarin_"
    ext_audio = ".mp3"
    ext_timing = "_timing.txt"
    instance.filename = filename
    instance.audio_simplified_chinese = prefix_cant + filename + ext_audio
    instance.timing_simplified_chinese =  prefix_cant + filename + ext_timing
    instance.audio_traditional_chinese = prefix_mand + filename + ext_audio
    instance.timing_traditional_chinese = prefix_mand + filename + ext_timing
    if instance.attachment:
        ext = instance.attachment.split('.')[-1]
        instance.attachment = "attachment_" + filename + "." + ext 

@receiver(post_save, sender=Post)
def add_audio_in_post(instance, created, *args, **kwargs):
    """
    Instance is an object of a model class.
    Will be transferred to Google task for MP3 creation.
    VOICE_OVER_CHOICES = (
            (0, 'woman-woman'),
            (1, 'man-man'),
            (2, 'woman-child'),
            (3, 'custom-woman'),
            (4, 'women-custom'),
            (5, 'custom-custom'),
        )
    """
    votype = instance.voice_over_type
    voiceover_type = (
        ('cantonese_normal', 'mandarin_normal'),
        ('cantonese_normal_male', 'mandarin_normal_male'),
        ('cantonese_normal', 'mandarin_child_normal'),
        (None, 'mandarin_normal'),
        ('cantonese_normal', None),
        (None, None),
    )
    if instance.generate_voiceovers:
        cant_votype = voiceover_type[votype][0]
        mand_votype = voiceover_type[votype][1]
        if instance.text_simplified_chinese and cant_votype:
            sim_spaced_sentence = "\n".join(instance.text_simplified_chinese)
            instance.sim_spaced_datastore_text = ''.join([str(elem) for elem in sim_spaced_sentence])
            sim_spaced_sentence = sim_spaced_sentence.replace("<p>", "\n").replace("<BR>", "\n<BR>\n")
            create_mp3_task(language_code="tw", speaker=cant_votype, text=sim_spaced_sentence, output_filename=instance.audio_simplified_chinese).delay()
            
        if instance.text_traditional_chinese and mand_votype:
            trad_spaced_sentence = "\n".join(instance.text_traditional_chinese)
            instance.trad_spaced_datastore_text = ''.join([str(elem) for elem in trad_spaced_sentence])
            trad_spaced_sentence = trad_spaced_sentence.replace("<p>", "\n").replace("<BR>", "\n<BR>\n")
            create_mp3_task(language_code="hk", speaker=mand_votype, text=trad_spaced_sentence, output_filename=instance.audio_traditional_chinese).delay()
        instance.generate_voiceovers = False
        instance.save()

    if not created:
        return

    if instance.text_traditional_chinese and instance.text_simplified_chinese and instance.meaning_words and instance.pin_yin_words:
        add_full_data_translations(instance_id=instance.id).delay()


"""
TYPES = (
    (0, 'announcement'),
    (10, 'like'),
    (20, 'comment'),
    (30, 'follow'),
    (40, 'subscribe'),
)
"""


# Create Notifications
@receiver(post_save, sender=LikePost)
def create_like_notification(instance, created, *args, **kwargs):
    if not created:
        return

    # notification_type: 10 for like
    notification_type = 10
    to_user = instance.post.owner
    liked_by = instance.liker

    if to_user == liked_by:
        return

    likes_count = instance.post.likepost_set.count()
    if likes_count == 1:
        content = f'@{liked_by.username} liked your post.'
    else:
        content = f'@{liked_by.username} and {likes_count - 1} others liked your post.'

    notification, created = Notification.objects.get_or_create(
        notification_type=notification_type,
        to_user=to_user,
        from_user=liked_by,
        object_id=instance.post.id)
    notification.content = content
    notification.save()


@receiver(post_save, sender=Comment)
def create_comment_notification(instance, created, *args, **kwargs):
    if not created:
        return

    notification_type = 20  # 20 for comment
    to_user = instance.post.owner
    commented_by = instance.owner

    if to_user == commented_by:
        return

    comments_count = instance.post.comments.count()

    if comments_count == 1:
        content = f'@{commented_by.username} commented on your post.'
    else:
        content = f'@{commented_by.username} and {comments_count - 1} others liked your post.'

    Notification.objects.create(
        notification_type=notification_type,
        to_user=to_user,
        from_user=commented_by,
        content=content,
        object_id=instance.post.id)


@receiver(post_save, sender=Subscribe)
def create_subscribe_notification(instance, created, *args, **kwargs):
    if not created:
        return

    notification_type = 40  # 40 for subscribe
    to_user = instance.subscription.owner
    subscribed_by = instance.subscriber

    if to_user == subscribed_by:
        return

    subscriptions_count = instance.subscription.subscribe_set.count()

    if subscriptions_count == 1:
        content = f'@{subscribed_by.username} subscribed to your subscription plan.'
    else:
        content = f'@{subscribed_by.username} and {subscriptions_count - 1} others subscribed' \
                  f' to your subscription plan.'

    Notification.objects.create(
        notification_type=notification_type,
        to_user=to_user,
        from_user=subscribed_by,
        content=content,
        object_id=instance.subscription.id)


@receiver(post_save, sender=Follow)
def create_follow_notification(instance, created, *args, **kwargs):
    if not created:
        return

    notification_type = 30  # 20 for follow
    to_user = instance.followed_user
    followed_by = instance.followed_by

    if to_user == followed_by:
        return

    follows_count = instance.followed_user.followers.count()

    if follows_count == 1:
        content = f'@{followed_by.username} followed you.'
    else:
        content = f'@{followed_by.username} and {follows_count - 1} others followed you.'

    Notification.objects.create(
        notification_type=notification_type,
        to_user=to_user,
        from_user=followed_by,
        content=content,
        object_id=instance.followed_user.id)
