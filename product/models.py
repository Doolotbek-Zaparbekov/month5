from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
import random
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Review(models.Model):
    text = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    stars = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=1
    )

    def __str__(self):
        return f"Review for {self.product.title}"
    

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
