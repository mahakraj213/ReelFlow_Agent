
import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
VERSION = os.getenv("META_GRAPH_API_VERSION", "v25.0")

# Paste the container ID printed by test_reel_upload.py here
CONTAINER_ID = "18082572032367938"

url = f"https://graph.instagram.com/{VERSION}/{CONTAINER_ID}"

response = requests.get(
    url,
    headers={"Authorization": f"Bearer {TOKEN}"},
    params={"fields": "status_code,status"},
    timeout=30,
)

print("HTTP status:", response.status_code)
print("Response:", response.text)
response.raise_for_status()
