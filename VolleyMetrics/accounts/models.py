from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    COACH = 'COACH'
    JOUEUR = 'JOUEUR'
    ADMIN = 'ADMIN'

    ROLE_CHOICES = (
        (COACH, 'Coach'),
        (JOUEUR, 'Joueur'),
        (ADMIN, 'Admin')
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle', default="JOUEUR")
    

