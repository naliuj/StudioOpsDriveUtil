import json
import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError


class GoogleDriveTools:

    teamDriveID = None
    SCOPES = ["https://www.googleapis.com/auth/drive"]
    creds = None
    apiService = None

    def __init__(self, team_drive_id):
        # self.apiService = service
        self.teamDriveID = team_drive_id

        self.authenticate()

    def authenticate(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

        if not self.creds or not self.creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', self.SCOPES)
            self.creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(self.creds.to_json())

        # Create a Google Drive API service
        self.apiService = build('drive', 'v3', credentials=self.creds)

    def get_files(self, folder_id):
        try:
            results = self.apiService.files().list(
                q=f"'{folder_id}' in parents and trashed = false",
                includeTeamDriveItems=True,
                supportsAllDrives=True,
                supportsTeamDrives=True,
                corpora='drive',
                teamDriveId=self.teamDriveID,
                fields="files(id, name, webViewLink)").execute()
            files = results.get('files', [])
            return files
        except HttpError as error:
            print(f"An error occurred: {error}")

    def get_folder_name(self, folder_id):
        try:
            folder = self.apiService.files().get(
                fileId=folder_id,
                fields="name",
                supportsTeamDrives=True).execute()
            return folder['name']
        except HttpError as error:
            print(f"An error occurred: {error}")

    def get_active_rooms(self, studio_logs):
        active_rooms = []
        for room in studio_logs:
            if self.get_files(room):
                active_rooms.append(room)
        return active_rooms

    def rename_file(self, file_id, new_name):
        file_metadata = {
            'name': new_name,
            'teamDriveId': self.teamDriveID,  # Include the team drive ID as the driveId
            'supportsAllDrives': True,  # Set this to True to access files in shared drives
            'supportsTeamDrives': True
        }
        try:
            updated_file = self.apiService.files().update(fileId=file_id,
                                                          body=file_metadata,
                                                          supportsAllDrives=True,
                                                          supportsTeamDrives=True).execute()
            print(file_id + " renamed successfully")
        except Exception as e:
            print("An error occurred:", str(e))
            if isinstance(e, HttpError):
                error_response = json.loads(e.content)
                print("Error details:", error_response)
