from scout_apm.api import Config  # type: ignore

from hermys.settings import get_settings

settings = get_settings()


def configure_scout_apm():
    Config.set(
        key=settings.SCOUT_KEY,
        name='Hermys API - FastAPI',
        monitor=True,
    )
