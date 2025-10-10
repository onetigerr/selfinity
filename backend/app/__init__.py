# SPDX-License-Identifier: MIT

"""Application package bootstrap."""

import sys

import python_multipart.multipart as python_multipart_multipart

# Ensure legacy `multipart` import points at the modern python_multipart package.
sys.modules.setdefault("multipart", python_multipart_multipart)

