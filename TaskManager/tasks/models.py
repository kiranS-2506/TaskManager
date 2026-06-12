from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Task(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')


    class Meta:
        db_table = "tasks"
        ordering = ["-created_at"] 
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['-updated_at']),
        ]


    def __str__(self):
        return f"{self.title} - {self.owner.username}"