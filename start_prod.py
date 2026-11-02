"""Lightweight single-port production server for Render Free Tier (512MB RAM)."""

import os

from reflex.reflex import _skip_compile
from reflex.utils import exec
from reflex_base import constants
from reflex_base.environment import environment


def main() -> None:
    environment.REFLEX_ENV_MODE.set(constants.Env.PROD)
    _skip_compile()
    port = int(os.environ.get("PORT", "8080"))
    exec.run_backend_prod(
        "0.0.0.0",
        port,
        constants.LogLevel.INFO,
        mount_frontend_compiled_app=True,
    )


if __name__ == "__main__":
    main()
