from django.db import models

# Create your models here.
class User(models.Model):
   user_id = models.AutoField(primary_key=True)
   first_name = models.CharField(max_length=200)
   last_name = models.CharField(max_length=50)
   birthday = models.DateTimeField()
   user_name = models.CharField(max_length=10)
   email = models.CharField(max_length=50)
   password = models.CharField(max_length=50)
   description = models.CharField(max_length=50)

class Post(models.Model):
   post_id = models.AutoField(primary_key=True)
   user_id = models.ForeignKey(User, on_delete=models.CASCADE)
   image_link =  models.CharField(max_length=300)
   description_photo = models.CharField(max_length=150)
   five_starts =  models.IntegerField(default=0)
   four_starts =  models.IntegerField(default=0)
   three_starts =  models.IntegerField(default=0)
   two_starts =  models.IntegerField(default=0)
   one_starts =  models.IntegerField(default=0)

class Interaction(models.Model):
   interaction_id = models.AutoField(primary_key=True)
   user_id = models.ForeignKey(User, on_delete=models.CASCADE)
   post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
   starts = models.IntegerField(default=0)
