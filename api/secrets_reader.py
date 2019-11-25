import os
from pathlib import Path


def secrets():
    secrets_path = _secrets_path()
    return {secret.name: open(str(secret), "r").read() for secret in Path(secrets_path).iterdir()}


def _secrets_path():
    try:
        return os.environ["VKS_SECRET_DEST_PATH"]
    except KeyError:
        raise EnvironmentError("Failed to import secrets: Environment variable VKS_SECRET_DEST_PATH is not set")

