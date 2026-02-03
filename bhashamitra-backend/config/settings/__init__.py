"""Settings initialization."""
import os

environment = os.getenv('DJANGO_ENV', 'dev')

# Also use prod settings if DATABASE_URL is present (Render/Heroku style)
database_url = os.getenv('DATABASE_URL')

if environment == 'prod' or database_url:
    from .prod import *
else:
    from .dev import *
