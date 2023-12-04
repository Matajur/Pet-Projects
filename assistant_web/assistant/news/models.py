from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    url = models.URLField()
    topic = models.CharField()
    date = models.CharField()