from datetime import datetime
from hashlib import sha1

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, LikePost, Notification, Comment, Subscribe, Follow, Playlist
from .utils import create_mp3_task, create_save_edit_fulldata
from utils.utils import get_random_string, google_translate


@receiver(post_save, sender=Post)
def add_audio_in_post(instance, created, *args, **kwargs):
    """
    Integrated in Django,
    Created by Kenneth Y.
    Instance is an object of a model class.
    Will be transferred to Google task for MP3 creation.
    """
    if not created:
        return
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    hashed_id = sha1(str.encode(get_random_string(10) + date_time)).hexdigest()
    str_hashed_id = str(hashed_id)
    storage_prefix = ""

    if instance.attachment:
        ext = instance.attachment.split('.')[-1]
        instance.attachment = "attachment_" + str_hashed_id + "." + ext  # change file name

    if instance.text_simplified_chinese:
        sim_spaced_sentence = "\n".join(instance.text_simplified_chinese)
        instance.sim_spaced_datastore_text = ''.join([str(elem) for elem in sim_spaced_sentence])
        sim_spaced_sentence = sim_spaced_sentence.replace("<p>", "\n").replace("<BR>", "\n<BR>\n")
        instance.audio_simplified_chinese = storage_prefix + str_hashed_id + "_tw" + ".mp3"
        instance.timing_simplified_chinese = storage_prefix + str_hashed_id + "_tw" + "_timing.txt"
        # print(sim_spaced_sentence)
        create_mp3_task("tw", sim_spaced_sentence, instance.audio_simplified_chinese)
    if instance.text_traditional_chinese:
        trad_spaced_sentence = "\n".join(instance.text_traditional_chinese)
        instance.trad_spaced_datastore_text = ''.join([str(elem) for elem in trad_spaced_sentence])
        trad_spaced_sentence = trad_spaced_sentence.replace("<p>", "\n").replace("<BR>", "\n<BR>\n")
        instance.audio_traditional_chinese = storage_prefix + str_hashed_id + "_hk" + ".mp3"
        instance.timing_traditional_chinese = storage_prefix + str_hashed_id + "_hk" + "_timing.txt"
        # print(trad_spaced_sentence)

        create_mp3_task("hk", trad_spaced_sentence, instance.audio_traditional_chinese)

    if instance.text_traditional_chinese and instance.text_simplified_chinese and instance.meaning_words and instance.pin_yin_words:
        instance.full_data = create_save_edit_fulldata(instance.text_traditional_chinese,
                                                       instance.text_simplified_chinese,
                                                       instance.meaning_words,
                                                       instance.pin_yin_words)

    if instance.english_meaning_article:
        instance.korean_meaning_translation = google_translate(
            instance.english_meaning_article, "zh", "ko")
        instance.indonesian_meaning_translation = google_translate(
            instance.english_meaning_article, "zh", "id")
        instance.tagalog_meaning_translation = google_translate(
            instance.english_meaning_article, "zh", "tl")

    instance.save()


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

    follows_count = instance.followed_user.follow_set.count()

    if follows_count == 1:
        content = f'@{followed_by.username} followed you.'
    else:
        content = f'@{followed_by.username} and {follows_count - 1} others followed you.'

    Notification.objects.create(
        notification_type=notification_type,
        to_user=to_user,
        content=content,
        object_id=instance.followed_user.id)
