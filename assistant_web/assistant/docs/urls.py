from django.urls import path
from . import views

app_name = "docs"

urlpatterns = [
    path("user_files/", views.user_files, name="user_files"),
    path("rename/", views.rename_file, name="rename_file"),
    path("delete/", views.delete_file, name="delete_file"),
]
