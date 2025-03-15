from django.http import JsonResponse
from django.shortcuts import render

from playground.services.json.caching import get_cached_json


def home(request):
    """Home page displaying played games."""
    played_games_json = get_cached_json("played_games.json", "played_games.json")
    if played_games_json is None:
        return JsonResponse({"error": "JSON data doesn't match the schema"}, status=500)

    return render(request, "home_page.html", {"played_games": played_games_json})


def faq(request):
    """FAQ page that loads cached FAQs."""
    faq_json = get_cached_json("faq.json", "faq.json")
    if faq_json is None:
        return JsonResponse({"error": "JSON data doesn't match the schema"}, status=500)

    return render(request, "faq_page.html", {"faq_list": faq_json})


def settings(request):
    """Settings page."""
    return render(request, "settings_page.html")


def profile(request):
    """User profile page."""
    user_json = get_cached_json("user.json", "user.json")
    if user_json is None:
        return JsonResponse({"error": "JSON data doesn't match the schema"}, status=500)
    current_user = list(filter(lambda f: f["id"] == "fobos", user_json))[0]

    return render(request, "profile_page.html", {"user": current_user})
