import os
import datetime
import logging
import random
import string

from config import RESOURCE_DIR, UPLOAD_DIR

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(threadName)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log(message: str):
    logging.info(message)

# Path validation to prevent traversal attacks
def validate_path(path: str) -> str:
    safe_path = os.path.normpath(path).lstrip("/")
    final_path = os.path.join(RESOURCE_DIR, safe_path)
    if not final_path.startswith(os.path.abspath(RESOURCE_DIR)):
        raise PermissionError("Forbidden path access")
    return final_path

# Generate unique filename for uploaded JSON
def generate_filename() -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    random_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    return f"upload_{timestamp}_{random_id}.json"

# Format date in RFC 7231
def rfc7231_date():
    now = datetime.datetime.utcnow()
    return now.strftime("%a, %d %b %Y %H:%M:%S GMT")
