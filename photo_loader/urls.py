from django.urls import path
from photo_loader import views

urlpatterns = [
    path('', views.PhotoLoader.as_view(), name='photo_loader'),
]