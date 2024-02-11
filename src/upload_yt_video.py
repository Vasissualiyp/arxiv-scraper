import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(file_name, title, description, category_id, keywords, privacy_status):
    # Disable OAuthlib's HTTPS verification when running locally.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    client_secrets_file = "./config/credentials.json"
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    # Manually creating the flow
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file,
        scopes=scopes,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    # Generate the authorization URL for manual visit
    auth_url, _ = flow.authorization_url(prompt='consent')

    print("Please go to this URL and authorize access:", auth_url)
    code = input("Enter the authorization code: ")
    flow.fetch_token(code=code)

    credentials = flow.credentials
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": category_id,
                "description": description,
                "title": title,
                "tags": keywords.split(",")
            },
            "status": {
                "privacyStatus": privacy_status
            }
        },
        media_body=googleapiclient.http.MediaFileUpload(file_name)
    )
    response = request.execute()

    print("Upload successful. Response:", response)



if __name__ == "__main__":
    file_name = "./workdir/separate_papers/relevant_papers.mp4"
    title = "Test title"
    description = "Test description"
    category_id = "22"  # See https://developers.google.com/youtube/v3/docs/videoCategories/list
    keywords = "keyword1,keyword2,keyword3"
    privacy_status = "private"  # or "private" or "unlisted"

    upload_video(file_name, title, description, category_id, keywords, privacy_status)

