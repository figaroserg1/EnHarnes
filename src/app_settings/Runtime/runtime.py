"""Runtime composition layer."""

from app_settings.Service.service import build_runtime_settings


def get_runtime_payload() -> dict:
    return {"runtime": build_runtime_settings()}
