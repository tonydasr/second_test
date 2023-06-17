from django import forms

from .models import Diposit, Withdrawal

from .models import LoanRequest

from django import forms
from .models import LoanRequest
from .models import Payment, Client_USDTerc20, Client_Trc20, Client_Bitcoin, Client_Ethereum

class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ['reason', 'amount']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4}),
        }



class DepositForm(forms.ModelForm):
    class Meta:
        model = Diposit
        fields = ["amount"]


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ["amount", "target", "target_email", "note"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(WithdrawalForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if self.user.account.balance < amount:
            raise forms.ValidationError(
                'You Can Not Withdraw More Than You Balance.'
            )

        return amount

    def clean_target(self):
        target = self.cleaned_data['target']

        

        return target


    def clean_target_email(self):
        target = self.cleaned_data['target_email']

        

        return target

    def clean_note(self):
        note = self.cleaned_data['note']

        

        return note


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'amount', 'proof_of_pay']


class Client_USDTerc20Form(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    address = forms.CharField()



class Client_Trc20_form(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    address = forms.CharField()

class Client_Bitcoin_form(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    address = forms.CharField()


class Client_Ethereum_form(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    address = forms.CharField()
