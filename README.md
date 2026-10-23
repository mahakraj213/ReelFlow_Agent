# Automated Instagram Reel Posting Agent

A small Python CLI that publishes a Reel to an Instagram **Business or Creator** account using Meta's official Graph API. It creates a media container, polls processing status, then publishes the container.

## What it does

1. Reads credentials from `.env` (never hard-code tokens).
2. Creates a Reel container with `media_type=REELS`.
3. Polls the container until `status_code=FINISHED`, or exits on an error/timeout.
4. Calls `/{ig-user-id}/media_publish`.
5. Prints the resulting Instagram media ID and useful API errors.

## Prerequisites

- An Instagram **Professional** account (Business or Creator).
- For the Facebook Login flow used here, the Instagram professional account must be linked to a Facebook Page.
- A Meta developer app configured for the Instagram Graph API.
- An access token with the required permissions approved/granted for the account, typically `instagram_basic`, `instagram_content_publish`, `pages_show_list`, and `pages_read_engagement` for the Facebook Login flow. Exact requirements depend on the app/login setup and current Meta documentation.
- Instagram account ID (`IG_USER_ID`) and an appropriate access token.
- A video hosted at a **publicly accessible HTTPS URL**. Meta fetches the video from its servers; a local path such as `./reel.mp4` will not work with this `video_url` flow.

Official references:
- Meta's Instagram API collection: https://www.postman.com/meta/instagram/documentation/6yqw8pt/instagram-api
- Meta content publishing docs: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/content-publishing/

## Setup

### 1. Create a virtual environment and install dependencies

Python 3.10+ recommended.

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 2. Configure credentials

```bash
cp .env.example .env
```

On Windows, copy `.env.example` to `.env` manually if `cp` is unavailable. Edit `.env` and replace the placeholders:

- `IG_USER_ID`: the Instagram professional account ID used by the API.
- `META_ACCESS_TOKEN`: your valid Meta access token.
- `META_GRAPH_API_VERSION`: API version enabled for your Meta app; default is `v25.0` in this sample. Change it if your app is pinned to another supported version.
- `IG_CAPTION`: optional default caption.

**Do not commit `.env`, paste tokens into chat, or include tokens in screenshots/submissions.** This project does not generate credentials or bypass Meta permissions.

### 3. Publish a Reel

```bash
python main.py --video-url "https://your-public-host.example/reel.mp4" \
  --caption "A new Reel! #reels"
```

Use the default caption in `.env` by omitting `--caption`:

```bash
python main.py --video-url "https://your-public-host.example/reel.mp4"
```

To avoid sharing the Reel to the main feed (if supported for your account/API version):

```bash
python main.py --video-url "https://your-public-host.example/reel.mp4" --no-feed
```

The script makes a **real publish request**. Test first with a suitable test account and video. There is no dry-run mode.

## Video and API notes

- Use a supported MP4/MOV video with compatible video/audio codecs, dimensions, frame rate, duration, and file size. Check the current Meta docs for limits before posting.
- The URL must be publicly reachable by Meta and remain available while processing.
- Video processing may take several minutes; the polling interval and timeout are configurable.
- Publishing may fail if the token is expired, permissions are missing, the account isn't professional/linked correctly, the API version is unavailable, or Meta's publishing limit is reached.
- If the script times out, inspect the container status in Meta before rerunning; don't blindly retry an uncertain publish.
- Keep API versions current and confirm exact permission requirements in Meta's official documentation.
- This is a CLI publisher, not a persistent scheduler. For scheduled posting, run it from cron/Task Scheduler or add a queue/worker and secure token management.

## Troubleshooting

- **OAuth/access token error**: generate a token for the correct app/account and verify required permissions.
- **Unsupported get request / invalid IG user ID**: confirm you are using the Instagram professional account ID, not a username or Facebook Page ID.
- **Invalid video URL**: open the URL in a private browser window to verify it is publicly reachable without cookies/login.
- **Container ERROR**: inspect the API's returned message and verify media format/limits.
- **Permission error**: ensure the app has the necessary permissions and, for non-role accounts, any required App Review / access level.

## Project structure

```text
instagram_reel_agent/
├── main.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Deadline hand-in checklist

- [ ] Install dependencies successfully.
- [ ] Configure your own Meta credentials in `.env`.
- [ ] Confirm the account is Business/Creator and linked to the right Facebook Page for this login flow.
- [ ] Verify the video URL is public and compatible.
- [ ] Publish a test Reel and save the terminal output with the token redacted.
- [ ] Include the repository/project files, not `.env`.
