from typing import NamedTuple
from dotenv import load_dotenv
from os import getenv as os_getenv


class ConfigAuth(NamedTuple):
    login: str
    password: str


class LoadEnv:
    def load(self):
        load_dotenv()

        EDUSITE_LOGIN = os_getenv("edusite_login")
        EDUSITE_PASSWORD = os_getenv("edusite_password")

        if EDUSITE_LOGIN is None or EDUSITE_PASSWORD is None:
            return

        return ConfigAuth(EDUSITE_LOGIN, EDUSITE_PASSWORD)
