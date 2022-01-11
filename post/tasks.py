from celery import shared_task

from post.models import Post
from utils.models import Word
from utils.utils import speech_tts_msft, google_translate


@shared_task
def create_mp3_task(language_code, text, output_filename):
    speech_tts_msft(language_code, text, output_filename)
    return f'mp3 file is created for {output_filename}'


@shared_task
def add_full_data_translations(instance_id):
    instance = Post.objects.get(id=instance_id)
    trad_words = instance.text_traditional_chinese
    pinyin_words = instance.pin_yin_words
    sim_words = instance.text_simplified_chinese
    eng_words = instance.meaning_words

    full_data = list(Word.objects.filter(trad__in=trad_words).values())

    for word in full_data:
        word['word'] = word['trad']
        word['korean'] = word['ko']
        word['indonesian'] = word['ind']
        word['tagalog'] = word['tl']

    new_full_data = []
    for tw, pw, sw, ew in zip(trad_words, pinyin_words, sim_words, eng_words):
        word = None
        for w in full_data:
            if w['trad'] == tw:
                word = w
                break

        if word is None:
            word = {'trad': tw}

        word['pinyin'] = pw
        word['sim'] = sw
        word['eng'] = ew
        new_full_data.append(word)
    instance.full_data = new_full_data

    english_article = instance.english_meaning_article
    if english_article:
        instance.korean_meaning_translation = google_translate(english_article, "en", "ko")
        instance.indonesian_meaning_translation = google_translate(english_article, "en", "id")
        instance.tagalog_meaning_translation = google_translate(english_article, "en", "tl")
    instance.save()

    return f'full data and translation is created for {instance.id}'
