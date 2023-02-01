import os
import sys

from migrate.versioning.shell import main
from migrate.exceptions import DatabaseAlreadyControlledError, DatabaseNotControlledError

path = os.path.join(os.path.dirname(__file__), '../')
sys.path.append(path)

from src.config import config

if __name__ == '__main__':
    try:
        main(
            debug='False',
            url=config.DATABASE_URL,
            repository='.'
        )
        print("[INFO] Successfully completed.")
    except DatabaseAlreadyControlledError:
        print("[WARNING] The database has already been initialized.")
        print("[INFO] Successfully completed.")
    except DatabaseNotControlledError:
        print("[ERROR] The database has not been initialized.")
        exit(1)
    except Exception as err:
        print(f"[ERROR] {err}")
        exit(1)