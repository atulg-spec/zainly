import sys
import os
import django
from django.core.wsgi import get_wsgi_application

# Set your project's settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'zainly.settings'

# Add your project directory to the PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Django setup
django.setup()

# Get the WSGI application for the Django project
application = get_wsgi_application()
