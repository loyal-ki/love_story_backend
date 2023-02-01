import asyncio
import logging
import re
from contextvars import ContextVar

from sqlalchemy.orm import sessionmaker
from pydantic import BaseSettings, Field, validator
from starlette.config import Config

from src.constants.constants import APP_NAME
from src.utils.files import ensure_exists
from src.utils.logger import configure_logserver, get_exception_message, get_logger
from src.config.config import DOCKER_ENV

# App settings
class Settings(BaseSettings):
    # log file
    log_file: str = None

    # log file redex
    log_file_regex: re.Pattern = None

    # app config
    config: Config = None

    # app logger
    logger: logging.Logger = None

    # plugins
    plugins: list = None

    # plugins schema
    plugins_schema: dict = {}

    # env config
    class Config:
        env_file = "conf/.env"

    @property
    def logserver_client_host(self) -> str:
        return "worker" if DOCKER_ENV else "localhost"

    # initial settings
    def __init__(self, **data):
        super().__init__(**data)
        self.config = Config("conf/.env")

    async def init(self):
        asyncio.get_running_loop().set_exception_handler(
            lambda *args, **kwargs: handle_exception(self, *args, **kwargs))

    async def shutdown(self):
        pass

    def init_logging(self, worker=True):
        if worker:
            configure_logserver(self.logserver_client_host)
        self.logger = get_logger(__name__)

    @property
    def connection_str(self):
        return


# handle exception
def handle_exception(settings, loop, context):
    if "exception" in context:
        msg = get_exception_message(context["exception"])
    else:
        msg = context["message"]
    settings.logger.error(msg)


# init
async def init():
    settings = settings_ctx.get()
    await settings.init()

settings_ctx = ContextVar("settings")


# get attribute by name
def __getattr__(name):
    if name == "settings":
        return settings_ctx.get()
    raise AttributeError(f"module {__name__} has no attribute {name}")
