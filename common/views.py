from typing import Optional, Type, List, Dict
from djoser.views import UserViewSet
from rest_framework import mixins
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework.serializers import Serializer
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet


class ExtendedView:
    """
    Базовый класс для представлений с поддержкой динамического выбора
    сериализаторов и разрешений на основе действия (action) или HTTP-метода.

    Атрибуты:
        multi_serializer_class (Optional[Dict[str, Type[Serializer]]]):
            Словарь с привязкой действий (или методов) к сериализаторам.
        multi_permission_classes (Optional[Dict[str, List[Type[BasePermission]]]]):
            Словарь с привязкой действий (или методов) к классам разрешений.
        permission_classes (Tuple[Type[BasePermission], ...]):
            Классы разрешений по умолчанию.
        serializer_class (Optional[Type[Serializer]]):
            Сериализатор по умолчанию, если multi_serializer_class не указан.
        request (Optional[Request]):
            Текущий объект запроса, содержащий метод HTTP и данные.
    """
    multi_serializer_class: Optional[Dict[str, Type[Serializer]]] = None
    multi_permission_classes: Optional[Dict[str, List[Type[BasePermission]]]] = None
    permission_classes: tuple = (AllowAny,)
    serializer_class: Optional[Type[Serializer]] = None
    request: Optional[Request] = None

    def get_serializer_class(self) -> Type[Serializer]:
        """
        Возвращает сериализатор для текущего действия или HTTP-метода.

        Если `multi_serializer_class` не указан, используется `serializer_class`.

        Возвращает:
            Type[Serializer]: Класс сериализатора.

        Исключения:
            AssertionError: Если оба атрибута (`serializer_class` и `multi_serializer_class`) не определены.
        """
        assert self.serializer_class or self.multi_serializer_class, (
            '"%s" должен либо включать `serializer_classes`, '
            '`multi_serializer_classes`, атрибут, либо переопределять '
            '`get_serializer_class()` метод.' % self.__class__.__name__
        )
        if not self.multi_serializer_class:
            return self.serializer_class  # type: ignore
        # raise NotImplementedError(
        #     "multi_serializer_class поддержка не реализована в данном методе."
        # )

    def get_permission(self) -> List[BasePermission]:
        """
        Возвращает список разрешений для текущего действия или HTTP-метода.

        Если `multi_permission_classes` определён, используются разрешения,
        привязанные к текущему действию или методу. Иначе — `permission_classes`.

        Возвращает:
            List[BasePermission]: Список экземпляров разрешений.
        """
        if hasattr(self, 'action'):
            action = self.action  # type: ignore
        else:
            action = self.request.method if self.request else None

        if self.multi_permission_classes and action:
            permissions = self.multi_permission_classes.get(action)
            if permissions:
                return [permission() for permission in permissions]

        return [permission() for permission in self.permission_classes]


class ExtendedGenericViewSet(ExtendedView, GenericViewSet):
    """Расширенный набор общих представлений."""
    pass


class ExtendedUserViewSet(ExtendedView, UserViewSet):
    """Расширенное представление пользователя."""
    pass


class ExtendedCreateAPIView(ExtendedView, CreateAPIView):
    """Расширенное представление для создания."""
    pass


class ListViewSet(ExtendedGenericViewSet, mixins.ListModelMixin):
    """
    Класс включающий базовый набор поведения generic view и включающий
    модель списка, имеет такие методы как: `get_object`, `get_queryset`, `list`.
    """
    pass


class CreateViewSet(ExtendedGenericViewSet, mixins.CreateModelMixin):
    """Класс представления включающий в себя Create mixins."""
    pass


class RetrieveListViewSet(
    ExtendedGenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin
):
    """Класс представления включающий в себя List и Retrieve mixins."""
    pass


class CRDListViewSet(
    ExtendedGenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin
):
    """
    Класс представления включающий в себя список, базовые операции,
    кроме UpdateModelMixin.
    """
    pass


class CUDViewSet(
    ExtendedGenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    """
    Класс представления включающий в себя базовые операции, кроме RetrieveModelMixin.
    """
    pass


class RUDViewSet(
    ExtendedGenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    """
    Класс представления включающий в себя базовые операции, кроме CreateModelMixin.
    """
    pass


class CRUListViewSet(
    ExtendedGenericViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin
):
    """Класс включающий в себя базовые операции, кроме DestroyModelMixin."""
    pass


class CRUDListViewSet(
    CRUListViewSet,
    mixins.DestroyModelMixin
):
    """Класс включающий в себя CRUD-операции."""
    pass
