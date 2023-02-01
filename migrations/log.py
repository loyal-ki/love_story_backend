import sys
import logging

LOG = logging.getLogger("api_migration")
LOG.propagate = False
LOG_FORMAT = '[%(levelname)s] %(message)s'
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(LOG_FORMAT)
stream_handler.setFormatter(formatter)
LOG.addHandler(stream_handler)