from celery import shared_task

from post.models import Post
from utils.models import Word
from utils.utils import speech_tts_msft, google_translate, translate_word


@shared_task
def create_mp3_task(language_code, text, output_filename):
    speech_tts_msft(language_code, text, output_filename)
    return f'mp3 file is created for {output_filename}'


@shared_task
def add_full_data_translations(instance_id, trad_words, sim_words, eng_words, pinyin_words):
    instance = Post.objects.get(id=instance_id)
    full_data = []
    # for tw, sw, ew, pw in zip(trad_words, sim_words, eng_words, pinyin_words):
    #     translated_word = {'word': tw, 'eng': [ew], 'sim': [sw], 'pinyin': [pw], 'trad': [tw],
    #                        }
    #     translated_word.update(translate_word(tw))
    #     full_data.append(translated_word)

    full_data = Word.objects.filter(trad__in=trad_words).values()

    for word in full_data:
        word['korean'] = word['ko']
        word['indonesian'] = word['ind']

    instance.full_data = list(full_data)
    english_article = instance.english_meaning_article
    if english_article:
        instance.korean_meaning_translation = google_translate(english_article, "en", "ko")
        instance.indonesian_meaning_translation = google_translate(english_article, "en", "id")
        instance.tagalog_meaning_translation = google_translate(english_article, "en", "tl")
    instance.save()

    return f'full data and translation is created for {instance.id}'
