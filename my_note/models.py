from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class MyNote(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    is_favourite = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-is_favourite']
