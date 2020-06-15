import uuid
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy
from stdimage import JPEGField


class User(AbstractUser):
    email = models.EmailField(
        gettext_lazy('email address'),
        blank=True,
        unique=True
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00')
    )

    class Roles(models.IntegerChoices):
        STUDENT = 0, gettext_lazy('Student')
        CLERK = 1, gettext_lazy('Clerk')
        ACCOUNTANT = 2, gettext_lazy('Accountant')
        PERSONAL_BANKER = 3, gettext_lazy('Personal Banker')
        TEAM_MANAGER = 4, gettext_lazy('TEAM Manager')
        DIRECTOR = 5, gettext_lazy('Director')
        SYSTEM = 6, gettext_lazy('System User')

    role = models.PositiveSmallIntegerField(
        choices=Roles.choices,
        default=Roles.STUDENT
    )
    notes = models.TextField(blank=True)
    picture = JPEGField(
        blank=True,
        upload_to='users/images',
        variations={
            'full': (None, None),
            'medium': (300, 300)
        },
    )
    leaderboard = models.BooleanField(
        help_text=gettext_lazy(
            'Uncheck this, if you do not want your '
            'name shown on the leaderboard!'
        ),
        default=True
    )

    def update_balance(self):
        # Get all deposits on current user
        deposits = Transaction.objects.filter(
            recipient=self
        ).aggregate(balance=Sum('amount'))
        # Get all withdrawings on current user
        withdrawings = Transaction.objects.filter(
            sender=self
        ).aggregate(balance=Sum('amount'))
        # Do the math
        deposits = deposits.get("balance")
        withdrawings = withdrawings.get("balance")
        if deposits is None:
            deposits = Decimal('0.00')
        if withdrawings is None:
            withdrawings = Decimal('0.00')
        self.balance = deposits - withdrawings
        self.save()

    def get_start_deposit(self):
        Transaction.objects.create(
            sender=User.objects.get(username="system"),
            recipient=self,
            amount=settings.START_DEPOSIT
        )


class Transaction(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transaction_withdraw"
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transaction_deposit"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now=True)


class Deposit(models.Model):
    name = models.CharField(max_length=100)
    code = models.UUIDField(default=uuid.uuid4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} {self.amount}"


class DepositHistory(models.Model):
    deposit = models.ForeignKey(
        Deposit,
        on_delete=models.CASCADE,
        related_name='history'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='deposits'
    )
    created = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['deposit', 'user'], name='unique deposit_user'
            )
        ]
