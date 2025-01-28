from django.contrib import admin
from clients.models.client import Client
from clients.models.deals import Deal
from clients.models.tasks import Task

admin.site.register(Client)
admin.site.register(Task)
admin.site.register(Deal)
