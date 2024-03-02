from django.db import models

class ProfileData(models.Model):
    user_id = models.CharField(max_length=50, unique=True)
    icon = models.URLField()
    description = models.TextField(max_length=300)
    spotify_id = models.CharField(max_length=100)

class MusicFollowData(models.Model):
    user_id = models.IntegerField()
    music_id = models.CharField(max_length=100)

class UserFollowData(models.Model):
    user_id = models.IntegerField()
    opponent_id = models.IntegerField()

class PostData(models.Model):
    user_id = models.IntegerField()
    contents = models.TextField(max_length=500)
    music = models.CharField(max_length=100)
    original_post_id = models.IntegerField()
    
class GoodData(models.Model):
    post_id = models.IntegerField()
    gooded_id = models.IntegerField()