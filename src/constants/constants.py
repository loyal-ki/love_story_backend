from pathlib import Path
from typing import Any

# version
VERSION = "0.0.1"

# App name
APP_NAME = "LoveStory"

# App description
APP_DESCRIPTION = "LoveStory is an app that helps couples create love stories!"

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Github repository
GIT_REPO_URL = "https://github.com/loyal-ki/love_story_backend"

# Default redis channel
EVENTS_CHANNEL = "events"

# Log server port
LOG_SERVER_PORT = 9020  # port for logserver in the worker

# Token type
TOKEN_TYPE = "Bearer"

# api version v1
API_V1 = "v1"


# api prefix
API_PREFIX = "/api/v1"


# Mail Subject
MAIL_SUBJECT = "LoveStory - Verify email"
