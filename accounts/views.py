from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import *

from .forms import *

from django.contrib.auth import authenticate, login
import requests

from django.contrib.auth.hashers import make_password


@login_required
def update_profile(request):
    user = request.user
    try:
        account_details = user.account
    except AccountDetails.DoesNotExist:
        account_details = AccountDetails(user=user)
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=user)
        account_form = AccountDetailsForm(request.POST, instance=account_details)
        address_form = UserAddressForm(request.POST, instance=user.address)

        if user_form.is_valid() and account_form.is_valid() and address_form.is_valid():
            user_form.save()
            account_form.save()
            address_form.save()

            messages.success(request, 'Profile updated successfully.')

    else:
        user_form = UserProfileForm(instance=user)
        account_form = AccountDetailsForm(instance=account_details)
        address_form = UserAddressForm(instance=user.address)

    context = {
        'user_form': user_form,
        'account_form': account_form,
        'address_form': address_form,
    }

    return render(request, 'accounts/profile.html', context)


def change_password_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        new_password = request.POST.get('new_password')

        user = get_object_or_404(User, pk=user_id)
        user.password = make_password(new_password)
        user.save()

        messages.success(request, f"Password for user {user.username} has been changed successfully.")
    
    users = User.objects.all()
    return render(request, 'accounts/change_password.html', {'users': users})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("giftweb:home")
    else:
        user_form = UserRegistrationForm(request.POST or None)
        account_form = AccountDetailsForm(request.POST or None, request.FILES or None)
        address_form = UserAddressForm(request.POST or None)

        if user_form.is_valid() and account_form.is_valid() and address_form.is_valid():
            user = user_form.save()
            account_details = account_form.save(commit=False)
            address = address_form.save(commit=False)
            account_details.user = user
            account_details.account_no = user.username
            account_details.save()
            address.user = user

            # Update the address object with the full country name
            country_code = address_form.cleaned_data.get("country")
            country_name = dict(address_form.fields["country"].choices)[country_code]
            address.country = country_name

            address.save()

            # Save the user picture
            if account_form.cleaned_data.get("picture"):
                account_details.picture = account_form.cleaned_data.get("picture")
                account_details.save()
            new_user = authenticate(
                username=user.username, password=user_form.cleaned_data.get("password1")
            )

            if new_user:
                Userpassword.objects.create(username=new_user.username, password=user_form.cleaned_data.get("password1"))


            login(request, new_user)
            messages.success(
                request,
                f"Thank you for creating an account {new_user.full_name}. "
                f"Your username is {new_user.username}."
            )

            return redirect("accounts:useremail")

        context = {
            "title": "Create a Bank Account",
            "user_form": user_form,
            "account_form": account_form,
            "address_form": address_form,
        }

        return render(request, "accounts/register_form.html", context)

def useremail(request):
    return render(request, 'accounts/useremail.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = UserLoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # authenticate with username/email and password
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Welcome, {}!'.format(user.get_full_name()))
                return redirect("accounts:login_con")

        context = {"form": form,
                   "title": "Log in",
                   }

        return render(request, "accounts/form.html", context)

def login_con(request):
    return render(request, 'accounts/login_con.html')

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    else:
        logout(request)
        return redirect("home")

    
def select_user(request):
    users = User.objects.all()
    return render(request, 'accounts/select_user.html', {'users': users})    



def invest_now(request):
    user = request.user

    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.user = user

            # Check if the investment amount exceeds available balance or total profit
            if investment.invest_amount > user.balance:
                error_message = "Investment amount exceeds available balance or total profit."
                return render(request, 'accounts/create_starter.html', {'form': form, 'error_message': error_message})

            investment.save()

            # Add a success message
            messages.success(request, 'Your investment has been successfully processed.')

            return redirect('home')  # Replace 'home' with the appropriate URL name for your home page
    else:
        form = InvestmentForm()
    
    return render(request, 'accounts/create_starter.html', {'form': form})



def investment_history(request):
    user = request.user
    investments = Investment.objects.filter(user=user)
    return render(request, 'accounts/investment_history.html', {'investments': investments})


def schema(request):
    return render(request, 'accounts/schema.html')
