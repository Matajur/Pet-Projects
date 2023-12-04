from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False)
    thurname = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
