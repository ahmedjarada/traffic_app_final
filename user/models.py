# Imports packages:
from django.contrib.auth.models import AbstractUser
from django.db import models


# Models file for define all models on this app that be required to this app.

# Define types of users on the system:
class Role(models.Model):
    # Notes:
    """
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    """
    USER = 1
    ADMIN = 2
    ROLE_CHOICES = (
        (USER, 'user'),  # Normal user type
        (ADMIN, 'admin'),  # Admin superuser type

    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    # Define readable object style:
    def __str__(self):
        return self.get_id_display()


# Define User class
class User(AbstractUser):
    # Fields of this user "account":
    email = models.EmailField(null=False, verbose_name='Email', max_length=254)
    username = models.CharField(max_length=254, unique=True,
                                error_messages={'unique': 'This username is existing, try another username'})
    password = models.CharField(max_length=254, null=False, verbose_name='Password')
    roles = models.ManyToManyField(Role, editable=False)
    gender = models.CharField(max_length=1, choices=(('F', 'Female'), ('M', 'Male'), ('N', 'Undefined')),
                              verbose_name='Gender', default="N")
    state = models.CharField(max_length=128, null=True, verbose_name='State')
    creation_date = models.DateTimeField(auto_now_add=True, auto_created=True, editable=False,
                                         verbose_name='Creation Date')
    last_update = models.DateTimeField(null=True, editable=True, verbose_name='Last Update')
    is_verified = models.BooleanField(default=False, verbose_name='Verification')
    avatar = models.CharField(null=True, max_length=254, verbose_name='Avatar')
    bio = models.CharField(null=True, max_length=254, verbose_name='Bio')
    user_permissions = {}
    groups = {}

    # Define readable object style:
    def __str__(self):
        return 'User ID: {} with email: {}'.format(self.pk, self.email)
