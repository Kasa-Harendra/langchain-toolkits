from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = []

class CalendarClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        access_token: str,
        refresh_token: str
    ): 
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.access_token: str = access_token
        self.refresh_token: str = refresh_token
        
        self.service = build(
            "calendar",
            "v3",
            credentials= Credentials(
                token = self.access_token,
                refresh_token = self.refresh_token,
                client_id = self.client_id,
                client_secret = self.client_secret,
                token_uri = "https://oauth2.googleapis.com/token",
                scopes=SCOPES
            )
        )
        
    @staticmethod
    def get_client_using_refresh_token(
        client_id: str,
        client_secret: str,
        refresh_token: str 
    ):
        creds = Credentials(
            token = None,
            refresh_token = refresh_token,
            client_id = client_id,
            client_secret = client_secret,
            token_uri = "https://oauth2.googleapis.com/token",
            scopes=SCOPES
        )
        
        creds.refresh(Request())
        
        return CalendarClient(
            client_id=client_id,
            client_secret=client_secret,
            access_token=creds.token,
            refresh_token=refresh_token
        )