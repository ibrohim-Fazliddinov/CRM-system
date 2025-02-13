import os
from celery import Celery

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE, если она не задана
# Это необходимо, чтобы Celery мог получить доступ к настройкам Django
os.environ.setdefault(key='DJANGO_SETTINGS_MODULE', value='config.settings')

# Создаем объект Celery и даем ему имя 'config'
# Это имя используется для организации задач в рамках приложения
app = Celery('config')

# Загружаем конфигурацию Celery из настроек Django
# Здесь 'django.conf:settings' указывает, что настройки берутся из Django
# 'namespace' определяет префикс, который используется для всех переменных, связанных с Celery
# Например, если в Django settings указано CELERY_BROKER_URL, Celery сможет его найти
app.config_from_object(obj='django.conf:settings', namespace='CELERY')

# Автоматически находит и загружает задачи (tasks) из установленных приложений Django
# Celery ищет модуль model_tk.py в каждом зарегистрированном приложении
app.autodiscover_tasks()