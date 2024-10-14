from django.db import models
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
   user_id = models.AutoField(primary_key=True)
   birthday = models.DateTimeField()
   description = models.CharField(max_length=50)
   # groups = None
   # user_permissions = None
   api_settings.USER_ID_FIELD = 'user_id'
   USERNAME_FIELD  = 'username'
   REQUIRED_FIELDS = ['email', 'first_name', 'last_name','birthday','description']

class Post(models.Model):
   post_id = models.AutoField(primary_key=True)
   user_id = models.ForeignKey(User, on_delete=models.CASCADE)
   image_link = models.ImageField(upload_to='images/',null=True,default=None)
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
