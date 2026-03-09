"""Development-specific settings."""
from .base import *  # noqa: F401, F403

DEBUG = True

INSTALLED_APPS = INSTALLED_APPS + ["debug_toolbar"]  # noqa: F405

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE  # noqa: F405

INTERNAL_IPS = ["127.0.0.1", "localhost"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "scrapy": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
