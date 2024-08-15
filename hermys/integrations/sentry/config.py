import sentry_sdk

from hermys.settings import get_settings

settings = get_settings()


def configure_sentry():
    sentry_sdk.init(
        dsn=settings.SENTRY_DNS,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
