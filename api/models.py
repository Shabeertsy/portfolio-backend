from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)



# Create your models here.

class BaseClass(models.Model):
    uuid = models.SlugField(default=uuid.uuid4, unique=True)
    active_status = models.BooleanField(default=True)
    created_date_time = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract=True


class Profile(AbstractUser):
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    profile_image = models.ImageField(null=True,blank=True,upload_to='profile_images')
    email=models.EmailField(unique=True)
    bio=models.TextField(null=True,blank=True)
    groups = models.ManyToManyField('auth.Group',blank=True,related_name='user_profiles',related_query_name='user_profile',)
    user_permissions = models.ManyToManyField('auth.Permission',blank=True,related_name='user_profiles',related_query_name='user_profile',)
    verify=models.BooleanField(default=False)
    objects = CustomUserManager()

    def  __str__(self):
        return self.email 

    class Meta:
        ordering = ['-id']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'


class OTPVerification(BaseClass):
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True,blank=True)
    otp=models.CharField(max_length=10,null=True,blank=True)
    created_time = models.DateTimeField(null=True,blank=True)


    def __str__(self):
        return self.email
    class Meta:
        verbose_name = 'OTP'
        verbose_name_plural = 'OTP'