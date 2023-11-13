from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View
from account.forms import LoginForm


class Login(View):
    def get(self, request):
        context = dict()
        form = LoginForm()
        context['login_form'] = form

        return render(request, 'account/login.html', context)

    def post(self, request):
        context = dict()
        form = LoginForm(request, request.POST)
        context['login_form'] = form

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if 'next' in request.GET:
                return redirect(request.GET['next'])

            return redirect('photo_loader')

        context['error_messages'] = form.errors

        return render(request, 'account/login.html', context)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('home')
