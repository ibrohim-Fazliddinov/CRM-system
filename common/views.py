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
            Словарь, связывающий действия (или HTTP-методы) с соответствующими классами сериализаторов.
        multi_permission_classes (Optional[Dict[str, List[Type[BasePermission]]]]):
            Словарь, связывающий действия (или HTTP-методы) с соответствующими классами разрешений.
        permission_classes (Tuple[Type[BasePermission], ...]):
            Классы разрешений по умолчанию, если для действия или метода разрешения не указаны.
        serializer_class (Optional[Type[Serializer]]):
            Сериализатор по умолчанию, если multi_serializer_class не указан.
        request (Optional[Request]):
            Объект текущего запроса, содержащий метод HTTP и данные запроса.
    """
    multi_serializer_class: Optional[Dict[str, Type[Serializer]]] = None
    multi_permission_classes: Optional[Dict[str, List[Type[BasePermission]]]] = None
    permission_classes: tuple = (AllowAny,)
    serializer_class: Optional[Type[Serializer]] = None
    request: Optional[Request] = None

    def __get_action_or_method(self):
        """
        Определяет текущее действие (action) или HTTP-метод.

        Если у объекта есть атрибут `action`, он возвращается. Иначе возвращается
        HTTP-метод текущего запроса.

        Возвращает:
            str: Название текущего действия или HTTP-метод.
        """
        if hasattr(self, 'action') and self.action:
            return self.action
        return self.request.method

    def get_serializer_class(self) -> Type[Serializer]:
        """
        Возвращает класс сериализатора для текущего действия или HTTP-метода.

        Если `multi_serializer_class` не задан, используется `serializer_class`.

        Возвращает:
            Type[Serializer]: Класс сериализатора.

        Исключения:
            AssertionError: Если ни `serializer_class`, ни `multi_serializer_class` не заданы.
        """
        assert self.serializer_class or self.multi_serializer_class, (
            f'"{self.__class__.__name__}" должен включать либо "serializer_class", '
            f'"multi_serializer_class", либо переопределять метод "get_serializer_class()".'
        )

        if not self.multi_serializer_class:
            return self.serializer_class  # type: ignore

        action = self.__get_action_or_method()
        return self.multi_serializer_class.get(action) or self.serializer_class

    def get_permission(self) -> List[BasePermission]:
        """
        Возвращает список разрешений для текущего действия или HTTP-метода.

        Если `multi_permission_classes` определён, используются разрешения,
        привязанные к текущему действию или методу. В противном случае используются
        классы из `permission_classes`.

        Возвращает:
            List[BasePermission]: Список экземпляров классов разрешений.
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


class CLUDViewSet(
    ExtendedGenericViewSet,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
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
