🛡️ YouTube AI Comment Moderator
A smart YouTube comment moderation tool that uses keyword-based detection and Google’s YouTube Data API to fetch, analyze, and delete abusive or harassing comments automatically. Built using Streamlit, this application aims to promote respectful communication on digital platforms.

📌 Features
🔐 OAuth2 Authentication with YouTube API

🧠 Basic keyword-based harassment detection (upgradeable to ML/NLP)

📝 Fetches top-level comments from any public YouTube video

🚨 Detects and removes abusive comments using moderation APIs

🌐 Simple and interactive Streamlit UI

🧠 Tech Stack
Python

Streamlit – for interactive web interface

Google API Client Library – for YouTube Data API v3

OAuth 2.0 – for secure access with refresh token

NLTK / ML models – (optional for future upgrade)

🚀 How It Works
Authenticate using your Google account via OAuth2.

Enter a YouTube Video ID.

Click Fetch Comments to list recent comments.

Click Detect & Remove Abusive Comments to automatically moderate harmful content.

🛠️ Installation
Clone the repo:

bash
Copy
Edit
git clone https://github.com/your-username/youtube-ai-comment-moderator.git
cd youtube-ai-comment-moderator
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Add your client_secret.json (OAuth credentials from Google Cloud Console).

Run the app:

bash
Copy
Edit
streamlit run app.py
📂 File Structure
graphql
Copy
Edit
├── app.py                 # Main Streamlit app
├── token.json             # Generated after first authentication
├── client_secret.json     # Your Google OAuth credentials
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
🔐 Authentication Notes
First run will open a browser for Google sign-in.

Refresh token is stored securely in token.json.

🔮 Future Enhancements
Integrate ML models for toxic comment classification

Expand detection to support multiple languages

Add dashboard analytics and user control panel

Include comment replies in moderation flow

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to improve.
