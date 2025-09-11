from datetime import datetime
from typing import ClassVar, Any

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.fields import EmailField, CharField, BooleanField, DateTimeField
from django.utils import timezone
from django.core.exceptions import ValidationError



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email:str, password:str, **extra_fields:Any)->'User':
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email:str, password:str, **extra_fields:Any)->'User':
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses email for authentication instead of usernames.
    """
    USER_TYPES: ClassVar[tuple[tuple[str, str], ...]] = (
        ('passenger', 'Passenger'),
        ('rider', 'Rider'),
    )

    # Required fields for authentication
    email: EmailField = models.EmailField(unique=True)

    # Custom fields
    user_type: CharField = models.CharField(max_length=20, choices=USER_TYPES)
    phone_number: CharField = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')]
    )

    # Fields required by Django
    first_name: CharField = models.CharField(max_length=150, blank=True)
    last_name: CharField = models.CharField(max_length=150, blank=True)
    is_staff: BooleanField = models.BooleanField(default=False)
    is_active: BooleanField = models.BooleanField(default=True)
    date_joined: DateTimeField = models.DateTimeField(default=timezone.now)

    created_at: DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: DateTimeField = models.DateTimeField(auto_now=True)

    # Set the custom manager and the username field
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# TODO: Complete the Passenger model implementation
class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='passenger_profile')
    passenger_id = models.CharField(max_length=10, unique=True)
    preferred_payment_method = models.CharField(max_length=10, default='momo')
    home_address = models.TextField(max_length=100)


    def __str__(self):
        return f"Passenger: {self.user.email}"


    def clean(self):
        if self.user.user_type != 'passenger':
            raise ValidationError('User is not a passenger')


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


#  TODO: Complete the Rider model implementation
class Rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rider_profile')

    def __str__(self):
        return f"Rider: {self.user.email}"




