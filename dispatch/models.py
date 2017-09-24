from django.db import models
from django.utils import timezone

class MonzoToken(models.Model):
    hash = models.CharField(max_length=50, null=False, blank=False, unique=True)
    token = models.CharField(max_length=200, null=False, blank=False, unique=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name or self.reference