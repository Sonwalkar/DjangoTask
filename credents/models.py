from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_super_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
