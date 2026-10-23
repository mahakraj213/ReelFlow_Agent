
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
USER_ID = os.getenv("INSTAGRAM_USER_ID")
print("Instagram User ID being used:", USER_ID)
VERSION = os.getenv("META_GRAPH_API_VERSION", "v25.0")
VIDEO_URL = os.getenv("IG_VIDEO_URL")

if not all([TOKEN, USER_ID, VIDEO_URL]):
    raise ValueError("Check your .env settings.")

url = f"https://graph.instagram.com/{VERSION}/{USER_ID}/media"

response = requests.post(
    url,
    headers={"Authorization": f"Bearer {TOKEN}"},
    data={
        "media_type": "REELS",
        "video_url": VIDEO_URL,
        "caption": (
            "Get started🎀 "
            "College, hostel life, gym, coding and internship dreams. "
            "#CSStudent #Life #getstarted"
        ),
        "share_to_feed": "true",
    },
    timeout=60,
)

print("HTTP status:", response.status_code)
print("Response:", response.text)
response.raise_for_status()

container_id = response.json().get("id")
if not container_id:
    raise RuntimeError("Instagram did not return a container ID.")

print("Reel container created:", container_id)
print("Nothing has been published yet.")
