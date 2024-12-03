from config.settings import *

PINIT_API_TOKEN = os.getenv('PINIT_API_TOKEN', 'il tokeno')
PINIT_API_BASE_URL = os.getenv(
    'PINIT_API_BASE_URL', 'https://fake.api.pinit.ch'
)

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'TEST_CHARSET': 'UTF8',  # if your normal db is utf8
    'NAME': ':memory:',  # in memory
    'TEST_NAME': ':memory:',  # in memory
}
