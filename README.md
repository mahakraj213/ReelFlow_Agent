# Automated Instagram Reel Posting Agent

A Python-based project that automates publishing Instagram Reels using the Meta Instagram API.

## Features
- Connects to an Instagram Creator/ business account using the API.
- Uploads video media and checks its processing status.
- Publishes the Reel to Instagram.

## Requirements
- Python 3.13.9
- An Instagram Creator account configured for API access
- A valid Meta access token and Instagram User ID

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/mahakraj213/ReelFlow_Agent.git
   cd ReelFlow_Agent
   ```

2. Create and activate a virtual environment (recommended):

   **Windows:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example` and configure:

   ```env
   IG_USER_ID=your_instagram_user_id
   META_ACCESS_TOKEN=your_meta_access_token
   ```

## Run the Project

Place your video file in the project folder and run the main script:

```bash
python main.py
```

Follow any prompts or configuration required by the script.

## Security

The `.env` file should remain excluded from version control.

## Mahak Raj

Developed as an internship project to demonstrate Instagram Reel publishing automation using Python and the Meta Instagram API.
