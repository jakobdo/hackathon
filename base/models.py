from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy

from stdimage import JPEGField


class User(AbstractUser):
    class Roles(models.IntegerChoices):
        CLERK = 1, gettext_lazy('Clerk')
        ACCOUNTANT = 2, gettext_lazy('Accountant')
        PERSONAL_BANKER = 3, gettext_lazy('Personal Banker')
        TEAM_MANAGER = 4, gettext_lazy('TEAM Manager')
        DIRECTOR = 5, gettext_lazy('Director')

    role = models.PositiveSmallIntegerField(
        choices=Roles.choices,
        default=Roles.CLERK
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField()
    picture = JPEGField(
        upload_to='users/images',
        variations={
            'full': (None, None),
            'medium': (300, 300)
        },
    )


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now=True)
