"""Compatibility shim so tests can import python_multipart.multipart.

The real package installed via pip is `python-multipart`, which exposes the
module `multipart`. This shim makes `python_multipart.multipart` importable by
re-exporting from `multipart`.
"""

from .multipart import *  # noqa: F401,F403
