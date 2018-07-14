import json
import os
import time
import urllib.request


def theta_api(save_dir):

    urllib.request.urlopen("http://192.168.1.1/osc/info").read()

    # create session
    print('Create Session')
    data = json.dumps({"name":"camera.startSession"}).encode('ascii')
    res = urllib.request.urlopen('http://192.168.1.1/osc/commands/execute', data)
    sessionId = json.loads(res.read().decode('utf-8'))["results"]["sessionId"]

    # record fingerprint before taking photo
    res = urllib.request.urlopen('http://192.168.1.1/osc/state', urllib.parse.urlencode({}).encode('ascii'))
    prev_fingerprint = fingerprint = json.loads(res.read().decode('utf-8'))["fingerprint"]

    # take a picture
    data = json.dumps({"name":"camera.takePicture", "parameters": {"sessionId": sessionId}}).encode('ascii')
    urllib.request.urlopen('http://192.168.1.1/osc/commands/execute', data)
    print('Took a photo')

    # get photo url
    fileUri = ""
    while True:
        res = urllib.request.urlopen('http://192.168.1.1/osc/state', urllib.parse.urlencode({}).encode('ascii'))
        j = json.loads(res.read().decode('utf-8'))
        fingerprint = j["fingerprint"]
        fileUri = j["state"]["_latestFileUri"]
        file_name = os.path.basename(fileUri)
        if not fileUri or fingerprint == prev_fingerprint:
            time.sleep(0.2)  # avoid a load by frequent requesting on theta.
        else:
            print('new_photo_file:', file_name)
            break

    # save photo
    print('Saving a photo')
    content = None
    while content is None:
        try:
            data = json.dumps({"name":"camera.getImage", "parameters": {"fileUri": fileUri}}).encode('ascii')
            res = urllib.request.urlopen('http://192.168.1.1/osc/commands/execute', data)
            content = res.read()
            with open(os.path.join(save_dir, file_name), "wb") as file:
                    file.write(content)
        except urllib.error.HTTPError as err:
            if err.code != 400:
                print("taken photo may not be saved to the theta storage yet.")
                raise err
            else:
                time.sleep(0.2)

    print('Saved a photo')

    # close session
    data = json.dumps({"name":"camera.closeSession", "parameters": {"sessionId": sessionId}}).encode('ascii')
    urllib.request.urlopen('http://192.168.1.1/osc/commands/execute', data)
    print('Closed session')
