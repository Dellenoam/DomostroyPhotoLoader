from django.urls import path
from photo_loader import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('photo_loader', views.PhotoLoader.as_view(), name='photo_loader'),
    path('photo_loader/submit', views.PhotoLoaderSubmit.as_view(), name='photo_loader_submit')
]
