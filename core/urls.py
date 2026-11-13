from django.urls import path

from core.controllers import home

urlpatterns = [
    path("", home, name="home"),
]
