from config.settings import *  # noqa: F403, F401

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

SIMPLE_JWT["USER_AUTHENTICATION_RULE"] = lambda *args: True  # type: ignore # noqa: F405
