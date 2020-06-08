from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

from accounts.utility import phone_number_validation


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique
    identifiers for authentication instead of usernames.
    """
    # from ipdb import set_trace; set_trace()
    def create_user(self, identifier, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if '@' in identifier:
            email = self.normalize_email(identifier)
            user = self.model(identifier=email, **extra_fields)
        else:
            mobile_no = phone_number_validation(identifier)
            user = self.model(identifier=mobile_no, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, identifier, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(identifier, password, **extra_fields)
