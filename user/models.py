from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    )

    STATUS_CHOICES = (
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    password_changed_at = models.DateTimeField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    def get_token(self):
        refresh = RefreshToken.for_user(self)

        # token
        refresh['name'] = self.name
        refresh['email'] = self.email
        refresh['mobileNumber'] = self.mobile_number
        refresh['role'] = self.role
        refresh['status'] = self.status
        refresh['profilePhoto'] = self.profile_photo.url if self.profile_photo else None

        return {
            'refreshToken': str(refresh),
            'accessToken': str(refresh.access_token),
        }