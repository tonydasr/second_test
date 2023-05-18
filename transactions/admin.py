from django.contrib import admin

from .models import Diposit, Withdrawal, Interest, LoanRequest, Payment, Client_USDTerc20, Client_Trc20, Client_Bitcoin,Client_Ethereum
# Register your models here.
from django.utils.html import format_html

from django.db import models

class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'amount', 'recipient_account', 'date', 'status', 'current_balance')
    list_filter = ('status', )
    search_fields = ('user__email', 'user__username')
    
    def client_name(self, obj):
        return obj.user.get_full_name()
    client_name.short_description = 'Client Name'
    
    def client_email(self, obj):
        return obj.user.email
    client_email.short_description = 'Client Email'
    
    def recipient_account(self, obj):
        return obj.target
    recipient_account.short_description = 'Recipient Account'
    
    def current_balance(self, obj):
        deposits = obj.user.deposits.aggregate(models.Sum('amount'))['amount__sum'] or 0
        withdrawals = obj.user.withdrawals.aggregate(models.Sum('amount'))['amount__sum'] or 0
        balance = deposits - withdrawals
        return balance
    current_balance.short_description = 'Current Balance'
    
admin.site.register(Withdrawal, WithdrawalAdmin)



@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'payment_method', 'amount', 'status', 'date')
    list_filter = ('status',)
    search_fields = ('user__email',)

    def client_name(self, obj):
        return obj.user.full_name
    client_name.short_description = 'Client Name'

    def client_email(self, obj):
        return obj.user.email
    client_email.short_description = 'Client Email'

    actions = ('mark_complete',)

    def mark_complete(self, request, queryset):
        queryset.update(status='COMPLETE')
        for payment in queryset:
            payment.update_balance()

    mark_complete.short_description = "Mark selected payments as complete"




class Client_USDTerc20Admin(admin.ModelAdmin):
    list_display = ('client_name', 'email', 'amount', 'status', 'date', 'balance')
    list_filter = ('status', 'date')
    search_fields = ('user__email',)
    actions = ['mark_as_complete']
    ordering = ('-date',)

    def client_name(self, obj):
        return obj.user.full_name
    client_name.admin_order_field = 'user__first_name'

    def email(self, obj):
        return obj.user.email
    email.admin_order_field = 'user__email'

    def balance(self, obj):
        return obj.user.account.balance
    balance.admin_order_field = 'user__account__balance'

    def mark_as_complete(self, request, queryset):
        for transaction in queryset:
            if transaction.user.account.balance < transaction.amount:
                self.message_user(request, f"Insufficient balance for {transaction.user.email}")
            else:
                # Deduct withdrawal amount from user's account balance
                transaction.user.account.balance -= transaction.amount
                transaction.user.account.total_withdrawal += transaction.amount
                transaction.user.account.save()

                # Update the transaction status to complete
                transaction.status = Client_USDTerc20.STATUS_COMPLETE
                transaction.save()

                # Show the updated balance after withdrawal
                balance_message = f"Balance after withdrawal: {transaction.user.account.balance}"
                self.message_user(request, balance_message)

        self.message_user(request, f"{len(queryset)} transaction(s) marked as complete.")



admin.site.register(Client_USDTerc20, Client_USDTerc20Admin)




class Client_Trc20Admin(admin.ModelAdmin):
    list_display = ('client_name', 'email', 'amount', 'status', 'date', 'balance')
    list_filter = ('status', 'date')
    search_fields = ('user__email',)
    actions = ['mark_as_complete']
    ordering = ('-date',)

    def client_name(self, obj):
        return obj.user.full_name
    client_name.admin_order_field = 'user__first_name'

    def email(self, obj):
        return obj.user.email
    email.admin_order_field = 'user__email'

    def balance(self, obj):
        return obj.user.account.balance
    balance.admin_order_field = 'user__account__balance'

    def mark_as_complete(self, request, queryset):
        for transaction in queryset:
            if transaction.user.account.balance < transaction.amount:
                self.message_user(request, f"Insufficient balance for {transaction.user.email}")
            else:
                # Deduct withdrawal amount from user's account balance
                transaction.user.account.balance -= transaction.amount
                transaction.user.account.total_withdrawal += transaction.amount
                transaction.user.account.save()

                # Update the transaction status to complete
                transaction.status = Client_Trc20.STATUS_COMPLETE
                transaction.save()

                # Show the updated balance after withdrawal
                balance_message = f"Balance after withdrawal: {transaction.user.account.balance}"
                self.message_user(request, balance_message)

        self.message_user(request, f"{len(queryset)} transaction(s) marked as complete.")

admin.site.register(Client_Trc20, Client_Trc20Admin)



class Client_BitcoinAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'email', 'amount', 'status', 'date', 'balance')
    list_filter = ('status', 'date')
    search_fields = ('user__email',)
    actions = ['mark_as_complete']
    ordering = ('-date',)

    def client_name(self, obj):
        return obj.user.full_name
    client_name.admin_order_field = 'user__first_name'

    def email(self, obj):
        return obj.user.email
    email.admin_order_field = 'user__email'

    def balance(self, obj):
        return obj.user.account.balance
    balance.admin_order_field = 'user__account__balance'

    def mark_as_complete(self, request, queryset):
        for transaction in queryset:
            if transaction.user.account.balance < transaction.amount:
                self.message_user(request, f"Insufficient balance for {transaction.user.email}")
            else:
                # Deduct withdrawal amount from user's account balance
                transaction.user.account.balance -= transaction.amount
                transaction.user.account.total_withdrawal += transaction.amount
                transaction.user.account.save()

                # Update the transaction status to complete
                transaction.status = Client_Bitcoin.STATUS_COMPLETE
                transaction.save()

                # Show the updated balance after withdrawal
                balance_message = f"Balance after withdrawal: {transaction.user.account.balance}"
                self.message_user(request, balance_message)

        self.message_user(request, f"{len(queryset)} transaction(s) marked as complete.")

admin.site.register(Client_Bitcoin, Client_BitcoinAdmin)







class Client_EthereumAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'email', 'amount', 'status', 'date', 'balance')
    list_filter = ('status', 'date')
    search_fields = ('user__email',)
    actions = ['mark_as_complete']
    ordering = ('-date',)

    def client_name(self, obj):
        return obj.user.full_name
    client_name.admin_order_field = 'user__first_name'

    def email(self, obj):
        return obj.user.email
    email.admin_order_field = 'user__email'

    def balance(self, obj):
        return obj.user.account.balance
    balance.admin_order_field = 'user__account__balance'

    def mark_as_complete(self, request, queryset):
        for transaction in queryset:
            if transaction.user.account.balance < transaction.amount:
                self.message_user(request, f"Insufficient balance for {transaction.user.email}")
            else:
                # Deduct withdrawal amount from user's account balance
                transaction.user.account.balance -= transaction.amount
                transaction.user.account.total_withdrawal += transaction.amount
                transaction.user.account.save()

                # Update the transaction status to complete
                transaction.status = Client_Ethereum.STATUS_COMPLETE
                transaction.save()

                # Show the updated balance after withdrawal
                balance_message = f"Balance after withdrawal: {transaction.user.account.balance}"
                self.message_user(request, balance_message)

        self.message_user(request, f"{len(queryset)} transaction(s) marked as complete.")

admin.site.register(Client_Ethereum, Client_EthereumAdmin)










