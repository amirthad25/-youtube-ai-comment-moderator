from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import json
import os

# Define the required YouTube API scope

TOKEN_FILE = "token.json"

def authenticate_youtube():
    """Authenticate and authorize YouTube API access, ensuring a refresh token is included."""

    creds = None

    # Load existing token if available
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials, authenticate user
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
        creds = flow.run_local_server(port=8501, access_type="offline", prompt="consent")  # ✅ Forces refresh token

        # ✅ Ensure refresh token is saved
        token_data = json.loads(creds.to_json())
        if "refresh_token" not in token_data:
            print("❌ Refresh token is missing! Try deleting 'token.json' and re-authenticating.")
            return None  # Return None instead of exit(1) for better handling

        with open(TOKEN_FILE, "w") as token_file:
            json.dump(token_data, token_file, indent=4)

        print("✅ YouTube API Authentication Successful! Token saved.")

    return creds

if __name__ == "__main__":
    authenticate_youtube()
