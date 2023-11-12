from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('photo_loader.urls')),
    path('', include('account.urls')),
]
