"""Test fixtures and import shims.

The ``omnirun`` SDK is not published to PyPI, so it cannot be installed in CI
or in a clean local environment. Every test in this suite already patches
``llama_index_tools_omnirun.tools.Sandbox`` with a ``MagicMock``, so the real
SDK is never exercised — we only need the ``omnirun`` module to be *importable*
so that ``from omnirun import Sandbox`` succeeds at module load time.

This installs a minimal stub module into ``sys.modules`` before the package
under test is imported. If the real ``omnirun`` package is installed, it is
left untouched.
"""

from __future__ import annotations

import sys
import types


def _install_omnirun_stub() -> None:
    if "omnirun" in sys.modules:
        return
    try:  # pragma: no cover - exercised only when the real SDK is present
        import omnirun  # noqa: F401

        return
    except ImportError:
        pass

    stub = types.ModuleType("omnirun")

    class Sandbox:  # noqa: D401 - stub stand-in for the real SDK class
        """Placeholder for omnirun.Sandbox; replaced by mocks in tests."""

        @classmethod
        def create(cls, *args: object, **kwargs: object) -> Sandbox:
            raise RuntimeError(
                "The omnirun stub Sandbox should never be created directly; "
                "tests must patch llama_index_tools_omnirun.tools.Sandbox."
            )

    stub.Sandbox = Sandbox
    sys.modules["omnirun"] = stub


_install_omnirun_stub()
