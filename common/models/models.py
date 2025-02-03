from crum import get_current_user
from django.db import models
class BaseModel(models.Model):
    class Meta:
        abstract = True