

from clients.models.client import Client
from clients.models.deals import Deal
from rest_framework.exceptions import ValidationError

class ManagerClientLimitValidator:
    """
    Валидатор, который проверяет, что менеджер не управляет более 5 клиентами.
    Этот валидатор вызывается при создании или обновлении клиента, чтобы убедиться, что
    менеджер не превышает лимит.

    :raises ValidationError: Если менеджер управляет более 5 клиентами.
    """

    def __call__(self, attrs):
        """
        Проверяет количество клиентов у менеджера.

        :param attrs: Атрибуты сериализатора, в которых ожидается наличие поля `manager`.
        :raises ValidationError: Если количество клиентов для данного менеджера >= 5.
        """
        manager = attrs.get('manager')

        # Если менеджер не передан, берем текущего пользователя из контекста запроса
        if not manager and 'request' in attrs:
            manager = attrs['request'].user

        if manager:
            client_count = Client.objects.filter(manager=manager).count()
            if client_count >= 5:
                raise ValidationError(
                    {'manager': f'Менеджер {manager} уже управляет 5 клиентами, нельзя добавить больше.'})


class DealClientLimitValidator:
    """
    Валидатор, который проверяет, что у клиента не больше 3 сделок со статусом 'В работе'.
    Этот валидатор вызывается при создании или обновлении сделки, чтобы убедиться, что
    клиент не превышает лимит активных сделок.

    :raises ValidationError: Если количество активных сделок клиента >= 3.
    """

    def __call__(self, attrs):
        """
        Проверяет количество активных сделок у клиента.

        :param attrs: Атрибуты сериализатора, в которых ожидается наличие поля `deal`.
        :raises ValidationError: Если у клиента более 3 активных сделок.
        """
        client_id = attrs.get('client_id')

        if client_id:
            deal_count = Deal.objects.filter(client_id=client_id, status_deal='В работе').count()
            if deal_count >= 3:
                raise ValidationError({'deal': 'У клиента уже есть 3 активные сделки, нельзя добавить больше.'})
