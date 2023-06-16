
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import DepositForm, WithdrawalForm
from .models import Client_USDTerc20
from .forms import Client_USDTerc20Form, Client_Bitcoin_form

from .forms import *
from .models import LoanRequest

from .forms import Client_USDTerc20Form, Client_Trc20_form, Client_Ethereum_form
from .models import Client_USDTerc20, Client_Trc20, Client_Bitcoin, Client_Ethereum


@login_required
def loan_request_view(request):
    if request.method == 'POST':
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            loan_request = form.save(commit=False)
            loan_request.user = request.user
            loan_request.save()
            messages.success(request, 'Your loan request has been submitted. You will be notified within 24 hours.')
            return redirect('home')
    else:
        form = LoanRequestForm()
    context = {
        'title': 'Loan Request',
        'form': form,
    }
    return render(request, 'transactions/loan_request.html', context)
@login_required()
def deposit_view(request):
    form = DepositForm(request.POST or None)

    if form.is_valid():
        deposit = form.save(commit=False)
        deposit.user = request.user
        deposit.save()
        # adds users deposit to balance.
        deposit.user.account.balance += deposit.amount
        deposit.user.account.save()
        messages.success(request, 'You Have Deposited {} $.'
                         .format(deposit.amount))
        return redirect("home")

    context = {
        "title": "Deposit",
        "form": form
    }
    return render(request, "transactions/form.html", context)


@login_required()
def withdrawal_view(request):
    form = WithdrawalForm(request.POST or None, user=request.user)

    if form.is_valid():
        withdrawal = form.save(commit=False)
        withdrawal.user = request.user
        
        # subtracts users withdrawal from balance.
        withdrawal.user.account.balance -= withdrawal.amount
        withdrawal.user.account.save()

        withdrawal.save()
        messages.success(
            request, 
            f'Withdrawal successful! ${withdrawal.amount} has been transferred to {form.cleaned_data["target_email"]} and should arrive within <strong>10 minutes to 1 business day</strong>. Thank you for banking with us!'
        )

        return redirect("confirm") # change the URL name to "transactions:index" to redirect to the index page

    context = {
        "title": "Withdraw",
        "form": form
    }
    return render(request, "transactions/form.html", context)






@login_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            return redirect('transactions:payment_success')  # add app name
    else:
        form = PaymentForm()
    return render(request, 'transactions/payment_form.html', {'form': form})


@login_required
def payment_success(request):
    payment = Payment.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'transactions/payment_success.html', {'payment': payment})


@login_required
def withdrawals(request):
    return render(request, 'transactions/withdrawals.html')





@login_required
def withdraw_usdt_erc20(request):
    if request.method == 'POST':
        form = Client_USDTerc20Form(request.POST)
        if form.is_valid():
            withdrawal_amount = form.cleaned_data.get('amount')
            withdrawal_address = form.cleaned_data.get('address')
            Client_USDTerc20.objects.create(user=request.user, amount=withdrawal_amount, address=withdrawal_address)
            messages.success(request, f"Withdrawal request for {withdrawal_amount} USDT ERC20 submitted successfully.")
            return redirect('transactions:erc20')
    else:
        form = Client_USDTerc20Form()
    context = {'form': form}
    return render(request, 'transactions/withdraw_usdt_erc20.html', context)


@login_required
def erc20(request):
    payment = Client_USDTerc20.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'transactions/erc20.html', {'payment': payment})




@login_required
def withdraw_trc20(request):
    form = Client_Trc20_form()
    if request.method == 'POST':
        form = Client_Trc20_form(request.POST)
        if form.is_valid():
            withdrawal_amount = form.cleaned_data.get('amount')
            withdrawal_address = form.cleaned_data.get('address')
            Client_Trc20.objects.create(user=request.user, amount=withdrawal_amount, address=withdrawal_address)
            messages.success(request, f"Withdrawal request for {withdrawal_amount} USDT TRC20 submitted successfully.")
            return redirect('transactions:trc20')
    context = {'form': form}
    return render(request, 'transactions/withdraw_usdt_trc20.html', context)

@login_required
def trc20(request):
    payment = Client_Trc20.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'transactions/trc.html', {'payment': payment})


@login_required
def withdraw_bitcoin(request):
    form = Client_Bitcoin_form()
    if request.method == 'POST':
        form = Client_Bitcoin_form(request.POST)
        if form.is_valid():
            withdrawal_amount = form.cleaned_data.get('amount')
            withdrawal_address = form.cleaned_data.get('address')
            Client_Bitcoin.objects.create(user=request.user, amount=withdrawal_amount, address=withdrawal_address)
            messages.success(request, f"Withdrawal request for {withdrawal_amount} BITCOIN submitted successfully.")
            return redirect('transactions:bitcoin')
    context = {'form': form}
    return render(request, 'transactions/withdraw_bitcoin.html', context)

@login_required
def bitcoin(request):
    payment = Client_Bitcoin.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'transactions/bitcoin.html', {'payment': payment})
    
@login_required
def withdraw_ethereum(request):
    form = Client_Ethereum_form()
    if request.method == 'POST':
        form = Client_Ethereum_form(request.POST)
        if form.is_valid():
            withdrawal_amount = form.cleaned_data.get('amount')
            withdrawal_address = form.cleaned_data.get('address')
            Client_Ethereum.objects.create(user=request.user, amount=withdrawal_amount, address=withdrawal_address)
            messages.success(request, f"Withdrawal request for {withdrawal_amount}  ETHEREUM successfully.")
            return redirect('transactions:ethereum')
    context = {'form': form}
    return render(request, 'transactions/withdraw_ethereum.html', context)

@login_required
def ethereum(request):
    payment = Client_Ethereum.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'transactions/ethereum.html', {'payment': payment})


@login_required
def transaction_history(request):
    user = request.user
    deposit_history = Diposit.objects.filter(user=user).order_by('-timestamp')
    withdrawal_history = Withdrawal.objects.filter(user=user).order_by('-timestamp')
    loan_request_history = LoanRequest.objects.filter(user=user).order_by('-requested_at')
    payment_history = Payment.objects.filter(user=user).order_by('-date')
    usdt_erc20_withdrawal_history = Client_USDTerc20.objects.filter(user=user).order_by('-date')
    trc20_withdrawal_history = Client_Trc20.objects.filter(user=user).order_by('-date')
    bitcoin_withdrawal_history = Client_Bitcoin.objects.filter(user=user).order_by('-date')
    ethereum_withdrawal_history = Client_Ethereum.objects.filter(user=user).order_by('-date')

    context = {
        'deposit_history': deposit_history,
        'withdrawal_history': withdrawal_history,
        'loan_request_history': loan_request_history,
        'payment_history': payment_history,
        'usdt_erc20_withdrawal_history': usdt_erc20_withdrawal_history,
        'trc20_withdrawal_history': trc20_withdrawal_history,
        'bitcoin_withdrawal_history': bitcoin_withdrawal_history,
        'ethereum_withdrawal_history': ethereum_withdrawal_history
    }

    return render(request, 'transactions/history.html', context)


def recent_payments(request):
    recent_payments = Payment.objects.order_by('-date', '-timestamp')[:10]
    context = {'recent_payments': recent_payments}
    return render(request, 'transactions/payment.html', context)


@login_required
def accounthistory(request):

    return render(request, 'transactions/accounthistory.html')


@login_required
def asset_balance(request):

    return render(request, 'transactions/asset_balance.html')


@login_required
def transfer_funds(request):

    return render(request, 'transactions/transfer_funds.html')


@login_required
def subtrade(request):

    return render(request, 'transactions/subtrade.html')


@login_required
def acct_profile(request):

    return render(request, 'transactions/acct_profile.html')


@login_required
def trading_plan(request):

    return render(request, 'transactions/trading_plan.html')


@login_required
def myplan(request):

    return render(request, 'transactions/myplan.html')


@login_required
def referral(request):

    return render(request, 'transactions/referral.html')

