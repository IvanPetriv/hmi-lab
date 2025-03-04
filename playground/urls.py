from django.urls import path
from . import views


urlpatterns = [
    path("home/", views.home),
    path("play/", views.play),
    path("blogs/", views.blogs),
    path("settings/", views.settings),
    path("profile/", views.profile),
]
