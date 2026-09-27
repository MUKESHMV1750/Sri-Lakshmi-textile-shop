"""
Fallback WSGI entry point for Render deployments.
Exposes `app` for Render's default start command: gunicorn app:app
"""

from config.wsgi import application as app
