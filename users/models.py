from django.db import models
import random
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    birthday = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True) 

    def __str__(self):
        return self.username


def generate_confirmation_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

class UserConfirmation(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='confirmation')
    code = models.CharField(max_length=6)
    is_confirmed = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_confirmation_code()
        super().save(*args, **kwargs)







        