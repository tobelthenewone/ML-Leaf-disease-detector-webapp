from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import EmailValidator, MinLengthValidator
from datetime import date
import os


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        
        email_validator = EmailValidator(_('Enter a valid email address'))
        email_validator(email)  # Validate email format

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, first_name=first_name, **other_fields)

        # Validate user_name field
        user_name_validator = MinLengthValidator(3, _('User name must be at least 3 characters long'))
        user_name_validator(user_name)  # Validate user_name length
        
        # Validate first_name field
        first_name_validator = MinLengthValidator(2, _('First name must be at least 2 characters long'))
        first_name_validator(first_name)  # Validate first_name length

        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True, validators=[MinLengthValidator(3)])
    first_name = models.CharField(max_length=150, blank=True, validators=[MinLengthValidator(2)])
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    def __str__(self):
        return self.user_name


 # Import your custom user model

# Define the Disease model
class Disease(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



# Define the Prediction model
class Prediction(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users')
    imageName = models.CharField(max_length=255, blank=True)
    predictedImage = models.ImageField(upload_to='predictions/', default='image.jpg')
    image = models.ImageField(upload_to='original/', default='image.jpg')
    scanned = models.BooleanField(default=False)
    severity = models.FloatField()
    diseases = models.ManyToManyField(Disease)
    # date = models.DateField(default=date.today)
    date = models.DateTimeField(auto_now_add=True)


  

    class Meta:
        ordering = ('date',)

    def get_diseases_summary(self):
        return ", ".join([disease.name for disease in self.diseases.all()])
    get_diseases_summary.short_description = "Diseases"
