#!/usr/bin/env python
# encoding: utf-8
# pylint: disable=wildcard-import,unused-wildcard-import
from .base import *

COMPRESS_ENABLED = False

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['vld.herokuapp.com']
