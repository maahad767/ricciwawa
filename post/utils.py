import datetime

from google.cloud import tasks_v2, storage

from utils.utils import speech_tts_msft


def create_mp3_task(language_code, text, output_filename, time_delay=0):
    """
    Not being used, check post.tasks.create_mp3_task instead.
    """

    # from google.protobuf import timestamp_pb2
    # Create a client.
    # client = tasks_v2.CloudTasksClient()
    # project = 'ricciwawa'
    # queue = 'my-queue'
    # location = 'asia-east2'
    speech_tts_msft(language_code, text, output_filename)

    # if settings.DEBUG:
    #     import requests
    #     hostname = os.environ.get('HOSTNAME')
    #     if hostname is None:
    #         hostname = 'localhost:8000'
    #     resp = requests.post(hostname + "utils/mp3-task-handler/", data=payload).json()
    #     # print(resp)
    #     return

        # Construct the fully qualified queue name.
    # parent = client.queue_path(project, location, queue)

    # celery
    # Construct the request body.
    # task = {
    #     'app_engine_http_request': {  # Specify the type of request.
    #         'http_method': tasks_v2.HttpMethod.POST,
    #         'relative_uri': 'utils/mp3-task-handler/'
    #     }
    # }
    # for local testing
    # print (filename)
    # if mp3_lang == "hk":
    #    result = speech_tts_google (mp3_lang, mp3_text, filename)
    # else:
    #    result = speech_tts_msft (mp3_lang, mp3_text, filename)
    #
    # print("512", payload)
    # if payload is not None:
    #     # The API expects a payload of type bytes.
    #     converted_payload = json.dumps(payload).encode('utf-8')
    #     # Add the payload to the request.
    #     task['app_engine_http_request']['body'] = converted_payload
    #     timestamp = datetime.datetime.utcnow() + datetime.timedelta(1)
    #     # Add the timestamp to the tasks.
    #     now = time.time() + 1
    #     seconds = int(now)
    #     nanos = int((now - seconds) * 10 ** 9)
    #
    #     # Create Timestamp protobuf.https://lihkg.com/thread/2432996/page/1
    #     timestamp = timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)
    #
    #     task['schedule_time'] = timestamp
    #
    #     # Use the client to build and send the task.
    #     response = client.create_task(parent=parent, task=task)







def create_save_edit_fulldata(trad_words, sim_word, english_words, pinyin_list):
    """
    NOT BEING USED. CHECK post.tasks.add_full_data instead.
    """
    all_translated_words = []
    for index, val in enumerate(trad_words):
        translated_word = {}
        translated_word["word"] = trad_words[index]
        translated_word["eng"] = [[english_words[index]]]
        translated_word["sim"] = [sim_word[index]]
        translated_word["trad"] = [trad_words[index]]
        # translated_word["tagalog"] = [
        #    [google_translate(val, "hk", "tl")]]
        # translated_word["indonesian"] = [
        #    [google_translate(val, "hk", "id")]]
        # translated_word["korean"] = [
        #    [google_translate(val, "hk", "ko")]]
        translated_word["pinyin"] = [[pinyin_list[index]]]
        all_translated_words.append(translated_word)

        # replace trad_words[index] with val
        # translation each word for all the languages.

    return all_translated_words


