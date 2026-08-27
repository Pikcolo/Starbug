"""
Configuration module for Starbucks AI LINE Chatbot.
Loads settings from .env file and environment variables.
"""
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MENU_FILE_PATH = os.path.join(DATA_DIR, "starbucks_menu.json")

# Load environment variables from .env file
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

# LINE Bot API Credentials
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "").strip()
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "").strip()

# Flask Web Server Settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")

# Scraper Settings
SCRAPER_RATE_LIMIT_SECONDS = 1.0
SCRAPER_TIMEOUT = 10
STARBUCKS_BASE_URL = "https://www.starbucks.co.th"
STARBUCKS_MENU_URL = "https://www.starbucks.co.th/th/menu"
