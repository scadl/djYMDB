"""
WSGI config for djYMDB project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
'''
import sys
DJANGO_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..')
sys.path.append(DJANGO_PATH)
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),'../venv/Scripts'))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),'../venv/Lib/site-packages'))
activate_this = os.path.join(os.path.abspath(os.path.dirname(__file__)),'../venv/scripts/activate_this.py')
exec(open(activate_this).read())
'''

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djYMDB.settings')

application = get_wsgi_application()
