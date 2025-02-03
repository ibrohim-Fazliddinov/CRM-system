from django.contrib import admin
from clients.models.client import Client
from clients.models.deals import Deal
from clients.models.tasks import Task

class AdminMixin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'created_by', 'updated_by', 'updated_at',)

# Inline для задач, связанных с клиентом
class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ('name', 'status_task', 'due_date', 'priority', 'manager')
    readonly_fields = ('created_by', 'created_at',)  # можно добавить, если какие-то поля должны быть только для чтения

@admin.register(Client)
class ClientAdmin(AdminMixin):
    list_display = ('pk', 'email', 'company', 'manager', 'is_active_client')
    search_fields = ('email', 'name', 'company')
    list_filter = ('is_active_client', 'manager')
    inlines = [TaskInline]  # чтобы видеть задачи, связанные с клиентом

@admin.register(Task)
class TaskAdmin(AdminMixin):
    list_display = ('name', 'get_status_task_display', 'due_date', 'priority', 'manager', 'client', 'deal')
    list_filter = ('status_task', 'priority', 'manager')
    search_fields = ('name', 'description')
    date_hierarchy = 'due_date'
    # readonly_fields = ('created_at', 'created_by', 'updated_by', 'updated_at')

@admin.register(Deal)
class DealAdmin(AdminMixin):
    list_display = ('name', 'get_status_deal_display', 'amount', 'manager', 'client')
    list_filter = ('status_deal', 'manager')
    search_fields = ('name', )

