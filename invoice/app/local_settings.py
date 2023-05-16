import os
import asyncio
import sys

# Local db
DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": "invoice",
        "USER": "postgres",
        "PASSWORD": "Use588mead@123",
        "HOST": "localhost".strip(),
        "PORT": "5432",
        "ATOMIC_REQUESTS": True,
    }
}