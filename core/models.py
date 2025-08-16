from django.db import models
from django.contrib.auth.models import User

class UserMetadata(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="metadata")
    name = models.CharField(max_length=100)
    interests = models.TextField(help_text="Comma-separated list of user interests")
    drives = models.BooleanField(default=False)

    def __str__(self):
        return self.name