from django.urls import include, re_path

from .views import *

app_name = 'transactions'

urlpatterns = [
    # re_path(r'^$', home_view, name='home'),
    re_path(r'^deposit/$', deposit_view, name='deposit'),
    re_path(r'^withdrawal/$', withdrawal_view, name='withdrawal'),
    re_path(r'^loan_request/$', loan_request_view, name='loan_request'),
    re_path(r'^create/$', payment_create, name='payment_create'),
    re_path(r'^success/$', payment_success, name='payment_success'),
    re_path(r'^withdrawals/$', withdrawals, name='withdrawals'),
    re_path(r'^withdraw_usdt_erc20/$', withdraw_usdt_erc20, name='withdraw_usdt_erc20'),
    re_path(r'^erc20/$', erc20, name='erc20'),
    re_path(r'^withdraw_trc20/$', withdraw_trc20, name='withdraw_trc20'),
    re_path(r'^trc20/$', trc20, name='trc20'),
    re_path(r'^withdraw_bitcoin/$', withdraw_bitcoin, name='withdraw_bitcoin'),
    re_path(r'^bitcoin/$', bitcoin, name='bitcoin'),
    re_path(r'^withdraw_ethereum/$', withdraw_ethereum, name='withdraw_ethereum'),
    re_path(r'^ethereum/$', ethereum, name='ethereum'),
    re_path(r'^transaction_history/$', transaction_history, name='transaction_history'),
    re_path(r'^accounthistory/$', accounthistory, name='accounthistory'),
    re_path(r'^asset_balance/$', asset_balance, name='asset_balance'),
    re_path(r'^transfer_funds/$', transfer_funds, name='transfer_funds'),
    re_path(r'^subtrade/$', subtrade, name='subtrade'),
    re_path(r'^acct_profile/$', acct_profile, name='acct_profile'),
    re_path(r'^recent_payments/$', recent_payments, name='recent_payments'),
    re_path(r'^myplan/$', myplan, name='myplan'),
    re_path(r'^referral/$', referral, name='referral'),
]
