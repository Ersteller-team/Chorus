from django.db import models

# Create your models here.
class profileData(models.Model):
    user_id = models.CharField(max_length=50, unique=True)
    icon = models.URLField()
    description = models.TextField(max_length=300)
    spotify_id = models.CharField(max_length=100)
