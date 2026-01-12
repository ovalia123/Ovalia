from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from decimal import Decimal
class User(AbstractUser):
    email = models.EmailField(unique=False)
    file = models.FileField(upload_to='diplomes/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/', blank=True)
    description = models.TextField(blank=True)
    cou = models.DecimalField(max_digits=10, decimal_places=2)
    poignee = models.DecimalField(max_digits=10, decimal_places=2)
    cheville = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    materiaux_choices = [
        ('Or massif 14k', 'Or massif 14k'),
        ('Or massif 10k', 'Or massif 10k'),
        ('Or rempli / Gold filled', 'Or rempli / Gold filled'),
        ('Argent sterling', 'Argent sterling'),
        ('Charms', 'Charms'),
        ('Tennis', 'Tennis'),
    ]
    materiaux = models.CharField(choices=materiaux_choices, max_length=50, default='Non defini')
    numero = models.IntegerField(null=True, unique=True)

    def __str__(self):
        return self.name

class Sales(models.Model):
    CATEGORY_CHOICES = [
        ("Collier", "Collier"),
        ("Bague", "Bague"),
        ("Bracelet de cheville", "Bracelet de cheville"),
        ("Bracelet", "Bracelet"),
        ("Bijou de main", "Bijou de main"),
        ("Boucle doreille", "Boucle doreille"),
    ]
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/', blank=True)
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    materiaux_choices = [
        ('Or massif 14k', 'Or massif 14k'),
        ('Or massif 10k', 'Or massif 10k'),
        ('Or rempli / Gold filled', 'Or rempli / Gold filled'),
        ('Argent sterling', 'Argent sterling'),
        ('Charms', 'Charms'),
        ('Tennis', 'Tennis'),
    ]
    materiaux = models.CharField(choices=materiaux_choices, max_length=255, default='Non defini')

    numero = models.CharField(max_length=255, default='Non defini')
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='Non defini')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Order(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50, default="Canada")

    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    stripe_session_id = models.CharField(max_length=255, unique=True)
    paid = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.email}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    sale = models.ForeignKey("Sales", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
