"""Repository access layer."""

from Config.settings import CONFIG_SCHEMA


def load_settings_record() -> dict:
    return {"schema": CONFIG_SCHEMA, "source": "stub-repo"}
