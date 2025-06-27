from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.apps import AppConfig



class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")  # Proper user referencing
    message = models.TextField(blank=True, null=True)  # Optional text content
    file = models.FileField(upload_to="shared_files/", blank=True, null=True)  # File upload field
    timestamp = models.DateTimeField(default=timezone.now)  # Auto timestamp

    def __str__(self):
        # Display either the message content or the file name
        if self.message:
            return f"{self.user.username}: {self.message[:20]}"
        elif self.file:
            return f"{self.user.username}: [File] {self.file.name}"
        else:
            return f"{self.user.username}: [No Content]"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default.png')
    nickname = models.CharField(max_length=50, default='Anonymous', blank=True)

    def __str__(self):
        return self.nickname or self.user.username

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        # Ensure signals are imported and connected
        import myapp.signals

