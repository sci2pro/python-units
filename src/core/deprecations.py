# -*- coding: utf-8 -*-
"""Deprecation helpers for compatibility APIs."""

from __future__ import annotations

import warnings
from collections.abc import Callable
from typing import TypeVar


_T = TypeVar("_T")


def warn_legacy_api(name: str, replacement: str, removal_version: str) -> None:
    """
    Emit a deprecation warning for a legacy public API.

    Args:
        name: Deprecated API name.
        replacement: Preferred API name or usage pattern.
        removal_version: Planned removal release.

    Returns:
        None.

    Raises:
        None.
    """
    warnings.warn(
        "{} is deprecated; use {} instead. It is scheduled for removal in {}.".format(
            name,
            replacement,
            removal_version,
        ),
        DeprecationWarning,
        stacklevel=4,
    )


def deprecated_call(
    name: str,
    replacement: str,
    removal_version: str,
    callback: Callable[[], _T],
) -> _T:
    """
    Warn for a deprecated API call and return the callback result.

    Args:
        name: Deprecated API name.
        replacement: Preferred API name or usage pattern.
        removal_version: Planned removal release.
        callback: Zero-argument callable that performs the actual work.

    Returns:
        The callback result.

    Raises:
        Any exception raised by ``callback``.
    """
    warn_legacy_api(name, replacement, removal_version)
    return callback()
