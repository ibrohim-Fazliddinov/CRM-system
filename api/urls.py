from django.urls import path, include

from api.spectacular.urls import urlpatterns as doc_api
api_name = 'api'

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
]

urlpatterns += doc_api
