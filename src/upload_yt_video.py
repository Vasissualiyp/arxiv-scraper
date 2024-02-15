import os
import google.oauth2.credentials
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
import json
from datetime import datetime
from configuration import extract_configuration

# Set up OAuth 2.0
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
#SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']
CLIENT_SECRETS_FILE = './config/credentials.json'
CREDENTIALS_PICKLE_FILE = './config/token.pickle'  # Path to save credentials

def list_video_categories(youtube):
    # Replace 'US' with your country code if necessary
    request = youtube.videoCategories().list(
        part="snippet",
        regionCode="US"
    )
    response = request.execute()

    for category in response["items"]:
        print(f'ID: {category["id"]} - Title: {category["snippet"]["title"]}')

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

def initialize_upload(title, description, youtube, file):
    body = {
        'snippet': {
            'title': f"{title}",
            'description': f"{description}",
            'tags': ['astrophysics', 'stars', 'numerical simulations'],
            'categoryId': '22'  # Category ID 14 stands for Science & Technology. Change as needed.
        },
        'status': {
            'privacyStatus': 'private'  # Change to public, private, or unlisted if needed
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

def generate_video_title_and_description(config):

    related_papers_json = config.RelatedPapersJson

    # Generate video title with today's date
    today_date = datetime.now().strftime("%Y-%m-%d")
    video_title = f"arXiv summary for {today_date}"

    # Load the related papers from the JSON file
    with open(related_papers_json, 'r') as file:
        related_papers = json.load(file)

    # Initialize the description with a header
    video_description = "Today's arXiv summaries include:\n\n"

    # Add each paper to the description
    for arxiv_id, paper_title in related_papers.items():
        # Assuming arxiv_id is enough to generate the link; adjust if the structure is different
        paper_link = f"https://arxiv.org/abs/{arxiv_id}"
        video_description += f"{paper_title}: {paper_link}\n\n"

    return video_title, video_description

def main_video_upload():
    
    # Extract configuration from ini file
    config = extract_configuration('config/config.ini')

    # Generate video title and description
    title, description = generate_video_title_and_description(config)

    video_file_path = config.OutputVideoFile
    youtube = get_authenticated_service()
    #list_video_categories(youtube)
    initialize_upload(title, description, youtube, video_file_path)

if __name__ == '__main__':
    main_video_upload()
