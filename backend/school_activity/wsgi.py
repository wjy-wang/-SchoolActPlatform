import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_activity.settings')

try:
    from django.conf import settings
    LOG_DIR = settings.LOG_DIR
    LOG_DIR.mkdir(exist_ok=True)
except Exception as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"无法创建日志目录: {e}")

application = get_wsgi_application()
