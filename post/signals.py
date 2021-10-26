from datetime import datetime
from hashlib import sha1

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post
from .utils import create_mp3_task
from utils.utils import get_random_string


@receiver(post_save, sender=Post)
def add_audio_in_post(instance, created, *args, **kwargs):
    """
    Integrated in Django,
    Created by Kenneth Y.
    """
    if not created:
        return
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    hashed_id = sha1(str.encode(get_random_string(10) + date_time)).hexdigest()
    str_hashed_id = str(hashed_id)
    storage_prefix = "media/temp/"

    if instance.text_simplified_chinese:
        sim_spaced_sentence = "\n".join(instance.text_simplified_chinese)
        instance.sim_spaced_datastore_text = ''.join([str(elem) for elem in sim_spaced_sentence])
        sim_spaced_sentence = sim_spaced_sentence.replace("<p>", "\n").replace("<BR>", "\n<BR>\n")
        instance.audio_simplified_chinese = storage_prefix + str_hashed_id + "_tw" + ".mp3"
        instance.timing_simplified_chinese = storage_prefix + str_hashed_id + "_tw" + "_timing.txt"
        create_mp3_task("tw", sim_spaced_sentence, instance.audio_simplified_chinese)
    if instance.text_traditional_chinese:
        trad_spaced_sentence = "\n".join(instance.text_traditional_chinese)
        instance.trad_spaced_datastore_text = ''.join([str(elem) for elem in trad_spaced_sentence])
        trad_spaced_sentence = trad_spaced_sentence.replace("<p>", "\n").replace("<BR>", "\n<BR>\n")
        instance.audio_traditional_chinese = storage_prefix + str_hashed_id + "_hk" + ".mp3"
        instance.timing_traditional_chinese = storage_prefix + str_hashed_id + "_hk" + "_timing.txt"
        create_mp3_task("hk", trad_spaced_sentence, instance.audio_traditional_chinese)

    instance.save()
