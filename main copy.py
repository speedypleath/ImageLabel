import io
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from auth import SCOPES, google_auth
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaIoBaseDownload
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/hdd/memory-box-329820-6a22d487571d.json"

class ParserSecrets():
    def __init__(self, filename):
        json_obj = open(filename, 'r')
        data = json.load(json_obj)
        self.client_id = data["web"]["client_id"]
        self.client_secret = data["web"]["client_secret"]
        self.project_id = data["web"]["project_id"]
        
class CredentialsModel():
    def __init__(self, id, token, refresh_token):
        self.id = id
        self.token = token
        self.refresh_token = refresh_token
    def get_google_credentials(self):
        secrets = ParserSecrets("client_secrets.json")
        return Credentials(token=self.token,
                        refresh_token=self.refresh_token,
                        client_id=secrets.client_id,
                        client_secret=secrets.client_secret)


def download_file():
    pass

def get_google_photos(user, credentials: Credentials):
    service = build('photoslibrary', 'v1', credentials=credentials)
    print(service)
    page_token = None
    # while True:
    #     response = service.files().list(q="mimeType='image/jpeg'",
    #                                         spaces='drive',
    #                                         fields='nextPageToken, files(id, name)',
    #                                         pageToken=page_token).execute()
    #     for file in response.get('files', []):
    #         print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
    #         id = file.get('id')
    #         pic = service.files().get_media(fileId=id)
    #         fh = io.FileIO('img/'+ file.get('name'), 'w+')
    #         downloader = MediaIoBaseDownload(fh, pic)
    #         done = False
    #         while done is False:
    #             status, done = downloader.next_chunk()
    #             print("Download %d%%." % int(status.progress() * 100))
    #         fh.close()
    #     page_token = response.get('nextPageToken', None)
    #     if page_token is None:
    #         break

def get_drive_photos(user, credentials: Credentials):
    service = build('drive', 'v3', credentials=credentials, developerKey="AIzaSyB--_O8kLzBJ_xNinC9MGyw--FDVjmCdIE")
    page_token = None
    while True:
        response = service.files().list(q="mimeType='image/jpeg'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=page_token).execute()
        for file in response.get('files', []):
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            id = file.get('id')
            pic = service.files().get_media(fileId=id)
            fh = io.FileIO('img/'+ file.get('name'), 'w+')
            downloader = MediaIoBaseDownload(fh, pic)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
            fh.close()
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

profile = google_auth()
model = CredentialsModel(profile["id"], profile["token"], profile["refresh_token"])
# get_drive_photos(profile, model.get_google_credentials())
get_google_photos(profile, model.get_google_credentials())