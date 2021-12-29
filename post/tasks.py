from celery import shared_task

from post.models import Post
from utils.utils import speech_tts_msft, google_translate


@shared_task
def create_mp3_task(language_code, text, output_filename):
    speech_tts_msft(language_code, text, output_filename)
    return f'mp3 file is created for {output_filename}'


@shared_task
def add_full_data(instance_id, trad_words, sim_words, eng_words, pinyin_words):
    instance = Post.objects.get(id=instance_id)
    full_data = []
    for tw, sw, ew, pw in zip(trad_words, sim_words, eng_words, pinyin_words):
        translated_word = {'word': tw, 'eng': [ew], 'sim': [sw], 'pinyin': [pw], 'trad': [tw],
                           "tagalog": google_translate(tw, "zh-TW", "tl"),
                           "indonesian": google_translate(tw, "zh-TW", "id"),
                           "korean": google_translate(tw, "zh-TW", "ko")}

        full_data.append(translated_word)
    instance.full_data = full_data
    instance.update(fulldata=full_data)
    return f'full data is created for {instance.id}'


@shared_task
def add_full_translations(instance_id, english_article):
    instance = Post.objects.get(id=instance_id)
    korean_meaning_translation = google_translate(
        english_article, "en", "ko")
    indonesian_meaning_translation = google_translate(
        english_article, "en", "id")
    tagalog_meaning_translation = google_translate(
        english_article, "en", "tl")
    instance.update(korean_meaning_translation=korean_meaning_translation,
                    indonesian_meaning_translation=indonesian_meaning_translation,
                    tagalog_meaning_translation=tagalog_meaning_translation)

    return f'full translations are created for {instance.id}'
