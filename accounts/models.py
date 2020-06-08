from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
# from django.core.validators import RegexValidator

from django_countries.fields import CountryField

from accounts.managers import CustomUserManager


class Custom_user(AbstractUser):
    # Regex = RegexValidator(regex=r'^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$'))

    username = None
    # email = models.EmailField(_('email address'), unique=True)
    identifier = models.CharField(unique=True, max_length=254)
    name = models.CharField(max_length=100)
    # mobile_no = models.CharField(validators=[Regex], unique=True, max_length=10)
    dob = models.DateField(null=True)
    country = CountryField(null=True)

    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.identifier
