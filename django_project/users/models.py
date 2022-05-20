from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    def __str__(self):
        return self.user.username
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='profile.jpg',upload_to='profile_pictures')
    fname = models.CharField(max_length=50,null = True, blank = True)
    lname = models.CharField(max_length=50,null = True, blank = True)
    contact_number = models.IntegerField(default='999999999')
    email = models.EmailField(null = True, blank = True)
    address = models.CharField(max_length=250,null = True, blank = True)
