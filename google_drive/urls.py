from django.urls import path
from . import views

urlpatterns = [
    path("create_doc/", views.create_google_doc),
]
