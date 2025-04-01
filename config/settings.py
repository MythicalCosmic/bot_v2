import os
import logging
from dotenv import load_dotenv
import yaml

load_dotenv(override=True)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
ADMINS_GROUP_ID = os.getenv("ADMINS_GROUP_ID")

CLICK_TOKEN = os.getenv("CLICK_TOKEN")
PAYME_TOKEN = os.getenv("PAYME_TOKEN")

LINK_CHANNEL_ID = os.getenv("LINK_CHANNEL_ID")

SOURCE_CHANNEL_ID = os.getenv("SOURCE_CHANNEL_ID")
VIDEO_MESSAGE_ID = os.getenv("VIDEO_MESSAGE_ID")
PDF_MESSAGE_ID = os.getenv("PDF_MESSAGE_ID")

TIMEZONE = os.getenv("TIMEZONE")

WEBHOOK = os.getenv("WEBHOOK", "False").lower() == "true"
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")


DEBUG = os.getenv("DEBUG", "True").lower() == "true"
DEBUG_LEVEL = os.getenv("DEBUG_LEVEL", "info").upper()


LOG_DIR = "requests"
LOG_FILE = f"{LOG_DIR}/request.log"


os.makedirs(LOG_DIR, exist_ok=True)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  
LANGUAGES_FILE = os.path.join(BASE_DIR, "languages", "uz.yaml")

with open(LANGUAGES_FILE, "r", encoding="utf-8") as file:
    LANGUAGES = yaml.safe_load(file)

    
BOT_LANGUAGE = "uz"

def get_translation(key: str, language: str = BOT_LANGUAGE) -> str:
    
    return LANGUAGES.get(language, LANGUAGES["uz"]).get(key, key)


logging.basicConfig(
    level=getattr(logging, DEBUG_LEVEL, logging.INFO),
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ],
)

logging.info("Configuration loaded successfully.")
