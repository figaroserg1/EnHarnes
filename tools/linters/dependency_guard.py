#!/usr/bin/env python3
import os
import sys

# запрещаем infra -> domain
FORBIDDEN = ("infra", "domain")


def check(path: str) -> bool:
    with open(path, "r", errors="ignore", encoding="utf-8") as f:
        text = f.read()
    if "from infra" in text and "domain" in path:
        print(f"[DEPENDENCY] forbidden import in {path}")
        return False
    return True


def walk() -> bool:
    ok = True
    if not os.path.isdir("src"):
        print("[DEPENDENCY] src directory not found; skipping check")
        return ok

    for root, _, files in os.walk("src"):
        for name in files:
            if name.endswith(".py"):
                if not check(os.path.join(root, name)):
                    ok = False
    return ok


if __name__ == "__main__":
    if not walk():
        sys.exit(1)
