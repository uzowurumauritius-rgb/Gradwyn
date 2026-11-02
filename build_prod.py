"""Pre-compile and build the Reflex production static frontend at Docker build time."""

from pathlib import Path

from reflex.reflex import _compile_app, _init
from reflex.utils import build, prerequisites
from reflex_base import constants, environment
from reflex_base.config import get_config


def main() -> None:
    environment.REFLEX_ENV_MODE.set(constants.Env.PROD)
    config = get_config()
    if prerequisites.needs_reinit():
        _init(name=config.app_name)
    _compile_app(avoid_dirty_check=False)
    build.setup_frontend_prod(Path.cwd())
    print("Production frontend bundle built successfully in .web/_static!")


if __name__ == "__main__":
    main()
