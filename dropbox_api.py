import dropbox
from api_key import DROPBOX_ACCESS_TOKEN

def dropbox_uploader(file_from, file_to):
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    with open(file_from, 'rb') as f:
        dbx.files_upload(f.read(), file_to)
