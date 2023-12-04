from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path("", views.note_list, name="note_list"),
    path("create/", views.create_note, name="create_note"),
    path("search/", views.search_note, name="search_note"),
    path("<int:pk>/edit/", views.edit_note, name="edit_note"),
    path("<int:pk>/delete/", views.delete_note, name="delete_note"),
]
