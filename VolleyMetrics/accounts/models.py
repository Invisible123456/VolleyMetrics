from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    COACH = 'COACH'
    JOUEUR = 'JOUEUR'
    DEV = 'DEV'

    ROLE_CHOICES = (
        (COACH, 'Coach'),
        (JOUEUR, 'Joueur'),
        (DEV, 'DEV')
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
    

