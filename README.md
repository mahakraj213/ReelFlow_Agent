# ReelFlow_Agent
This is a functional script/agent that programmatically publishes a video Reel to an Instagram Business account using the official Meta Graph API.
# Automated Instagram Reel Posting Agent

## 1. Project Overview

The **Automated Instagram Reel Posting Agent** is a Python-based project that uses the Instagram API to automate the process of publishing Instagram Reels.

The application connects to an Instagram Creator account, uploads a video using a publicly accessible video URL, checks the video processing status, and publishes the Reel to the account.

This project demonstrates API integration, environment variable management, HTTP requests, error handling, and automation using Python.

## 2. Objectives

- Connect a Python application to the Instagram API.
- Authenticate requests using an Instagram access token.
- Create a media container for a Reel.
- Check whether the video has finished processing.
- Publish the Reel through the API.
- Keep credentials separate from the source code.

## 3. Technologies Used

- **Programming language:** Python
- **API:** Instagram API with Instagram Login
- **HTTP requests:** `requests`
- **Environment configuration:** `python-dotenv`
- **Development environment:** Visual Studio Code

## 4. Project Workflow

1. Load the Instagram access token and configuration from the `.env` file.
2. Verify the API connection and retrieve the Instagram account details.
3. Send the video URL and caption to the Instagram API to create a Reel media container.
4. Check the container status until video processing is complete.
5. Publish the processed Reel using its container ID.
6. Verify the published Reel on the Instagram profile.

## 5. Project Structure

```text
AI project/
├── .env                    # Private credentials; do not submit
├── .env.example            # Example configuration with placeholders
├── .gitignore              # Excludes secrets and temporary files
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── test_connection.py      # Tests the API connection
├── test_reel_upload.py     # Creates a Reel media container
├── check_reel_status.py    # Checks video processing status
└── publish_reel.py         # Publishes the Reel
```

Additional video files may be stored locally for testing.

## 6. Prerequisites

Before running the project, ensure you have:

- Python installed.
- An Instagram account eligible for the required API functionality.
- An app configured for Instagram API with Instagram Login.
- A valid Instagram access token with the necessary permissions.
- A publicly accessible video URL supported by the API.
- Internet connectivity.

## 7. Installation and Setup

### Step 1: Install dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

### Step 2: Configure environment variables

Create a `.env` file based on `.env.example` and enter your own valid credentials and video URL.

Example `.env.example`:

```env
INSTAGRAM_ACCESS_TOKEN=your_access_token_here
INSTAGRAM_USER_ID=your_instagram_user_id_here
META_GRAPH_API_VERSION=v25.0
IG_VIDEO_URL=https://example.com/your-video.mp4
```

Replace the example values with valid configuration values before running the application. The video URL must point to a publicly accessible video file that meets Instagram's media requirements.

**Security note:** Never commit your real `.env` file or expose your access token in screenshots, source control, or project documentation.

### Step 3: Test the connection

```bash
python test_connection.py
```

Confirm that the API returns the expected Instagram account information.

## 8. Running the Application

### Create a Reel container

```bash
python test_reel_upload.py
```

This sends the video URL and caption to the API and creates a media container. It does not publish the Reel.

Save the returned container ID for the following steps.

### Check processing status

```bash
python check_reel_status.py
```

Use the container ID returned by the upload step. Wait until the API reports that processing is complete (`FINISHED`).

### Publish the Reel

```bash
python publish_reel.py
```

Use the same container ID. A successful API response should return the published media ID. Verify the Reel on the Instagram profile.

**Note:** The current scripts are run manually in sequence. Scheduled or unattended posting would require additional scheduling, status polling, and error-recovery logic.

## 9. Error Handling and Troubleshooting

- **HTTP 400:** Check the endpoint, account ID, request parameters, video URL, and permissions.
- **Authentication errors:** Verify that the access token is valid and has the required permissions.
- **Processing errors:** Check the video format, accessibility, and API status response.
- **Container still processing:** Wait before attempting to publish.
- **Missing configuration:** Confirm that the `.env` file exists and that variable names match the Python code.

Avoid printing or sharing access tokens when troubleshooting.

## 10. Results

The project successfully demonstrated the following workflow:

- Connected to the configured Instagram Creator account.
- Created a Reel media container using a video URL.
- Confirmed that the container reached the `FINISHED` status.
- Published the Reel through the Instagram API.
- Verified that the Reel appeared on the Instagram profile.

## 11. Future Enhancements

- Add automatic scheduling for posts.
- Implement retry logic and structured logging.
- Add automated processing-status polling.
- Store publishing history and error reports.
- Support multiple videos and captions through a queue.
- Add notifications after successful or failed publishing.

## 12. Conclusion

This project demonstrates how Python can integrate with the Instagram API to automate Reel publishing. It provides practical experience with API authentication, HTTP requests, media processing workflows, environment configuration, and error handling.

The project can be extended into a scheduled content-publishing system with additional automation and monitoring features.

