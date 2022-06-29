from email.policy import default
from pickle import FALSE
from unicodedata import name
from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import ugettext_lazy as _
import jwt
from datetime import datetime, timedelta


# Create your models here.
#custom user manager
class CustomUserManager(BaseUserManager):
    #override create user 
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    #override create superuser
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
#custom user model
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return self.full_name
    @property
    def token(self):
        return jwt.encode({'id':self.id , 'exp': datetime.utcnow() + timedelta(hours = 24)}, settings.SECRET_KEY,algorithm='HS256')


# class Themes(models.Model):
#     theme = models.CharField(max_length=255,unique=True)
#     def __str__(self):
#         return self.theme
#theme of user 
class ThemeDetail(models.Model):   
    user = models.OneToOneField(CustomUser, primary_key=True,on_delete= models.CASCADE)
    theme_selected = models.CharField(max_length=25, default='white')

    def __str__(self):
        return str(self.user)