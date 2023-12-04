from django.urls import path
from . import views

app_name = "contacts"

urlpatterns = [
    path("", views.contact_list, name="contact_list"),
    path("add/", views.add_contact, name="add_contact"),
    path("<int:contact_id>/edit/", views.edit_contact, name="edit_contact"),
    path("<int:contact_id>/delete/", views.delete_contact, name="delete_contact"),
    path("search/", views.search_contacts, name="search_contacts"),
    path("upcoming_birthdays/", views.upcoming_birthdays, name="upcoming_birthdays"),
]
