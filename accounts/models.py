from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

Phone_no_validator = RegexValidator(regex=r'^\d{10}$', message = 'Enter a valid phone no.')

class CustomUser(AbstractUser):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_photo')
    about = models.CharField(max_length=500,blank=True)
    birth_date = models.DateField(null=True,blank=True)
    location = models.CharField(max_length=30,blank=True)
    permanent = models.CharField(max_length=100,blank=True)
    pno = models.CharField(max_length=10,validators=[Phone_no_validator],blank=True)
    qualification = models.CharField(max_length=15,blank=True)
    gender = models.CharField(max_length=10,blank=True)
    def __str__(self):
    	return self.username
