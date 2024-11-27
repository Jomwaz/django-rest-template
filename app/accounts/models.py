from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
        It is cumbersome to attempt to modify the OOB django user model
        mid-project. This custom user model inherits the base model and
        allows for further customization of the model when/if required.   
    """
    # Add additional fields as needed
    pass
