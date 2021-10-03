from google.cloud import texttospeech, speech
import requests
import time
import base64


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

    with open("output.mp3", "wb") as output_file:
        output_file.write(response.audio_content)

    return open("output.mp3", "wb").read()


def speech_to_text(speech_file, language_code):
    """
    Converts a speech to text using google cloud speech to text api.
    
    :param speech_file: the speech's audio file in .wav format
    :param language_code: the language of the speech
    :return: transcript of the speech as a dictionary
    """
    client = speech.SpeechClient()
    binary_audio = speech_file.read()
    audio = speech.RecognitionAudio(content=binary_audio)
    config = speech.RecognitionConfig({
        'encoding': speech.RecognitionConfig.AudioEncoding.LINEAR16,
        'sample_rate_hertz': 16000,
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
