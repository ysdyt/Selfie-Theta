import json
import os
import urllib.request


def theta_api(save_dir):

    urllib.request.urlopen("http://192.168.1.1/osc/info").read()

    # create session
    print('Create Session')
    data = json.dumps({"name":"camera.startSession"}).encode('ascii')
    res = urllib.request.urlopen('http://192.168.1.1/osc/commands/execute', data)
    sessionId = json.loads(res.read().decode('utf-8'))["results"]["sessionId"]

    # take a picture
    data = json.dumps({"name":"camera.takePicture", "parameters": {"sessionId": sessionId}}).encode('ascii')
    urllib.request.urlopen('http://192.168.1.1/osc/commands/execute', data)
    print('Took a photo')

    # get photo url
    fileUri = ""
    while not fileUri:
        res = urllib.request.urlopen('http://192.168.1.1/osc/state', urllib.parse.urlencode({}).encode('ascii'))
        fileUri = json.loads(res.read().decode('utf-8'))["state"]["_latestFileUri"]
        file_name = os.path.basename(fileUri)
        print('new_photo_file:', file_name)

    # save photo
    print('Saving a photo')
    data = json.dumps({"name":"camera.getImage", "parameters": {"fileUri": fileUri}}).encode('ascii')
    res = urllib.request.urlopen('http://192.168.1.1/osc/commands/execute', data)
    with open(os.path.join(save_dir, file_name), "wb") as file:
            file.write(res.read())
    print('Saved a photo')

    # close session
    data = json.dumps({"name":"camera.closeSession", "parameters": {"sessionId": sessionId}}).encode('ascii')
    urllib.request.urlopen('http://192.168.1.1/osc/commands/execute', data)
    print('Closed session')
