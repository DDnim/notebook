"""
WSGI config for sites project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys  # 追加

from django.core.wsgi import get_wsgi_application

sys.path.append('/Users/sundongyang/WorkSpace/camelq')             # 追加
sys.path.append('/Users/sundongyang/WorkSpace/camelq/sites')   # 追加

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sites.settings")

application = get_wsgi_application()
