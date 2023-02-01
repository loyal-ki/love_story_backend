

import datetime
import logging
import re
import traceback
from decimal import Decimal
from logging.handlers import TimedRotatingFileHandler

from src.constants.constants import LOG_SERVER_PORT

import msgpack
from pydantic import BaseModel

# get exception message


def get_exception_message(exc: Exception):
    return "\n" + "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))


def timed_log_namer(default_name):
    base_filename, *ext, date = default_name.split(".")
    return f"{base_filename}{date}.{'.'.join(ext)}"


class MsgpackHandler(logging.handlers.SocketHandler):
    def __init__(self, host, port):
        logging.handlers.SocketHandler.__init__(self, host, port)

    def msgpack_encoder(self, obj):
        if isinstance(obj, BaseModel):
            return obj.dict()
        if isinstance(obj, datetime.datetime):
            return {"__datetime__": True, "data": obj.strftime("%Y%m%dT%H:%M:%S.%f")}
        if isinstance(obj, Decimal):
            return {"__decimal__": True, "data": str(obj)}
        return obj

    def makePickle(self, record):
        return msgpack.packb(record.__dict__, default=self.msgpack_encoder)


def configure_logserver(logserver_client_host):
    socket_handler = MsgpackHandler(logserver_client_host, LOG_SERVER_PORT)
    socket_handler.setLevel(logging.DEBUG)
    logger_client.addHandler(socket_handler)
    love_story_logger.addHandler(socket_handler)


logger_client = logging.getLogger("api.logclient")
love_story_logger = logging.getLogger("love_story")
logger_client.setLevel(logging.DEBUG)
love_story_logger.setLevel(logging.DEBUG)


def get_logger(name):
    return logger_client.getChild(name.replace("api.logclient.", ""))


def get_app_logger():
    return love_story_logger
