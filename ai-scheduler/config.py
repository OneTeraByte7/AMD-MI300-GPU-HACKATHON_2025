# config.py

import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# vLLM/OpenAI Server Configuration
BASE_URL = "http://129.212.177.3:8000/v1"  # vLLM server public IP and port
MODEL_PATH = "qwen2.5-7b"  # Served model name for Qwen2.5-7B-Instruct
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "abc-123")

# Google Calendar API
GOOGLE_SCOPES = ["https://www.googleapis.com/auth/calendar"]
KEYS_DIR = os.environ.get("KEYS_DIR", "./Keys")

# Flask App
FLASK_HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.environ.get("FLASK_PORT", 5000))

# Scheduler
SCHEDULER_API_ENABLED = True

# Other constants
DEFAULT_TIMEZONE = os.environ.get("DEFAULT_TIMEZONE", "Asia/Kolkata")
DEFAULT_MEETING_DURATION = int(os.environ.get("DEFAULT_MEETING_DURATION", "30"))  # in minutes

# Add any additional configuration constants as needed
