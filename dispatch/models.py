from django.db import models

class MonzoToken(models.Model):
    hash = models.CharField(max_length=50, null=False, blank=False)
    token = models.CharField(max_length=200, null=False, blank=False)
    
    def __str__(self):
        return self.name or self.reference