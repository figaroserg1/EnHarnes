"""UI layer adapters."""

from app_settings.Runtime.runtime import get_runtime_payload


def render_payload() -> dict:
    return {"ui": get_runtime_payload()}
