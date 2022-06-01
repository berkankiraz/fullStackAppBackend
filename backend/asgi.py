"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

"""
asgi.py allows for an optional Asynchronous Server Gateway Interface to run. 
wsgi.py which stands for Web Server Gateway Interface helps Django serve our web pages. 
Both files are used when deploying our app. We will revisit them later when we deploy our app.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_asgi_application()
