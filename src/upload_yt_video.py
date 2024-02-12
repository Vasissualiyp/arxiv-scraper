import os
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Set up OAuth 2.0
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRETS_FILE = './config/credentials.json'

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Set up OAuth 2.0
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRETS_FILE = './config/credentials.json'
CREDENTIALS_PICKLE_FILE = './config/token.pickle'  # Path to save credentials

def save_credentials(credentials):
    with open(CREDENTIALS_PICKLE_FILE, 'wb') as token:
        pickle.dump(credentials, token)

def get_authenticated_service():
    credentials = None
    # Check if credentials pickle file exists
    if os.path.exists(CREDENTIALS_PICKLE_FILE):
        print("Loading Credentials From File...")
        with open(CREDENTIALS_PICKLE_FILE, 'rb') as token:
            credentials = pickle.load(token)
    # If there are no valid credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Refreshing Access Token...")
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        save_credentials(credentials)
    return build('youtube', 'v3', credentials=credentials)

#def get_authenticated_service():
#    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
#    # Use run_local_server instead of run_console
#    credentials = flow.run_local_server(port=0)
#    return build('youtube', 'v3', credentials=credentials)


def initialize_upload(youtube, file):
    body = {
        'snippet': {
            'title': 'Your Video Title',
            'description': 'Video description here',
            'tags': ['sample', 'video', 'tags'],
            'categoryId': '22'  # Category ID 22 stands for People & Blogs. Change as needed.
        },
        'status': {
            'privacyStatus': 'private'  # Change to public or unlisted if needed
        }
    }

    # Replace with the path to your video file
    video_file = file
    media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype='video/mp4')

    response_upload = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    ).execute()
    print(f'Video uploaded. Video ID: {response_upload["id"]}')

if __name__ == '__main__':
    youtube = get_authenticated_service()
    video_file_path = './workdir/separate_papers/relevant_papers.mp4'
    initialize_upload(youtube, video_file_path)
