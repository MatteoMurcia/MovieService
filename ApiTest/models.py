from django.db import models

class People(models.Model):
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=200)
    
    def __str__(self):
        return self.email
    
class Movie(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=50)
    duration = models.CharField(max_length=20)
    objectType = models.CharField(max_length=10)
    clasification = models.CharField(max_length=50)
    creatorEmail = models.EmailField(max_length=50)
    
    def __str__(self) -> str:
        return self.name
    