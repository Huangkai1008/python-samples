from typing import Any

from environs import Env

env = Env()
env.read_env(override=True)


def get_database_uri() -> Any:
    return env.str('SQLALCHEMY_URL')


def get_api_url() -> str:
    return f'http://{env.str("HOST")}:8000'
