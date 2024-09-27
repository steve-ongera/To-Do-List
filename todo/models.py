from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile/', blank=True, null=True , default='profile/profile.png')  # Profile picture field

    def __str__(self):
        return self.user.username
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message_text = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.title
