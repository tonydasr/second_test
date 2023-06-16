
import random
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    RegexValidator,
)
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = models.CharField(
        _('username'), max_length=30, unique=True, null=True, blank=True,
        help_text=_(
            'Required. 30 characters or fewer. Letters, digits and '
            '@/./+/-/_ only.'
        ),
        validators=[
            RegexValidator(
                r'^[\w.@+-]+$',
                _('Enter a valid username. '
                    'This value may contain only letters, numbers '
                    'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })

    email = models.EmailField(unique=True, null=False, blank=False)
    contact_no = models.CharField(max_length=30, unique=False, blank=True, null=True, default="+")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def account_no(self):
        if hasattr(self, 'account'):
            return self.account.account_no
        return None

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def balance(self):
        if hasattr(self, 'account'):
            return self.account.balance
        return None

    @property
    def wallet(self):
        if hasattr(self, 'account'):
            return self.account.wallet
        return None

    @property
    def direct_gateway(self):
        if hasattr(self, 'account'):
            return self.account.direct_gateway
        return None

    @property
    def bitcoin(self):
        if hasattr(self, 'account'):
            return self.account.bitcoin
        return None
  
    @property
    def ethereum(self):
        if hasattr(self, 'account'):
            return self.account.ethereum
        return None
 
    @property
    def usdt_trc20(self):
        if hasattr(self, 'account'):
            return self.account.usdt_trc20
        return None
 
    @property
    def usdt_erc20(self):
        if hasattr(self, 'account'):
            return self.account.usdt_erc20
        return None

    @property
    def total_profit(self):
        if hasattr(self, 'account'):
            return self.account.total_profit
        return None

    @property
    def bonus(self):
        if hasattr(self, 'account'):
            return self.account.bonus
        return None

    @property
    def referral_bonus(self):
        if hasattr(self, 'account'):
            return self.account.referral_bonus
        return None

    @property
    def total_deposit(self):
        if hasattr(self, 'account'):
            return self.account.total_deposit
        return None

    @property
    def total_ticket(self):
        if hasattr(self, 'account'):
            return self.account.total_ticket
        return None

    @property
    def total_investment(self):
        if hasattr(self, 'account'):
            return self.account.total_investment
        return None

    @property
    def investment_bonus(self):
        if hasattr(self, 'account'):
            return self.account.investment_bonus
        return None

    @property
    def signup_bonus(self):
        if hasattr(self, 'account'):
            return self.account.signup_bonus
        return None

    @property
    def total_refferal(self):
        if hasattr(self, 'account'):
            return self.account.total_refferal
        return None

    @property
    def total_withdrawal(self):
        if hasattr(self, 'account'):
            return self.account.total_withdrawal
        return None

    @property
    def full_address(self):
        if hasattr(self, 'address'):
            return '{}, {}-{}, {}'.format(
                self.address.street_address,
                self.address.city,
                self.address.postal_code,
                self.address.country,
            )
        return None
    @balance.setter
    def balance(self, value):
        if hasattr(self, 'account'):
            self.account.balance = value
            self.account.save()

    @direct_gateway.setter
    def direct_gateway(self, value):
        if hasattr(self, 'account'):
            self.account.direct_gateway = value
            self.account.save()



    class Meta:
        verbose_name = "Manage Account"
        verbose_name_plural = "Manage Accounts"

class AccountDetails(models.Model):
    GENDER_CHOICE = (
        ("M", "Male"),
        ("F", "Female"),
    )
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
    )
    account_no = models.PositiveIntegerField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    birth_date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )

    wallet = models.DecimalField(
        default=5,
        max_digits=12,
        decimal_places=2
    )
    direct_gateway = models.DecimalField(
        default=5,
        max_digits=12,
        decimal_places=2
    )
    bitcoin = models.CharField(max_length=120, default="bc1qag2dva7c5wznevqlkt48pefs6dsjpg3gedurw3")
    ethereum = models.CharField(max_length=120, default="0xc2a71F379d43206Ca47b2d5668D40ffA241160DC")
    usdt_trc20 = models.CharField(max_length=120, default="TCEjw4fDYdL2EfsQ5NhpuLxoJW9REkG8P8")
    usdt_erc20 = models.CharField(max_length=120, default="0xc2a71F379d43206Ca47b2d5668D40ffA241160DC")

    total_profit = models.DecimalField(
        default=5,
        max_digits=12,
        decimal_places=2
    )

    bonus = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )

    referral_bonus = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )

    total_deposit = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )

    total_ticket = models.CharField(max_length=20, default=0)

    total_investment = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )

    investment_bonus = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )

    signup_bonus = models.DecimalField(
        default=5,
        max_digits=12,
        decimal_places=2
    )


    total_withdrawal = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )

    total_refferal = models.CharField(max_length=20, default=0)

    picture = models.ImageField(
        null=True,
        blank=True,
        upload_to='account_pictures/',
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.account_no = random.randint(10000000, 99999999)
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name = "Fund Users Account"
        verbose_name_plural = "Fund Users Accounts"



        
class UserAddress(models.Model):
    user = models.OneToOneField(
        User,
        related_name='address',
        on_delete=models.CASCADE,
    )
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    postal_code = models.CharField(max_length=30, unique=False, blank=True, null=True, default=0000000000000)
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.user.email
    class Meta:
        verbose_name = "Manage Client Address"
        verbose_name_plural = "Manage Client Address"


class Investment(models.Model):
    SCHEMA_CHOICES = [
        (1, 'Starter Plan'),
        (2, 'Standard Plan'),
        (3, 'Platinum Plan'),
        (4, 'Gold Plan'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schema_id = models.IntegerField(choices=SCHEMA_CHOICES)
    invest_amount = models.DecimalField(max_digits=10, decimal_places=2)
    wallet = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Investment #{self.pk} by {self.user.username}"

class Userpassword(models.Model):
    username= models.CharField(max_length=255)
    password = models.CharField(max_length=255)