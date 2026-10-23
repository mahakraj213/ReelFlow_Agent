
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
VERSION = os.getenv("META_GRAPH_API_VERSION", "v25.0")

# Use the same container ID from check_reel_status.py
CONTAINER_ID = "18082572032367938"

url = f"https://graph.instagram.com/{VERSION}/me/media_publish"

response = requests.post(
    url,
    headers={"Authorization": f"Bearer {TOKEN}"},
    data={"creation_id": CONTAINER_ID},
    timeout=60,
)

print("HTTP status:", response.status_code)
print("Response:", response.text)
response.raise_for_status()

result = response.json()
print("Published Reel media ID:", result.get("id"))
