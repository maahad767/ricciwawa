import json
import logging
import random
import string
import requests
import time
import base64

from google.cloud import texttospeech, speech, storage


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
    client = speech.SpeechClient()
    binary_audio = speech_file.read()
    audio = speech.RecognitionAudio(content=binary_audio)
    config = speech.RecognitionConfig({
        'encoding': speech.RecognitionConfig.AudioEncoding.LINEAR16,
        'sample_rate_hertz': int(sample_rate),
        'audio_channel_count': int(audio_channel_count),
        'language_code': language_code,
    })
    response = client.recognize(config=config, audio=audio)
    transcript = str()
    for result in response.results:
        transcript += result.alternatives[0].transcript
        print("Transcript: {}".format(result.alternatives[0].transcript))

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
    bucket_name = "ricciwawa"
    storage_path = "media/temp/"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_file_name)

    blob.upload_from_filename(storage_path + source_file_name)


# create a random string for hash
def get_random_string(length):
    """
    Created by: Kenneth Y.
    """
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def speech_tts_msft(lang, original_input_text, mp3_output_filename):
    """
    A text to speech function using Azure APIs.
    Created By: Kenneth Y.
    """
    previous_word_boundry_offset = 0
    previous_word_audio_offset = 0
    first_offset = 0
    total_len = 0
    input_text = ""
    complete_line = ""
    # input_text = original_input_text.replace("\n","").replace("<BR>","<p></p>")
    # Azure does not accept <BR> as line break but <p></p> increases the length, therefore use \n\n\n\n
    input_text = original_input_text.replace("\n", "").replace("<BR>", "\n")
    # import azure.cognitiveservices.speech as speechsdk
    from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, \
        SpeechSynthesisOutputFormat
    # , SpeechSynthesisEventArgs, SpeechSynthesisWordBoundaryEventArgs
    # from azure.cognitiveservices.speech.audio import AudioOutputConfig
    timing_file_name = mp3_output_filename.replace(".mp3", "_timing.txt")
    # first offset is to remove the first string that contains Azure information
    first_offset = 0

    def tts_callback(self):
        # print (self)
        temp = 0

    def show_tts_text(evt):
        try:
            global previous_word_boundry_offset, previous_word_audio_offset, first_offset
            print(925, evt.text_offset)
            # print (input_text[previous_word_boundry_offset : evt.text_offset],previous_word_boundry_offset,
            # evt.text_offset, evt.audio_offset, evt.audio_offset - previous_word_audio_offset)
            # use mp3_timing here... return it as json data
            with open("/tmp/" + timing_file_name, 'a') as f:
                temp_line = {"char_start": previous_word_boundry_offset - first_offset}
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
        return ""

    try:
        # speech_key, service_region = "9b8ded5a42674ea59cac09faeff3b616", "eastus"
        speech_key, service_region = "aae01d96cdce4194a17db9f5be956e11", "eastasia"
        # speech_key, service_region = "d273b009107642f6ab9ea4e1727a3b9b", "eastasia"
        speech_config = SpeechConfig(
            subscription=speech_key, region=service_region)
        speech_config.set_property_by_name(
            "SpeechServiceResponse_Synthesis_WordBoundaryEnabled", "true")
        if lang == "hk":
            speech_config.speech_synthesis_language = "zh-HK"
            speech_config.speech_synthesis_voice_name = "Microsoft Server Speech Text to Speech Voice (zh-HK, HiuMaanNeural)"
            input_text = '<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zn-HK"><voice name="zh-HK-HiuMaanNeural"><mstts:express-as style="newscast"><prosody rate="-35.00%">' + \
                         input_text + ' </prosody></mstts:express-as></voice></speak>'
        elif lang == "tw":
            speech_config.speech_synthesis_language = "zh-CN"
            speech_config.speech_synthesis_voice_name = "Microsoft Server Speech Text to Speech Voice (zh-CN, XiaoxiaoNeural)"
            input_text = '<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-CN"><voice name="zh-CN-XiaoxiaoNeural"><mstts:express-as style="newscast"><prosody rate="-45.00%">' + \
                         input_text + '</prosody></mstts:express-as></voice></speak>'
        elif lang == "ja":
            speech_config.speech_synthesis_language = "ja-JP"
            speech_config.speech_synthesis_voice_name = "Microsoft Server Speech Text to Speech Voice (ja-JP, NanamiNeural)"
            input_text = '<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="ja-JP"><voice name="ja-JP-NanamiNeural"><mstts:express-as style="newscast"><prosody rate="-25.00%">' + \
                         input_text + '</prosody></mstts:express-as></voice></speak>'
        elif lang == "en-US":
            print("line 461")
            speech_config.speech_synthesis_language = "en-US"
            speech_config.speech_synthesis_voice_name = "Microsoft Server Speech Text to Speech Voice (en-US, en-US-AriaNeural)"
            input_text = '<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US"><voice name="en-US-AriaNeural"><mstts:express-as style="customerservice"><prosody rate="-20.00%">' + \
                         input_text + '</prosody></mstts:express-as></voice></speak>'

        speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat["Audio24Khz48KBitRateMonoMp3"])

        synthesizer = SpeechSynthesizer(
            speech_config=speech_config, audio_config=None)
        # get the timing of speech per character
        synthesizer.synthesis_word_boundary.connect(
            lambda evt: show_tts_text(evt))
        result = synthesizer.speak_ssml_async(input_text).get()
        stream = AudioDataStream(result)
        stream.save_to_wav_file(mp3_output_filename)

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
