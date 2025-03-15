from __future__ import annotations

from django.http import JsonResponse
from django.shortcuts import render
from playground.services.json.caching import get_cached_json


def blogs(request):
    """Blogs page that loads cached blogs."""
    blogs_json = get_cached_json("blogs.json", "blogs.json")
    if blogs_json is None:
        return JsonResponse({"error": "JSON data doesn't match the schema"}, status=500)

    return render(request, "blogs_page.html", {"blogs_list": blogs_json})


def opened_blog(request, blog_id):
    """Renders an individual blog post (TBD)."""
    blogs_json = get_cached_json("blogs.json", "blogs.json")
    if blogs_json is None:
        return JsonResponse({"error": "JSON data doesn't match the schema"}, status=500)

    selected_blog = list(filter(lambda f: f["id"] == blog_id, blogs_json))[0]

    return render(request, "opened_blog_page.html", {"blog": selected_blog})
