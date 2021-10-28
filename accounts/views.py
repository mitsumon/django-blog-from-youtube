from django.shortcuts import render, redirect
from allauth.account import views


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'
