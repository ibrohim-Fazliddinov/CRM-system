# Это гарантирует, что приложение всегда импортируется при запуске
# Django, так что shared_task будет использовать это приложение.
from common.celery import app as celery_app

__all__ = ('celery_app',)