import json
import datetime
import os
import time

from google.cloud import tasks_v2, storage

from django.conf import settings


# =========================================================
# Creator: Kenneth Yip
# This function is very important
# It gets the text and create the Mandarin and Cantonese audios
# Will soon also have slower Mandarin and Cantonese audios based on Abdul silence adding module
# It calls Azure using background task to generate the MP3 files.  Background task is needed because it takes long time
# We use Azure because its Mandarin audio quality is the best.
# =========================================================
def create_mp3_task(mp3_lang, mp3_text, filename, time_delay=0):
    from google.protobuf import timestamp_pb2
    # Create a client.
    client = tasks_v2.CloudTasksClient()
    # TODO(developer): Uncomment these lines and replace with your values.
    project = 'ricciwawa'
    queue = 'my-queue'
    location = 'asia-east2'
    payload = {"language_code": mp3_lang, "text": mp3_text, "output_filename": filename}

    if settings.DEBUG:
        import requests
        hostname = os.environ.get('HOSTNAME')
        if hostname is None:
            hostname = 'localhost:8000'
        resp = requests.post(hostname + "utils/mp3-task-handler/", data=payload).json()
        # print(resp)
        return
        # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    # Construct the request body.
    task = {
        'app_engine_http_request': {  # Specify the type of request.
            'http_method': tasks_v2.HttpMethod.POST,
            'relative_uri': 'utils/mp3-task-handler/'
        }
    }
    # for local testing
    # print (filename)
    # if mp3_lang == "hk":
    #    result = speech_tts_google (mp3_lang, mp3_text, filename)
    # else:
    #    result = speech_tts_msft (mp3_lang, mp3_text, filename)

    print("512", payload)
    if payload is not None:
        # The API expects a payload of type bytes.
        converted_payload = json.dumps(payload).encode('utf-8')
        # Add the payload to the request.
        task['app_engine_http_request']['body'] = converted_payload
        timestamp = datetime.datetime.utcnow() + datetime.timedelta(1)
        # Add the timestamp to the tasks.
        now = time.time() + 1
        seconds = int(now)
        nanos = int((now - seconds) * 10 ** 9)

        # Create Timestamp protobuf.https://lihkg.com/thread/2432996/page/1
        timestamp = timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)

        task['schedule_time'] = timestamp

        # Use the client to build and send the task.
        response = client.create_task(parent=parent, task=task)


def upload_get_signed_up(filename):
    """
    generate a signed upload url

    Reference:
        https://stackoverflow.com/questions/30843450/how-to-create-google-cloud-storage-signed-urls-on-app-engine-python

    Args:
        filename (str): filename to store in google storage

    Returns:
        (str): returns signed url
    """
    """Generates a v4 signed URL for downloading a blob.

    Note that this method requires a service account key file. You can not use
    this if you are using Application Default Credentials from Google Compute
    Engine or from the Google Cloud SDK.
    """
    bucket_name = 'ricciwawa'
    blob_name = filename

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=15),
        method="PUT",
        content_type="application/octet-stream",
    )
    # print(
    #     "curl -X PUT -H 'Content-Type: application/octet-stream' "
    #     "--upload-file mhb.py '{}'".format(url)
    # )
    return url


def download_get_signed_up(filename):
    """
    Generates Signed Download URL
    """
    bucket_name = 'ricciwawa'
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)

    url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=30),
        method="GET",
    )

    # print("curl '{}'".format(url))
    return url


def create_save_edit_fulldata(trad_words, sim_word, english_words, pinyin_list):
    """
    CHECK WHAT IT IS DOING, IF NEEDS, COPY TO DJ
    """
    all_translated_words = []
    for index, val in enumerate(trad_words):
        translated_word = {}
        translated_word["word"] = trad_words[index]
        translated_word["eng"] = [[english_words[index]]]
        translated_word["sim"] = [sim_word[index]]
        translated_word["trad"] = [trad_words[index]]
        # translated_word["targetted_lang"] = [
        #     [google_translate(english_words[index], "zh", targetted_lang_code)]]
        # translated_word["tagalog"] = [
        #    [google_translate(english_words[index], "zh", "tl")]]
        # translated_word["indonesian"] = [
        #    [google_translate(english_words[index], "zh", "id")]]
        # translated_word["korean"] = [
        #    [google_translate(english_words[index], "zh", "ko")]]
        translated_word["pinyin"] = [[pinyin_list[index]]]
        all_translated_words.append(translated_word)
        # Kenneth 20210926 #######
        # add background task to translate the story to other languages and store them into different languages
        # add background task to have different audio speedt created
        # create_mp3_task("hk", trad_spaced_sentence, str(hashed_id)) different speed

    return all_translated_words
