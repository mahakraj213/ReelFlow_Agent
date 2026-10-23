#!/usr/bin/env python3
"""Publish an Instagram Reel using Meta's official Graph API (Facebook Login flow)."""
import argparse
import os
import sys
import time
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

GRAPH_BASE = "https://graph.instagram.com"


class MetaAPIError(RuntimeError):
    pass


def env_required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise MetaAPIError(f"Missing required environment variable: {name}")
    return value


class InstagramReelPublisher:
    def __init__(self, ig_user_id: str, access_token: str, api_version: str = "v25.0",
                 timeout: int = 60):
        self.ig_user_id = ig_user_id
        self.access_token = access_token
        self.base_url = f"{GRAPH_BASE}/{api_version}"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "instagram-reel-agent/1.0"})

    def _request(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        params = kwargs.pop("params", {})
        # Use Bearer auth rather than putting the token in logs/URLs.
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"
        try:
            response = self.session.request(
                method, url, params=params, headers=headers,
                timeout=self.timeout, **kwargs
            )
        except requests.RequestException as exc:
            raise MetaAPIError(f"Network error calling Meta API: {exc}") from exc

        try:
            payload = response.json()
        except ValueError:
            payload = {"raw_response": response.text[:1000]}

        if not response.ok or "error" in payload:
            error = payload.get("error", {})
            message = error.get("message") or payload.get("raw_response") or response.reason
            code = error.get("code")
            subcode = error.get("error_subcode")
            details = f" (code={code}, subcode={subcode})" if code is not None else ""
            raise MetaAPIError(f"Meta API error{details}: {message}")
        return payload

    def create_reel_container(self, video_url: str, caption: str, share_to_feed: bool = True) -> str:
        data = self._request(
            "POST", f"{self.ig_user_id}/media",
            data={
                "media_type": "REELS",
                "video_url": video_url,
                "caption": caption,
                "share_to_feed": str(share_to_feed).lower(),
            },
        )
        container_id = data.get("id")
        if not container_id:
            raise MetaAPIError(f"Meta did not return a container ID: {data}")
        print(f"Created Reel container: {container_id}")
        return str(container_id)

    def wait_until_ready(self, container_id: str, poll_interval: int = 15,
                         max_wait_seconds: int = 600) -> None:
        """Poll until FINISHED; stop on error/expiry or timeout."""
        deadline = time.monotonic() + max_wait_seconds
        while time.monotonic() < deadline:
            data = self._request(
                "GET", container_id,
                params={"fields": "status_code,status"},
            )
            status = str(data.get("status_code", "UNKNOWN")).upper()
            description = data.get("status", "")
            print(f"Container status: {status}" + (f" — {description}" if description else ""))
            if status == "FINISHED":
                return
            if status in {"ERROR", "EXPIRED", "PUBLISHED"}:
                raise MetaAPIError(
                    f"Container cannot be published (status={status}). "
                    f"Meta status: {description or 'no additional details'}"
                )
            time.sleep(min(poll_interval, max(0, deadline - time.monotonic())))
        raise MetaAPIError(
            f"Timed out after {max_wait_seconds}s waiting for the Reel container. "
            "Check the container status in Meta and retry only after confirming its state."
        )

    def publish(self, container_id: str) -> str:
        data = self._request(
            "POST", f"{self.ig_user_id}/media_publish",
            data={"creation_id": container_id},
        )
        media_id = data.get("id")
        if not media_id:
            raise MetaAPIError(f"Meta did not return a published media ID: {data}")
        return str(media_id)

    def publish_reel(self, video_url: str, caption: str, share_to_feed: bool = True,
                     poll_interval: int = 15, max_wait_seconds: int = 600) -> str:
        container_id = self.create_reel_container(video_url, caption, share_to_feed)
        self.wait_until_ready(container_id, poll_interval, max_wait_seconds)
        media_id = self.publish(container_id)
        print(f"Published successfully. Instagram media ID: {media_id}")
        return media_id


def parse_args():
    parser = argparse.ArgumentParser(
        description="Publish a Reel to an Instagram Professional account using Meta Graph API."
    )
    parser.add_argument("--video-url", required=True,
                        help="Publicly accessible HTTPS URL to an MP4/MOV video.")
    parser.add_argument("--caption", default="",
                        help="Caption text. If omitted, IG_CAPTION from .env is used.")
    parser.add_argument("--no-feed", action="store_true",
                        help="Keep the Reel off the profile feed where supported.")
    parser.add_argument("--poll-interval", type=int, default=15,
                        help="Seconds between container status checks (default: 15).")
    parser.add_argument("--max-wait", type=int, default=600,
                        help="Maximum seconds to wait for processing (default: 600).")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        ig_user_id = env_required("IG_USER_ID")
        access_token = env_required("META_ACCESS_TOKEN")
        api_version = os.getenv("META_GRAPH_API_VERSION", "v25.0").strip()
        caption = args.caption if args.caption else os.getenv("IG_CAPTION", "")
        publisher = InstagramReelPublisher(ig_user_id, access_token, api_version)
        publisher.publish_reel(
            video_url=args.video_url,
            caption=caption,
            share_to_feed=not args.no_feed,
            poll_interval=max(5, args.poll_interval),
            max_wait_seconds=max(30, args.max_wait),
        )
        return 0
    except MetaAPIError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
