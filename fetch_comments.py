from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import joblib  # To load your trained harassment detection model

# Load your OAuth credentials (replace with actual file path)
creds = Credentials.from_authorized_user_file("client_secret.json")

# Initialize YouTube API client
youtube = build("youtube", "v3", credentials=creds)

# Your specific video ID
VIDEO_ID = "s-wmkqxDKPQ"

# Load your trained harassment detection model
model = joblib.load("harassment_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Function to fetch comments from the given video
def get_comments(video_id):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100  # Fetch up to 100 comments
    )
    response = request.execute()

    comments = []
    for item in response.get("items", []):
        comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comment_id = item["snippet"]["topLevelComment"]["id"]
        comments.append((comment_id, comment_text))

    return comments

# Function to detect harassment
def detect_harassment(comments):
    for comment_id, text in comments:
        text_vectorized = vectorizer.transform([text])  # Convert to numerical format
        prediction = model.predict(text_vectorized)[0]  # Predict harassment (0 = Safe, 1 = Harassment)
        
        if prediction == 1:
            print(f"⚠️ Harassment Detected: {text}")
            delete_comment(comment_id)

# Function to delete a comment (Requires correct YouTube Data API permissions)
def delete_comment(comment_id):
    try:
        youtube.comments().delete(id=comment_id).execute()
        print(f"🗑️ Deleted Comment ID: {comment_id}")
    except Exception as e:
        print(f"❌ Failed to delete comment: {e}")

# Execute: Fetch comments, analyze, and delete if necessary
comments = get_comments(VIDEO_ID)
detect_harassment(comments)
