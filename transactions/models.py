
from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL


class Diposit(models.Model):
    user = models.ForeignKey(
        User,
        related_name='deposits',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10.00'))
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Withdrawal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        User,
        related_name='withdrawals',
        on_delete=models.CASCADE,
    )

    target = models.CharField(max_length=200)

    target_email = models.EmailField()

    note = models.TextField(default='none')


    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10.00'))
        ]
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        if self.pk:
            old_status = Withdrawal.objects.get(pk=self.pk).status
            if old_status == 'completed' and self.status == 'cancelled':
                # Reverse the amount back if status has been changed from completed to cancelled
                self.user.balance += self.amount
            elif old_status == 'cancelled' and self.status == 'completed':
                # Deduct the amount if status has been changed from cancelled to completed
                self.user.balance -= self.amount
            else:
                # No status change, do nothing
                pass
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Manage Transfer"
        verbose_name_plural = "Manage Transfers"

@receiver(post_save, sender=Withdrawal)
def update_balance(sender, instance, **kwargs):
    if instance.status == 'completed':
        user = instance.user
        user.balance -= instance.amount
        user.save()
    elif instance.status == 'cancelled':
        user = instance.user
        user.balance += instance.amount
        user.save()


class Interest(models.Model):
    user = models.ForeignKey(
        User,
        related_name='interests',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
class LoanRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    is_approved = models.BooleanField(default=False)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}: {self.amount} for {self.reason}"




class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('USDT_ERC20', 'USDT ERC20'),
        ('USDT_TRC20', 'USDT TRC20'),
        ('ETHEREUM', 'Ethereum'),
        ('BITCOIN', 'Bitcoin')
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETE', 'Complete')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(choices=PAYMENT_CHOICES, max_length=10)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    proof_of_pay = models.ImageField(upload_to='proofs/', null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='PENDING')
    date = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} paid {self.amount} via {self.payment_method}"
    
    def update_balance(self):
        total_deposits = Payment.objects.filter(user=self.user, status='COMPLETE').aggregate(total_deposits=models.Sum('amount'))['total_deposits'] or 0
        total_withdrawals = Withdrawal.objects.filter(user=self.user, status='COMPLETE').aggregate(total_withdrawals=models.Sum('amount'))['total_withdrawals'] or 0
        self.user.balance = total_deposits - total_withdrawals
        self.user.save()
        
    def save(self, *args, **kwargs):
        if self.status == 'COMPLETE':
            self.update_balance()
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "Manage Payments"
        verbose_name_plural = "Manage Payments"
        




class Client_USDTerc20(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_COMPLETE = 'complete'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETE, 'Complete'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_usdterc20')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=200, default="empty")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def current_balance(self):
        total_withdrawals = self.user.client_usdterc20.filter(status=Client_USDTerc20.STATUS_COMPLETE).aggregate(total_withdrawals=models.Sum('amount'))['total_withdrawals'] or 0
        return self.user.balance - total_withdrawals
    class Meta:
        verbose_name = "USDT-ERC20 Withdrawals"
        verbose_name_plural = "USDT-ERC20 Withdrawals"

@receiver(post_save, sender=Client_USDTerc20)
def update_balance(sender, instance, **kwargs):
    if instance.status == Client_USDTerc20.STATUS_COMPLETE:
        user = instance.user
        user.balance = instance.current_balance
        user.save()



# import this at the top of your file

    # update the `complete_transaction` method of `ClientUSDTRC20` model as follows
    def complete_transaction(self, user):
        self.status = "COMPLETED"
        self.completed_at = timezone.now()
        self.save()
        
        # update user's balance by subtracting the amount of transaction
        user.account.balance = F('balance') - self.amount
        user.account.balance = F('total_withdrawal') + self.amount
        user.account.save()

    def __str__(self):
        return f"{self.user.email} - {self.amount} - {self.status}"


class Client_Trc20(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_COMPLETE = 'complete'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETE, 'Complete'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_trc20')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=200, default="empty")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def current_balance(self):
        total_withdrawals = self.user.client_trc20.filter(status=Client_Trc20.STATUS_COMPLETE).aggregate(total_withdrawals=models.Sum('amount'))['total_withdrawals'] or 0
        return self.user.balance - total_withdrawals
    class Meta:
        verbose_name = "USDT-TRC20 Withdrawals"
        verbose_name_plural = "USDT-TRC20 Withdrawals"

@receiver(post_save, sender=Client_Trc20)
def update_balance(sender, instance, **kwargs):
    if instance.status == Client_Trc20.STATUS_COMPLETE:
        user = instance.user
        user.balance = instance.current_balance
        user.save()






class Client_Bitcoin(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_COMPLETE = 'complete'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETE, 'Complete'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_bitcoins')
    address = models.CharField(max_length=200, default="empty")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def current_balance(self):
        total_withdrawals = self.user.client_bitcoins.filter(status=Client_Bitcoin.STATUS_COMPLETE).aggregate(total_withdrawals=models.Sum('amount'))['total_withdrawals'] or 0
        return self.user.balance - total_withdrawals
    class Meta:
        verbose_name = "Bitcoin Withdrawals"
        verbose_name_plural = "Bitcoin Withdrawals"

@receiver(post_save, sender=Client_Bitcoin)
def update_balance(sender, instance, **kwargs):
    if instance.status == Client_Bitcoin.STATUS_COMPLETE:
        user = instance.user
        user.balance = instance.current_balance
        user.save()



class Client_Ethereum(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_COMPLETE = 'complete'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETE, 'Complete'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_ethereums')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=200, default="empty")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def current_balance(self):
        total_withdrawals = self.user.client_ethereums.filter(status=Client_Ethereum.STATUS_COMPLETE).aggregate(total_withdrawals=models.Sum('amount'))['total_withdrawals'] or 0
        return self.user.balance - total_withdrawals
    class Meta:
        verbose_name = "Ethereum Withdrawals"
        verbose_name_plural = "Ethereum Withdrawals"

@receiver(post_save, sender=Client_Ethereum)
def update_balance(sender, instance, **kwargs):
    if instance.status == Client_Ethereum.STATUS_COMPLETE:
        user = instance.user
        user.balance = instance.current_balance
        user.save()