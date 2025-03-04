from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "home_page.html")


def play(request):
    return render(request, "play_page.html")


def blogs(request):
    return render(request, "blogs_page.html")


def settings(request):
    return render(request, "settings_page.html")


def profile(request):
    return render(request, "profile_page.html")
