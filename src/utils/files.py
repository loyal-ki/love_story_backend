import os

# remove file by name
def safe_remove(filename):
    try:
        os.remove(filename)
    except (TypeError, OSError):
        pass

# ensure exists path
def ensure_exists(path):
    os.makedirs(path, exist_ok=True)
