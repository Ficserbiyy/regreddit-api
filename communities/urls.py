from django.urls import path
from .views import community_list


urlpatterns = [
    path("", community_list),
]
