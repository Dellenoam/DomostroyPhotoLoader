from django.shortcuts import render
from django.views import View


# rendering login page
class Login(View):
    @staticmethod
    def get(request):
        return render(request, 'account/login_form.html')


# rendering register page
class Register(View):
    @staticmethod
    def get(request):
        return render(request, 'account/register_form.html')