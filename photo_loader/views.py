from django.shortcuts import render
from django.views import View


class PhotoLoader(View):
    @staticmethod
    def get(request):
        return render(request, 'photo_loader/photo_loader.html')
