from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import graphql_view


urlpatterns = [
    path("", csrf_exempt(graphql_view)),
]
