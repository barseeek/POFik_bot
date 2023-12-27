from django.urls import path
from datacenter import views


urlpatterns = [
    path("", views.index, name="index"),
]
