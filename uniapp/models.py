from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    id=models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  
    image=models.ImageField(upload_to='media/profile',null=True)
    def __str__(self):
        return self.username
    
class Image(models.Model):
    image = models.ImageField(upload_to='media/image/')
class Items(models.Model):
    id = models.BigAutoField(primary_key=True)
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=100, default='active', null=True)
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=300, null=True)
    images = models.ManyToManyField(Image)  




class DriverRegistration(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    id=models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    car_number = models.CharField(max_length=20)
    driver_image = models.ImageField(upload_to='driver_images/', null=True, blank=True)
    car_image = models.ImageField(upload_to='driver_images/', null=True, blank=True)
    vehicle_type = models.CharField(max_length=20, null=True)
    price=models.IntegerField(null=True)
    city=models.CharField(max_length=200,null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )

  
