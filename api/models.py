from django.db import models

# Create your models here.
class User(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    accessToken = models.CharField(max_length=200)
    refreshToken = models.CharField(max_length=200)
    expirationDate = models.DateTimeField('expiration date')
    
    
    def __str__(self):
        return self.id


