"""
Main entry point for Django on Vercel.
This file wraps Django's WSGI application for Vercel's Python runtime.
"""

import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('USE_SQLITE', 'true')  # Use SQLite for development

# Initialize Django
import django
django.setup()

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Create the WSGI app
app = get_wsgi_application()

# For Vercel, we need to export the app
application = app
