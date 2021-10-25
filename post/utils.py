import json

import datetime
import time

from google.cloud import tasks_v2


# =========================================================
# Creator: Kenneth Yip
# This function is very important
# It gets the text and create the Mandarin and Cantonese audios
# Will soon also have slower Mandarin and Cantonese audios based on Abdul silence adding module
# It calls Azure using background task to generate the MP3 files.  Background task is needed because it takes long time
# We use Azure because its Mandarin audio quality is the best.
# =========================================================
def create_mp3_task(mp3_lang, mp3_text, hashed_id, time_delay=0):
    from google.protobuf import timestamp_pb2
    # Create a client.
    client = tasks_v2.CloudTasksClient()
    print("line 488 at create_mp3_task")
    # TODO(developer): Uncomment these lines and replace with your values.
    project = 'ricciwawa'
    queue = 'my-queue'
    location = 'asia-east2'
    filename = hashed_id + "_" + mp3_lang + ".mp3"
    payload = {"lang": mp3_lang, "mp3_text": mp3_text, "filename": filename}

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

