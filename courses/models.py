from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    profile_image_url = models.CharField(max_length=500, blank=True, null=True)

# ALL OTHER MODELS (Department, Student, etc.) MUST BE DELETED FROM THIS FILE