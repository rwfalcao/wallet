from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import login, authenticate

class Pessoa(models.Model):
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.PROTECT
        )

    first_name = models.CharField(
        'Primeiro nome',
        max_length=50,
        null=False
        )
        
    email = models.URLField(
        'E-mail',
        max_length=50,
        null=False
        )
    
    def __str__(self):
        return '%s (%s)' % (self.first_name, self.email)


    def get_wallet(self):
        return self.userwallet_set.filter().first()
    

