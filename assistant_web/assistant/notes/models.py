from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    tags = models.CharField(max_length=255)

    def __str__(self):
        return self.text
