from django.urls import include, re_path


from .views import *

app_name = 'accounts'

urlpatterns = [
    re_path(r'^login/$', login_view, name='login'),
    re_path(r'^register/$', register_view, name='register'),
    re_path(r'^logout/$', logout_view, name='logout'),
    re_path(r'^select_user/$', select_user, name='select_user'),
    re_path(r'^change-password/$', change_password_view, name='change_password'),
    re_path(r'^user/invest-now/$', invest_now, name='invest_now'),
    re_path(r'^schema$', schema, name='schema'),
    re_path(r'^investment_history$', investment_history, name='investment_history'),
    re_path(r'^update_profile$', update_profile, name='update_profile'),
    re_path(r'^login_con$', login_con, name='login_con'),
    re_path(r'^useremail$', useremail, name='useremail'),
]
