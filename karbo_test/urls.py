from django.urls import path
from .api import ViewForApi

urlpatterns = [
    path('api/', ViewForApi.as_view(), name='api'),
]