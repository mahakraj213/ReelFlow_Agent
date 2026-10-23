from unittest.mock import patch
from main import InstagramReelPublisher

def test_container_status_and_publish_flow():
    publisher = InstagramReelPublisher("123", "secret", "v25.0")
    with patch.object(publisher, "_request") as request:
        request.side_effect = [
            {"id": "container-1"},
            {"status_code": "IN_PROGRESS", "status": "Processing"},
            {"status_code": "FINISHED", "status": "Ready"},
            {"id": "media-1"},
        ]
        with patch("main.time.sleep"):
            media_id = publisher.publish_reel(
                "https://example.com/reel.mp4", "caption",
                poll_interval=5, max_wait_seconds=30
            )
    assert media_id == "media-1"
    assert request.call_count == 4
