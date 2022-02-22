import datetime
import json
import logging
import os
import random
import re
import string
import timeit
from hashlib import sha1

import firebase_admin
import requests
import time
import base64

from firebase_admin import credentials, auth
from google.cloud import texttospeech, speech, storage, datastore, translate, language

from utils.data.cedict import cedict_phrase
import azure.cognitiveservices.speech as speechsdk

from utils.models import Word

datastore_client = datastore.Client()


# cred = credentials.Certificate(os.environ.get('SERVICE_ACCOUNT_KEY', 'ricciwawa-6e11b342c999.json'))
# default_app = firebase_admin.initialize_app(cred)

def upload_get_signed_up(filename, bucket_name="ricciwawa"):
    """
    generate a signed upload url

    Reference:
        https://stackoverflow.com/questions/30843450/how-to-create-google-cloud-storage-signed-urls-on-app-engine-python

    Args:
        :param filename: filename to store in google storage
        :param bucket_name: you can change the bucket name if you need

    Returns:
        (str): returns signed url
    """
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    blob_name = filename

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=60),
        method="PUT",
        content_type="application/octet-stream",
    )
    # print(
    #     "curl -X PUT -H 'Content-Type: application/octet-stream' "
    #     "--upload-file mhb.py '{}'".format(url)
    # )
    return url


def download_get_signed_up(filename, bucket_name="ricciwawa"):
    """
    Generates Signed Download URL
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)

    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=60),
        method="GET",
    )

    # print("curl '{}'".format(url))
    return url


def text_to_speech(text, language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL):
    """
    Takes a text and converts to speech using google cloud text to speech service.

    :param text: Text to convert to
    :param language_code: The language of your text in code, for example, "en-US"
    :param ssml_gender: gender of the output speech. default is NEUTRAL.
    :return: audio/speech of the provided text in wave(.wav) format.
    """
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams({
        'language_code': language_code,
        'ssml_gender': ssml_gender
    })
    audio_config = texttospeech.AudioConfig({
        'audio_encoding': texttospeech.AudioEncoding.MP3
    })
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content


def speech_to_text(speech_file, sample_rate, audio_channel_count, language_code):
    """
    Converts a speech to text using google cloud speech to text api.
    
    :param audio_channel_count: The number of channels in the input audio data. ONLY set
            this for MULTI-CHANNEL recognition. Valid values for
            LINEAR16 and FLAC are ``1``-``8``. Valid values for OGG_OPUS
            are '1'-'254'. Valid value for MULAW, AMR, AMR_WB and
            SPEEX_WITH_HEADER_BYTE is only ``1``. If ``0`` or omitted,
            defaults to one channel (mono). Note: We only recognize the
            first channel by default. To perform independent recognition
            on each channel set
            ``enable_separate_recognition_per_channel`` to 'true'.
    :param sample_rate: sample rate of the audio file
    :param speech_file: the speech's audio file in .wav format
    :param language_code: the language of the speech
    :return: transcript of the speech as a dictionary
    """
    # print("UPLOADING AUDIO FILE")
    # bucket_name = "ricciwawa_mp3"
    # storage_client = storage.Client()
    # bucket = storage_client.get_bucket(bucket_name)
    # blob = bucket.blob(speech_file.name)
    # blob.upload_from_string(speech_file.file.read())
    #
    # client = speech.SpeechClient()
    # gcs_uri = 'gs://' + bucket_name + '/' + speech_file.name
    # audio = speech.RecognitionAudio(uri=gcs_uri)
    # config = speech.RecognitionConfig({
    #     'encoding': speech.RecognitionConfig.AudioEncoding.LINEAR16,
    #     'sample_rate_hertz': int(sample_rate),
    #     'audio_channel_count': int(audio_channel_count),
    #     'language_code': language_code,
    # })
    # operation = client.long_running_recognize(config=config, audio=audio)
    #
    # print("Waiting for operation to complete...")
    # response = operation.result(timeout=1000)
    # transcript = str()
    # for result in response.results:
    #     transcript += result.alternatives[0].transcript
    #     print("Transcript: {}".format(result.alternatives[0].transcript))
    #
    # blob.delete()
    # return {'transcript': transcript}

    subscription_key = "aea95857cbf14d41b132fefe96a3052e"  # transfer this to settings.py
    region = "eastasia"  # transfer this to settings.py
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.speech_recognition_language = "zh-CN"
    tmp_filename = random.choice(string.ascii_letters) + str(time.time()) + '.wav'
    done = False

    transcript = str()

    def recognizing(evt):
        nonlocal transcript
        print('RECOGNIZED: {}'.format(evt.result.text))
        transcript += evt.result.text

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    storage_path = "/tmp/"
    with open(storage_path + tmp_filename, "wb") as f:
        f.write(speech_file.file.read())
    audio_input = speechsdk.AudioConfig(filename=tmp_filename)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)
    speech_recognizer.recognizing.connect(lambda evt: None)

    speech_recognizer.recognized.connect(recognizing)
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)

    # os.remove(tmp_filename)
    # return {'transcript': result.text}
    return {'transcript': transcript}


def pronunciation_assessment(speech_file, reference_text, language_code='en-us'):
    """
    Pronunciation assessment using azure pronunciation assessment api.

    :param speech_file: audio of the speech in .wav format with 16k bit rate.
    :param reference_text: the transcript of the speech
    :param language_code: language of the speech.
    :return: returns a dictionary containing information about recognition status and scores like accuracy, fluency, etc
    """
    subscription_key = "aea95857cbf14d41b132fefe96a3052e"  # transfer this to settings.py
    region = "eastasia"  # transfer this to settings.py
    wave_header16_k16_bit_mono = bytes(
        [82, 73, 70, 70, 78, 128, 0, 0, 87, 65, 86, 69, 102, 109, 116, 32, 18, 0, 0, 0, 1, 0, 1, 0, 128, 62, 0, 0, 0,
         125, 0, 0, 2, 0, 16, 0, 0, 0, 100, 97, 116, 97, 0, 0, 0, 0])

    def get_chunk(audio_source, chunk_size=1024):
        yield wave_header16_k16_bit_mono
        while True:
            time.sleep(chunk_size / 32000)
            chunk = audio_source.read(chunk_size)
            if not chunk:
                break
            yield chunk

    # check next 3 lines, if they're redundant, remove these.
    pron_assessment_params_json = "{\"ReferenceText\":\"%s\",\"GradingSystem\":\"HundredMark\"," \
                                  "\"Dimension\":\"Comprehensive\"}" % reference_text
    pron_assessment_params_base64 = base64.b64encode(bytes(pron_assessment_params_json, 'utf-8'))
    pron_assessment_params = str(pron_assessment_params_base64, "utf-8")

    url = f"https://{region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language" \
          f"={language_code}"
    headers = {'Accept': 'application/json;text/xml',
               'Connection': 'Keep-Alive',
               'Content-Type': 'audio/wav; codecs=audio/pcm; samplerate=16000',
               'Ocp-Apim-Subscription-Key': subscription_key,
               'Pronunciation-Assessment': pron_assessment_params,
               'Transfer-Encoding': 'chunked',
               'Expect': '100-continue'}

    response = requests.post(url=url, data=get_chunk(speech_file), headers=headers)

    return response.text


####################
# Below lives codes by Kenneth Yip
####################

def upload_blob(source_file_name):
    """
    Uploads a file to the bucket.
    Created by: Kenneth Y.
    """
    storage_path = "/tmp/"
    bucket_name = "ricciwawa"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_file_name)

    blob.upload_from_filename(storage_path + source_file_name)
    print("Successful")


# create a random string for hash
def get_random_string(length):
    """
    Created by: Kenneth Y.
    """
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_hashed_filename(ext='.wav'):
    date_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    hashed_id = sha1(str.encode(get_random_string(10) + date_time)).hexdigest()
    return str(hashed_id) + ext


############################################ Speech to Text MSFT ################################
previous_word_boundry_offset = 0
previous_word_audio_offset = 0
first_offset = 0


def speech_tts_msft(lang, original_input_text, mp3_output_filename):
    """COPIED"""
    """
    A text to speech converter function
    => Seems like abandoned function.
    """
    storage_path = "/tmp/"
    lang = lang.lower().strip(" \"\'")
    # print(lang, original_input_text, mp3_output_filename)
    previous_word_boundry_offset = 0
    previous_word_audio_offset = 0
    first_offset = 0
    total_len = 0
    input_text = ""
    complete_line = ""
    # input_text = original_input_text.replace("\n","").replace("<BR>","<p></p>")
    # Azure does not accept <BR> as line break but <p></p> increases the length, therefore use \n\n\n\n
    input_text = original_input_text.replace("\n", "").replace("<BR>", "\n")
    import azure.cognitiveservices.speech as speechsdk
    from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, \
        SpeechSynthesisOutputFormat, SpeechSynthesisEventArgs, SpeechSynthesisWordBoundaryEventArgs
    from azure.cognitiveservices.speech.audio import AudioOutputConfig
    timing_file_name = mp3_output_filename.replace(".mp3", "_timing.txt")
    with open(storage_path + timing_file_name, 'a') as f:
        pass
    # first offset is to remove the first string that contains Azure information
    first_offset = 0

    def tts_callback(self):
        # print (self)
        temp = 0

    def show_tts_text(evt):
        try:
            global previous_word_boundry_offset, previous_word_audio_offset, first_offset
            # print (input_text[previous_word_boundry_offset : evt.text_offset],previous_word_boundry_offset, evt.text_offset, evt.audio_offset, evt.audio_offset - previous_word_audio_offset)
            # use mp3_timing here... return it as json data
            with open(storage_path + timing_file_name, 'a') as f:
                temp_line = {}

                temp_line["char_start"] = previous_word_boundry_offset - first_offset

                # first time
                if previous_word_boundry_offset == 0:
                    temp_line["char_end"] = 220
                else:
                    temp_line["char_end"] = evt.text_offset - first_offset
                # if (line_counter == 0):
                # print ("466 ", first_offset, evt.text_offset)

                if first_offset == 0:
                    first_offset = temp_line["char_end"]
                temp_word = input_text[previous_word_boundry_offset: evt.text_offset]
                temp_line["chars"] = temp_word.replace("\n", "<BR>")
                temp_line["audio_start"] = previous_word_audio_offset
                temp_line["audio_end"] = evt.audio_offset

                if len(temp_word) > 0:
                    f.write(json.dumps(temp_line))
                    f.write("\n")

            previous_word_boundry_offset = evt.text_offset
            previous_word_audio_offset = evt.audio_offset
        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)
            print("line 479 ", error_message)
        return ("")

    try:
        # speech_key, service_region = "9b8ded5a42674ea59cac09faeff3b616", "eastus"
        speech_key, service_region = "aae01d96cdce4194a17db9f5be956e11", "eastasia"
        # speech_key, service_region = "d273b009107642f6ab9ea4e1727a3b9b", "eastasia"
        speech_config = SpeechConfig(
            subscription=speech_key, region=service_region)
        speech_config.set_property_by_name(
            "SpeechServiceResponse_Synthesis_WordBoundaryEnabled", "true")
        if (lang == "hk"):
            speech_config.speech_synthesis_language = "zh-HK"
            speech_config.speech_synthesis_voice_name = "Microsoft Server Speech Text to Speech Voice (zh-HK, HiuMaanNeural)"
            input_text = '<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zn-HK"><voice name="zh-HK-HiuMaanNeural"><mstts:express-as style="newscast"><prosody rate="-35.00%">' + \
                         input_text + ' </prosody></mstts:express-as></voice></speak>'
        elif (lang == "tw"):
            # print("HELLO")
            speech_config.speech_synthesis_language = "zh-CN"
            speech_config.speech_synthesis_voice_name = "Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoxiaoNeural)"
            input_text = '<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-CN"><voice name="zh-CN-XiaoxiaoNeural"><mstts:express-as style="newscast"><prosody rate="-45.00%">' + \
                         input_text + '</prosody></mstts:express-as></voice></speak>'
        elif (lang == "ja"):
            speech_config.speech_synthesis_language = "ja-JP"
            speech_config.speech_synthesis_voice_name = "Microsoft Server Speech Text to Speech Voice (ja-JP, NanamiNeural)"
            input_text = '<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="ja-JP"><voice name="ja-JP-NanamiNeural"><mstts:express-as style="newscast"><prosody rate="-25.00%">' + \
                         input_text + '</prosody></mstts:express-as></voice></speak>'
        elif (lang == "en-US"):
            print("line 461")
            speech_config.speech_synthesis_language = "en-US"
            speech_config.speech_synthesis_voice_name = "Microsoft Server Speech Text to Speech Voice (en-US, en-US-AriaNeural)"
            input_text = '<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US"><voice name="en-US-AriaNeural"><mstts:express-as style="customerservice"><prosody rate="-20.00%">' + \
                         input_text + '</prosody></mstts:express-as></voice></speak>'

        # speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat["Audio24Khz96KBitRateMonoMp3"])
        speech_config.set_speech_synthesis_output_format(
            SpeechSynthesisOutputFormat["Audio24Khz48KBitRateMonoMp3"])

        synthesizer = SpeechSynthesizer(
            speech_config=speech_config, audio_config=None)
        # get the timing of speech per character
        synthesizer.synthesis_word_boundary.connect(
            lambda evt: show_tts_text(evt))
        result = synthesizer.speak_ssml_async(input_text).get()
        stream = AudioDataStream(result)
        stream.save_to_wav_file(storage_path + mp3_output_filename)
        # save to firebase storage
        upload_blob(mp3_output_filename)
        # upload timing file
        upload_blob(mp3_output_filename.replace(".mp3", "_timing.txt"))
        # os.remove(storage_path+mp3_output_filename)
        return result
    except ValueError as exc:
        # This will be raised if the token is expired or any other
        # verification checks fail.
        error_message = str(exc)
        logging.info(error_message)
        return "error tts"


# translate to user prefered language
# first check datastore, if it is not there, use Google translate

def translate_word(word):
    """
    @author: Mohammad
    Will translate a traditional word to tagalog, indonesian, and korean currently. Uses datastore dictionary.
    If a word is missing, then it'll use Google Translate.
    Returns a dictionary.
    """
    query = datastore_client.query(kind='dictionary')
    query.add_filter('trad', '=', word)
    word_translations = list(query.fetch(limit=1))
    data = dict()
    if word_translations:
        data['tagalog'] = word_translations[0]['tagalog']
        data['indonesian'] = word_translations[0]['indonesian']
        data['korean'] = word_translations[0]['korean']
    else:
        data['tagalog'] = google_translate(word, "zh-TW", "tl")
        data['indonesian'] = google_translate(word, "zh-TW", "id")
        data['korean'] = google_translate(word, "zh-TW", "ko")
    return data


def google_translate(text, source_language_code, target_language_code):
    try:
        client = translate.TranslationServiceClient()
        return_translated_text = ""
        # handle 1500 character limit

        if len(text) > 1500:
            text_list = []
            sentences = text.split(".")
            split_count = len(text) // 1200
            sentence_count = len(sentences) // split_count

            for sc in range(split_count):
                start_ind = sc * sentence_count
                end_ind = start_ind + sentence_count
                text_list.append(".".join(sentences[start_ind:end_ind]))

            for text_part in text_list:
                response = client.translate_text(
                    parent="projects/ricciwawa/locations/global",
                    contents=[text_part],
                    mime_type="text/html",  # mime types: text/plain, text/html
                    source_language_code=source_language_code,
                    target_language_code=target_language_code
                )
                # Display the translation for each input text provided
                for translation in response.translations:
                    # for some reasons, Google may add spaces
                    return_translated_text = return_translated_text + translation.translated_text
        else:
            # Detail on supported types can be found here:
            # https://cloud.google.com/translate/docs/supported-formats
            response = client.translate_text(
                parent="projects/ricciwawa/locations/global",
                contents=[text],
                mime_type="text/html",  # mime types: text/plain, text/html
                source_language_code=source_language_code,
                target_language_code=target_language_code
            )
            # Display the translation for each input text provided
            for translation in response.translations:
                # for some reasons, Google may add spaces
                return_translated_text = return_translated_text + translation.translated_text
        return return_translated_text.replace("> ", ">").replace(" < ", "<")
    except ValueError as exc:
        # This will be raised if the token is expired or any other
        # verification checks fail.
        error_message = str(exc)
        logging.info(error_message)
        return ""


# This is to translate a list of text
# it calls google translate one word by one word.  This could be time consumption
def google_translate_list(text_list, source_language_code, target_language_code):
    results = []
    for text in text_list:
        temp_result = google_translate(text, source_language_code, target_language_code)
        results.append(temp_result)
    return results


def dictionary_lookup(trad_spaced_sentence, sim_spaced_sentence):
    try:
        # pinyin is a list
        # replace <BR> with <p> because will
        all_words = trad_spaced_sentence.replace("<BR>", "<BR><p>").split("<p>")
        all_words_sim = sim_spaced_sentence.replace("<BR>", "<BR><p>").split("<p>")

        all_translated_words = []
        word_counter = 0  # used to identify the simplified word matching the trad word
        for word in all_words:
            translated_word = {}
            translated_word["word"] = word
            translated_word["eng"] = []
            translated_word["sim"] = []
            translated_word["trad"] = []
            translated_word["tagalog"] = []
            translated_word["indonesian"] = []
            translated_word["korean"] = []
            translated_word["pinyin"] = []
            if (word != "<BR>"):
                word = word.strip()
                datastore_query_result = dictionary_lookup_datastore(word)
                counter = 0
                # loop to find all the meaning
                for items in datastore_query_result:
                    counter += 1
                    # may contain multipll meaning seperated by ,
                    temp_eng = items["english"]
                    temp_sim = items["sim"]
                    temp_trad = items["trad"]
                    temp_tagalog = items["tagalog"]
                    temp_indonesian = items["indonesian"]
                    temp_korean = items["korean"]
                    temp_pinyin = items["pinyin"].split(" ")
                    translated_word["eng"].append(temp_eng)
                    translated_word["sim"].append(temp_sim)
                    translated_word["trad"].append(temp_trad)
                    translated_word["tagalog"].append(temp_tagalog)
                    translated_word["indonesian"].append(temp_indonesian)
                    translated_word["korean"].append(temp_korean)
                    translated_word["pinyin"].append(temp_pinyin)
                # cannot find such wording and the word length >1
                if (counter == 0 and len(word) > 1):
                    temp_sim = ""
                    word_pinyin = []
                    each_char_pinyin = []  # single char could have multiple pinyins, word can only have one pinyin
                    i = 0
                    while i < len(word):
                        # for each_char in word:
                        each_char_pinyin = []  # it is a word, so only one pinyin
                        each_char = word[i]
                        next_char = ""
                        last_char = ""
                        skip_flag = False
                        if (i + 1) < len(word):
                            next_char = word[i + 1]
                            two_chars_result = dictionary_lookup_datastore(each_char + next_char)
                            if two_chars_result != []:
                                print(two_chars_result[0]["pinyin"])
                                each_char_pinyin.append(two_chars_result[0]["pinyin"])
                                skip_flag = True
                                # jump one char ahead
                                i = i + 1
                        i = i + 1
                        if (skip_flag == False):
                            temp_result = dictionary_lookup_datastore(each_char)
                            # only use the first pinyin reported, could be an incorrect pinyin
                            if (temp_result != []):
                                # each character may have multiple meanings/pinyin
                                for each_temp_result in temp_result:
                                    if (len(temp_result[0]["sim"]) > 0):
                                        # could have multiple meanings and multiple pinyins,
                                        # if each_temp_result["pinyin"] is not a list, don't loop
                                        if (type(each_temp_result["pinyin"]) is list):
                                            for each_pinyin in each_temp_result["pinyin"]:
                                                # if not added before
                                                if not (each_pinyin in each_char_pinyin):
                                                    each_char_pinyin.append(each_pinyin)
                                        else:
                                            # if not a list, add directly
                                            if not (each_temp_result["pinyin"] in each_char_pinyin):
                                                each_char_pinyin.append(each_temp_result["pinyin"])
                                    else:
                                        # there is no pinyin, add space
                                        temp_pinyin = "&nbsp;"
                                if (temp_result.count(",") > 0):
                                    temp_pinyin = "(" + temp_pinyin + ")"
                                # if no sim, add space
                                if (len(temp_result[0]["sim"]) > 0):
                                    temp_sim = temp_result[0]["sim"][0]
                                else:
                                    temp_sim = each_char
                        # a list of pinyin per word.  Each char has its own list of pinyin
                        temp_sim = temp_sim.strip()
                        # a char may have mutliple pinyins, join them by comma
                        word_pinyin.append(",".join(each_char_pinyin))
                    # if it is a word, make sure there is one element in word_pinyin
                    if (len(word) > 1):
                        new_word_pinyin = ""  # a string to hold pinyin
                        for each_word_pinyin in word_pinyin:
                            if (type(each_word_pinyin) is list):
                                new_word_pinyin = new_word_pinyin + " " + " ".join(each_word_pinyin)
                            else:
                                new_word_pinyin = new_word_pinyin + " " + each_word_pinyin
                        word_pinyin = new_word_pinyin.strip().split(" ")
                    word_sim = all_words_sim[word_counter];
                    # translation from Google
                    # eng_meaning = google_translate(word, 'zh-TW', "en")
                    # id_meaning = google_translate(word, 'zh-TW', "id")
                    # tl_meaning = google_translate(word, 'zh-TW', "tl")
                    # ko_meaning = google_translate(word, 'zh-TW', "ko")

                    # now = datetime.datetime.now()
                    # date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                    # entity = datastore.Entity(key=datastore_client.key('dictionary'))
                    # entity.update({
                    #    "trad": word,
                    #    "sim": word_sim,
                    #    "pinyin": word_pinyin,
                    #    "english": eng_meaning,
                    #    "indonesian": id_meaning,
                    #    "tagalog": tl_meaning,
                    #    "korean": ko_meaning,
                    #    'timestamp': date_time,
                    # })
                    # datastore_client.put(entity)
                    # translated_word ["eng"].append(eng_meaning)
                    translated_word["sim"].append(word_sim)
                    translated_word["trad"].append(word)
                    # translated_word ["tagalog"].append(tl_meaning)
                    # translated_word ["indonesian"].append(id_meaning)
                    # translated_word ["korean"].append(ko_meaning)
                    translated_word["pinyin"].append(word_pinyin)
            all_translated_words.append(translated_word)
            word_counter = word_counter + 1
        # create simplified Chinese for
        return all_translated_words

    except ValueError as exc:
        print("error")
        error_message = str(exc)
        logging.info(error_message)
        return ("", "")


# translate to traditional text first
def google_translate_v2(text, source_language_code, target_language_code):
    try:
        # The input text could be simplified or traditional
        # loop twice to get the simplified and traditional versions
        client = translate.TranslationServiceClient()
        return_translated_text = ""
        # Detail on supported types can be found here:
        # https://cloud.google.com/translate/docs/supported-formats
        response = client.translate_text(
            parent="projects/ricciwawa/locations/global",
            contents=[text],
            mime_type="text/html",  # mime types: text/plain, text/html
            source_language_code=source_language_code,
            target_language_code=target_language_code
        )
        # Display the translation for each input text provided
        for translation in response.translations:
            # for some reaons, Google may add spaces
            return_translated_text = return_translated_text + translation.translated_text
        return return_translated_text.replace("> ", ">").replace(" < ", "<")
    except ValueError as exc:
        # This will be raised if the token is expired or any other
        # verification checks fail.
        error_message = str(exc)
        logging.info(error_message)
        return ""


def dictionary_lookup_datastore(input_text):
    # query = datastore_client.query(kind='dictionary')
    # query.add_filter('trad', '=', input_text)
    # datastore_query_result = list(query.fetch(limit=20))
    res = list(Word.objects.filter(trad__in=input_text).values())
    for word in res:
        word['word'] = word['trad']
        word['korean'] = word['ko']
        word['indonesian'] = word['ind']
        word['tagalog'] = word['tl']
        word['english'] = word['eng']
    return res


def uid_to_id_token(uid):
    """Get the ID token for the given UID."""

    custom_token = auth.create_custom_token(uid)
    url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken?key=AIzaSyAMC3CeECe7u8UuOGYObBXPSrKRGSm3Yto'
    body = {
        "token": custom_token,
        "returnSecureToken": True
    }
    response = requests.post(url, data=body).json()
    # print(response)
    return response['idToken']


def add_translation_data_to_database(filename):
    """Add translation data to the database. Not a regularly used function in the server(a script file actually)"""
    words = open(filename, 'r', encoding="utf-8").readlines()

    for i, word in enumerate(words):
        word = json.loads(word)
        trad = word["trad"]
        sim = word["sim"]
        eng = word["english"]
        ind = word["indonesian"]
        es = word['es']
        vi = word['vi']
        hu = word['hu']
        ko = word['korean']
        tl = word['tagalog']
        pinyin = word['pinyin']
        Word.objects.get_or_create(trad=trad, sim=sim, eng=eng, ind=ind, es=es, vi=vi, hu=hu, ko=ko, tl=tl,
                                   pinyin=pinyin)
        print(i)
    print("added data into database")


def analyze_text_syntax(text, lang_choice):
    try:
        return_data = []
        spaced_return = ""  # the traditional Chinese text.  Each element
        # ============= For Google library ==========
        client = language.LanguageServiceClient()
        document = language.Document(
            content=text.replace("<BR>", "AYHEBXTEUDJDGAUBZFDQ"),
            language=lang_choice,
            # type_=language.Document.Type.HTML)
            type_=language.Document.Type.PLAIN_TEXT)
        response = client.analyze_syntax(document=document)
        return_data.append(response)
        # ============= For Google API Call ==========

        a_sentences = response.sentences

        # store tokens and their positions
        tokens = response.tokens
        token_list = []  # holds the tokens
        # hold the tokens pos in a sentence
        for token in tokens:
            token_list.append(token.text.content)
        # store entities
        # use another document to avoid the <BR> replacement
        document = language.Document(
            content=text,
            language=lang_choice,
            type_=language.Document.Type.HTML)
        # type_=language.Document.Type.PLAIN_TEXT)
        response = client.analyze_entities(document=document)
        return_data.append(response)
        a_entity_name = []
        for entity in response.entities:
            if not ("(" in entity.name):
                if len(entity.name) > 1 and not entity.name in a_entity_name:  # if only one character, do not include it
                    a_entity_name.append(entity.name)

        # get phrase and add them to a_entity
        for list_phrase in cedict_phrase:
            for each_phrase in cedict_phrase[list_phrase]:
                if each_phrase in text:
                    a_entity_name.append(each_phrase)
                    print(1017, each_phrase)

        # for each sentence, replace the entity with spaces and the store the position of the entities
        sen_counter = 0
        for current_sentence in a_sentences:
            a_entity_position = {}
            a_token_pos = {}
            cur_text = current_sentence.text.content  # curent text content to store the sentence text
            for entity_name in a_entity_name:
                for m in re.finditer(entity_name, cur_text):
                    # must be longer than one and contain no digit
                    if len(entity_name) > 1 and not bool(re.search(r'\d', entity_name)):
                        a_entity_position[m.start()] = entity_name
                        # all entities are now replaced by spaces
                        # cur_text = cur_text.replace(entity_name,  " "*len(entity_name))
            # find the tokens per sentence
            j = 0
            temp_cur_text = cur_text

            while j < len(token_list):
                if token_list[j] is not None:
                    pos = temp_cur_text.find(token_list[j])
                    if pos > -1:
                        # print ("line 572", pos, token_list[j])
                        a_token_pos[pos] = token_list[j]
                        temp_cur_text = temp_cur_text[0:pos] + " " * len(token_list[j]) + temp_cur_text[
                                                                                          pos + len(token_list[j]):]
                        token_list[j] = None
                j = j + 1

            sen_counter = sen_counter + 1
            # print (a_token_pos)
            # print (a_entity_position)
            new_sentence = []
            i = 0
            while i < len(cur_text):
                if i in a_entity_position:
                    new_sentence.append(a_entity_position[i])
                    i = i + len(a_entity_position[i])
                elif i in a_token_pos:
                    new_sentence.append(a_token_pos[i])
                    i = i + len(a_token_pos[i])
                else:
                    i = i + 1
            # cannot trust the <BR> returned by Google in new_sentence
            # "<p>"+<p>.join the first <p> is for sentence break.  The second "<p>" is for join
            spaced_return = spaced_return + "<p>" + "<p>".join(new_sentence)
            spaced_return = spaced_return.replace("<<p>BR<p>>", "<BR>").replace("<BR<p>>", "<BR>")
            # print("968", spaced_return)
            # spaced_return = spaced_return.replace("<BR><p><BR><p>","<BR>")
            # print("970", spaced_return)
        spaced_return = spaced_return.replace("AYHEBXTEUDJDGAUBZFDQ", "<BR>").replace("<p>*=*=*", "<BR>").replace(
            "*<p>=*=*", "<BR>").replace("*<p>=*=<p>*", "<BR>").replace("<BR><BR>", "<p><BR>").replace(
            "<BR>*<p>=*<p>=*<p>", "<p><BR>")
        spaced_return = spaced_return[3:]  # remove the leading <p><BR>
        return spaced_return

    except ValueError as exc:
        print("error")
        error_message = str(exc)
        logging.info(error_message)
        return "", ""


def word_grouping(input_text):
    # text = google_translate (input_text,"zh-TW", "zh-TW")
    # start = timeit.default_timer()
    text = analyze_text_syntax(input_text, "zh-TW")
    # print(text)
    # stop = timeit.default_timer()
    # execution_time = stop - start
    # print(execution_time)
    # start = timeit.default_timer()
    sim_chinese_text = google_translate_v2(text, "zh-TW", "zh-CN")
    trad_chinese_text = google_translate_v2(sim_chinese_text, "zh-CN", "zh-TW")
    # stop = timeit.default_timer()

    # print('==============================')
    # print('==============================')
    # print(trad_chinese_text)
    # print('==============================')
    # print('==============================')
    # print(sim_chinese_text)
    # print('==============================')
    # print('==============================')
    all_words = trad_chinese_text.replace("<BR>", "<BR><p>").split("<p>")
    all_words_sim = sim_chinese_text.replace("<BR>", "<BR><p>").split("<p>")
    # print(all_words)
    # all_word_translations = list(Word.objects.filter(trad__in=all_words).values())
    #
    # for word in all_word_translations:
    #     word['word'] = word['trad']
    #     word['korean'] = word['ko']
    #     word['indonesian'] = word['ind']
    #     word['tagalog'] = word['tl']
    #
    # final_grouped_words = []
    # for tw in all_words:
    #     word = None
    #     for w in all_word_translations:
    #         if w['trad'] == tw:
    #             word = w
    #             break
    #
    #     if word is None:
    #         word = {'trad': tw}
    #
    #     final_grouped_words.append(word)
    # execution_time = stop - start
    # print(execution_time)

    all_translated_words = []
    word_counter = 0  # used to identify the simplified word matching the trad word
    for word in all_words:
        translated_word = {"word": word, "eng": [], "sim": [], "trad": [], "tagalog": [], "indonesian": [],
                           "korean": [], "pinyin": []}
        if word != "<BR>":
            word = word.strip()
            res = list(Word.objects.filter(trad=word).values())
            counter = 0
            # loop to find all the meaning
            for items in res:
                counter += 1
                # may contain multiple meaning seperated by ,
                temp_eng = items["eng"]
                temp_sim = items["sim"]
                temp_trad = items["trad"]
                temp_tagalog = items["tl"]
                temp_indonesian = items["ind"]
                temp_korean = items["ko"]
                temp_pinyin = items["pinyin"].split(" ")
                translated_word["eng"].append(temp_eng)
                translated_word["sim"].append(temp_sim)
                translated_word["trad"].append(temp_trad)
                translated_word["tagalog"].append(temp_tagalog)
                translated_word["indonesian"].append(temp_indonesian)
                translated_word["korean"].append(temp_korean)
                translated_word["pinyin"].append(temp_pinyin)

            # cannot find such wording and the word length >1
            if counter == 0 and len(word) > 1:
                temp_sim = ""
                word_pinyin = []
                each_char_pinyin = []  # single char could have multiple pinyins, word can only have one pinyin
                i = 0
                while i < len(word):
                    # for each_char in word:
                    each_char_pinyin = []  # it is a word, so only one pinyin
                    each_char = word[i]
                    next_char = ""
                    last_char = ""
                    skip_flag = False
                    if (i + 1) < len(word):
                        next_char = word[i + 1]
                        two_chars_result = list(Word.objects.filter(trad=each_char + next_char).values())
                        if two_chars_result:
                            print(two_chars_result[0]["pinyin"])
                            each_char_pinyin.append(two_chars_result[0]["pinyin"])
                            skip_flag = True
                            # jump one char ahead
                            i = i + 1
                    i = i + 1
                    if not skip_flag:
                        temp_result = list(Word.objects.filter(trad=each_char).values())
                        # only use the first pinyin reported, could be an incorrect pinyin
                        if temp_result:
                            # each character may have multiple meanings/pinyin
                            for each_temp_result in temp_result:
                                if len(temp_result[0]["sim"]) > 0:
                                    # could have multiple meanings and multiple pinyins,
                                    # if each_temp_result["pinyin"] is not a list, don't loop
                                    if type(each_temp_result["pinyin"]) is list:
                                        for each_pinyin in each_temp_result["pinyin"]:
                                            # if not added before
                                            if not (each_pinyin in each_char_pinyin):
                                                each_char_pinyin.append(each_pinyin)
                                    else:
                                        # if not a list, add directly
                                        if not (each_temp_result["pinyin"] in each_char_pinyin):
                                            each_char_pinyin.append(each_temp_result["pinyin"])
                                else:
                                    # there is no pinyin, add space
                                    temp_pinyin = "&nbsp;"
                            if temp_result.count(",") > 0:
                                temp_pinyin = "(" + temp_pinyin + ")"
                            # if no sim, add space
                            if len(temp_result[0]["sim"]) > 0:
                                temp_sim = temp_result[0]["sim"][0]
                            else:
                                temp_sim = each_char
                    # a list of pinyin per word.  Each char has its own list of pinyin
                    temp_sim = temp_sim.strip()
                    # a char may have multiple pinyins, join them by comma
                    word_pinyin.append(",".join(each_char_pinyin))
                # if it is a word, make sure there is one element in word_pinyin
                if len(word) > 1:
                    new_word_pinyin = ""  # a string to hold pinyin
                    for each_word_pinyin in word_pinyin:
                        if type(each_word_pinyin) is list:
                            new_word_pinyin = new_word_pinyin + " " + " ".join(each_word_pinyin)
                        else:
                            new_word_pinyin = new_word_pinyin + " " + each_word_pinyin
                    word_pinyin = new_word_pinyin.strip().split(" ")
                word_sim = all_words_sim[word_counter]
                translated_word["sim"].append(word_sim)
                translated_word["trad"].append(word)
                translated_word["pinyin"].append(word_pinyin)
        all_translated_words.append(translated_word)
        word_counter = word_counter + 1
    return all_translated_words


def check_file_successfully_uploaded(filename, size, bucket_name='ricciwawa'):
    """
    Check if file is successfully uploaded to Google Cloud Storage
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.get_blob(filename)
    if blob and blob.exists() and blob.size == size:
        print(blob.size)
        return True
    return False


def initiate_transcribing(filename, language_code, bucket_name="ricciwawa"):
    content_url = download_get_signed_up(filename, bucket_name)

    body = {
        'contentUrls': [content_url],
        'locale': language_code,
        'displayName': f'Transcription of file using default model for {language_code}'
    }
    subscription_key = "aea95857cbf14d41b132fefe96a3052e"  # transfer this to settings.py
    region = "eastasia"  # transfer this to settings.py
    endpoint = f'https://{region}.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    response = requests.post(endpoint, json=body, headers=headers).json()

    transcription_id = response['self'].split('/')[-1]
    status = response['status']

    data = {
        'transcription_id': transcription_id,
        'status': status
    }
    return data


def get_transcription_status(transcription_id):
    subscription_key = "aea95857cbf14d41b132fefe96a3052e"  # transfer this to settings.py
    region = "eastasia"  # transfer this to settings.py
    endpoint = f'https://{region}.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions/{transcription_id}'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    response = requests.get(endpoint, headers=headers).json()
    status = response['status']
    return status


def get_transcription_url(transcription_id):
    subscription_key = "aea95857cbf14d41b132fefe96a3052e"  # transfer this to settings.py
    region = "eastasia"  # transfer this to settings.py
    endpoint = f'https://{region}.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions/{transcription_id}/files'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    response = requests.get(endpoint, headers=headers).json()
    data = {
        'transcription_url': response['values'][1]['links']['contentUrl'],
    }
    return data


def start_transcribing(filename):
    host = "http://74.207.245.137:5000"
    # host = "http://localhost:5000"
    url = f"{host}/transcription/start/{filename}/"
    response = requests.get(url).json()
    return response


def get_transcript(tid):
    host = "http://74.207.245.137:5000"
    url = f"{host}/transcription/result/{tid}/"
    response = requests.get(url).json()
    return response
