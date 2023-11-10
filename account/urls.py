from django.urls import path
from account import views

urlpatterns = [
    path('login', views.Login.as_view(), name='login_form'),
    path('register', views.Register.as_view(), name='register_form')
]