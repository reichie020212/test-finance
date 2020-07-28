from django.conf import settings
from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel


class UserInfo(TimeStampedModel):
    GENDER_CHOICES = Choices(
        ('male', 'Male'),
        ('female', 'Female'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=254)
    middle_name = models.CharField(
        max_length=254,
        blank=True,
        null=True,
    )
    last_name = models.CharField(max_length=254)
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=20,
    )
    occupation = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.first_name

    @property
    def full_name(self):
        return '%(last_name)s, %(first_name)s %(middle_name)s' % {
            'last_name': self.last_name.upper(),
            'first_name': self.first_name,
            'middle_name': self.middle_name,
        }
