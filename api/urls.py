from api.spectacular.urls import urlpatterns as doc_api
from users.urls import urlpatterns as user_api
api_name = 'api'

urlpatterns = []

urlpatterns += doc_api
urlpatterns += user_api
