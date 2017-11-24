from .base import *

import dj_database_url

ALLOWED_HOSTS = [os.environ.get('DOMAIN'), ]

db_from_env = dj_database_url.config(conn_max_age=500)

DATABASES['default'].update(db_from_env)

# Production storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Email setting
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.environ.get('SMTP_SERVER')

EMAIL_HOST_USER = os.environ.get('SMTP_USER')

EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASSWORD')

EMAIL_PORT = os.environ.get('SMTP_PORT', 587)

EMAIL_USE_TLS = os.environ.get('SMTP_USE_TTL', True)

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_SITE_EMAIL')

try:
    from .local import *
except ImportError:
    pass