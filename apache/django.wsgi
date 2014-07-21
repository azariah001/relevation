import os
import os.path
import sys

sys.path.append('/var/www/django')
sys.path.append('/var/www/django/relevation')

os.environ['PYTHON_EGG_CACHE'] = '/var/www/django/egg_cache'
os.environ['DJANGO_SETTINGS_MODULE'] = 'relevation.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

//test edit
//second user edit