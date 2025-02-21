import os
from src.ecsapi import __initialize_env_file

_ = __initialize_env_file


def test___initialize_env_file():
    assert os.getenv("ECSAPI_ENV_FILE") is not None
