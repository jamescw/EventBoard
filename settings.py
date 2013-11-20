import os

DEBUG = True

REDIS_URL = os.environ.get('REDISCLOUD_URL',
                           'redis://localhost:6379')
REDIS_CHANNEL = 'event'

JSONSCHEMA_DIR = os.path.join(
    os.path.dirname(__file__), 'schemas')