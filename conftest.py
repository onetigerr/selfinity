"""
Root-level pytest configuration to ensure async tests run from repo root.

- Extends sys.path with backend/.venv site-packages if present
- Loads pytest-asyncio plugin so async def tests execute instead of skipping

This avoids requiring global installation of pytest-asyncio and preserves
the ability to simply run `pytest` from the project root.
"""
from __future__ import annotations

import sys
from pathlib import Path


def _extend_sys_path_with_backend_venv() -> None:
    root = Path(__file__).resolve().parent
    # POSIX venv layout
    posix_site = root / "backend" / ".venv" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
    # Windows venv layout
    win_site = root / "backend" / ".venv" / "Lib" / "site-packages"
    for site in (posix_site, win_site):
        if site.exists():
            sys.path.insert(0, str(site))
            break


_extend_sys_path_with_backend_venv()

# Ensure pytest-asyncio is loaded if available on sys.path (from backend venv)
pytest_plugins = ("pytest_asyncio",)

