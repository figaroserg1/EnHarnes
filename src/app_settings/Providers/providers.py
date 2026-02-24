"""Cross-cutting providers entrypoint."""

from app_settings.Service.service import build_runtime_settings


def provide_feature_flags() -> dict:
    return {"feature_flags": ["settings-v1"], "seed": build_runtime_settings()}
