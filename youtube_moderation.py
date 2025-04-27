import os
import google.auth
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Define YouTube API Scopes

TOKEN_FILE = "token.json"

# Authenticate and get YouTube API client
def authenticate_youtube():
    """Authenticate and return a YouTube API client with a refresh token."""
    creds = None

    # Load existing credentials if available
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no valid credentials, perform authentication
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json", SCOPES
        )
        creds = flow.run_local_server(port=8080, access_type="offline", prompt="consent")  # ✅ Forces refresh token

        # ✅ Ensure refresh token is saved
        token_data = json.loads(creds.to_json())
        if "refresh_token" not in token_data:
            st.error("❌ Refresh token is missing! Try deleting 'token.json' and re-authenticating.")
            return None

        with open(TOKEN_FILE, "w") as token_file:
            json.dump(token_data, token_file, indent=4)

    return build("youtube", "v3", credentials=creds)

# Fetch comments from a video
def fetch_comments(youtube, video_id):
    """Fetch comments from a given YouTube video ID."""
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100  # Adjust limit as needed
        )
        response = request.execute()

        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comment_id = item["snippet"]["topLevelComment"]["id"]
            text = comment["textDisplay"]
            comments.append((comment_id, text))
            st.write(f"📝 **Found Comment:** {text} (ID: {comment_id})")

    except HttpError as e:
        st.error(f"❌ Error fetching comments: {e}")
    
    return comments

# Simple Harassment Detection (Can be replaced with ML/NLP)
def detect_harassment(comment_text):
    """Basic keyword-based harassment detection."""
    abusive_keywords = ["dumb", "hate", "stupid", "idiot", "trash"]
    return any(word in comment_text.lower() for word in abusive_keywords)

# Delete (Moderate) a comment
def delete_comment(youtube, comment_id):
    """Mark a comment as 'rejected' (deletes it from public view)."""
    try:
        youtube.comments().setModerationStatus(
            id=comment_id,
            moderationStatus="rejected"
        ).execute()
        st.success(f"✅ Successfully deleted comment (ID: {comment_id})")
    except HttpError as e:
        st.error(f"❌ Failed to delete comment (ID: {comment_id}): {e}")

# Streamlit UI
st.title("YouTube AI Comment Moderator: Smart Harassment Detection & Auto-Removal🚀")

# Authenticate YouTube API
st.write("🔑 **Authenticating YouTube API...**")
youtube = authenticate_youtube()

if youtube:
    st.success("✅ YouTube API Authentication Successful!")

    # Input for Video ID
    video_id = st.text_input("🎥 Enter YouTube Video ID:", "")

    if st.button("🔍 Fetch Comments"):
        if video_id:
            st.write(f"🔍 Fetching comments from video ID: {video_id}...")
            comments = fetch_comments(youtube, video_id)
            st.write(f"✅ **Fetched {len(comments)} comments.**")
        else:
            st.warning("⚠️ Please enter a valid YouTube Video ID.")

    if st.button("🕵️‍♂️ Detect & Remove Abusive Comments"):
        if video_id:
            st.write("🕵️‍♂️ **Detecting harassment in comments...**")
            comments = fetch_comments(youtube, video_id)
            for comment_id, text in comments:
                if detect_harassment(text):
                    st.warning(f"🚨 **Abusive Comment Detected:** {text} (ID: {comment_id})")
                    delete_comment(youtube, comment_id)
        else:
            st.warning("⚠️ Please enter a valid YouTube Video ID.")
