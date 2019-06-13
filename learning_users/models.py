from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):

    # Create relationtship (don't inherit from User!)
    user = models.OneToOneField(User,on_delete=models.CASCADE) # This is like an extension of the User class

    #addtional attributes
    portfolio_site=models.URLField(blank=True)
    profile_pic=models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username


