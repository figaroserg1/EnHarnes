"""Service layer for app settings."""

from Repo.repository import load_settings_record


def build_runtime_settings() -> dict:
    return {"settings": load_settings_record(), "validated": True}
