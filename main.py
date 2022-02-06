import io
import os
import json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "memory-box-329820.json"
client = vision.ImageAnnotatorClient()

class Parser_Secrets():
    def __init__(self, filename):
        json_obj = open(filename, 'r')
        data = json.load(json_obj)
        self.client_id = data["web"]["client_id"]
        self.client_secret = data["web"]["client_secret"]
        self.project_id = data["web"]["project_id"]
        
class Service():
    def __init__(self, client_file, api_version, api_name, scopes, developerKey = None):
        self.client_file = client_file
        self.api_version = api_version
        self.api_name = api_name
        self.scopes = scopes
        self.developerKey = developerKey
        self.credentials = None
        
        pickle_file = f'token_{self.api_name}_{self.api_version}.pickle'
        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                self.credentials = pickle.load(token)

        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.client_file, self.scopes)
                self.credentials = flow.run_local_server()

            with open(pickle_file, 'wb') as token:
                pickle.dump(self.credentials, token)
    def build(self):
        try:
            service = build(self.api_name, self.api_version, credentials=self.credentials, developerKey=self.developerKey)
            print(self.api_name, 'service created successfully')
            return service
        except Exception as e:
            print('Unable to connect.')
            print(e)
            return None

def get_drive_photos(service: Service):
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

def analyze_photo(image_name):
    file_name = os.path.abspath(image_name)

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    f = open("analysis/" + image_name[4:-4] + ".txt", 'w+')
    f.write('Labels:')
    for label in labels:
        f.write(label.description + "  Score:" + str(label.score) + "\n")
        
def analyze_dir(dir_name):
    for file in os.listdir(dir_name):
        analyze_photo(dir_name + "/" + file)
# service_drive = Service("client_secrets.json", "v3", "drive", ['https://www.googleapis.com/auth/drive.readonly'], developerKey="AIzaSyB--_O8kLzBJ_xNinC9MGyw--FDVjmCdIE")
# get_drive_photos(service_drive.build())
analyze_dir("img")