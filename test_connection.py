import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")

print("Token found:", bool(token))
print("Token length:", len(token))
print("Looks like placeholder:", "your_" in token.lower())

url = "https://graph.instagram.com/v25.0/me"

response = requests.get(
    url,
    headers={"Authorization": f"Bearer {token}"},
    params={"fields": "user_id,username"},
    timeout=30,
)

print("HTTP status:", response.status_code)
print("Response:", response.text)

