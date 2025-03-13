import uuid
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect

from playground.services.blogs.blog import Blog
from playground.services.chess_engine.engine import GameInstance


# ------------------ Dummy Blog Data ------------------
elements = [
    Blog("hello", "author", "desc",
         datetime(2023, 10, 4, 21, 45, 36),
         r"../static/pictures/100720171932.jpg"),
    Blog("hi", "me", "dddd",
         datetime(2025, 10, 4, 21, 45, 36),
         r"../static/pictures/170720171937.jpg"),
    Blog("title", "iv", "d",
         datetime(2023, 10, 4, 21, 45, 36),
         r"../static/pictures/image (10).jpg"),
]


# ------------------ Home Page ------------------
def home(request):
    return render(request, "home_page.html")


# ------------------ Game Logic ------------------
def create_game(request):
    """Creates a new game, assigns a unique ID, and stores it in the session."""
    game_id = str(uuid.uuid4())

    if "games" not in request.session:
        request.session["games"] = {}

    # Create a new game instance and store its state
    game = GameInstance()
    request.session["games"][game_id] = game.game_state()
    request.session.modified = True

    return redirect(f"/playground/play/{game_id}/")


def play_game(request, game_id):
    """Retrieves the game state from the session and renders the game board."""
    games = request.session.get("games", {})

    if game_id not in games:
        return JsonResponse({"error": "No game with such ID exists"}, status=404)

    game_state = games[game_id]
    return render(request, "play_page.html", {
        "game_id": game_id,
        "fen": game_state["fen"],
    })


def is_move_legal(request, game_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    # If received move is correct
    move = request.POST.get("move")
    if not move or not game_id:
        return JsonResponse({"error": "Missing move or game_id"}, status=400)

    # If the game exists
    games = request.session.get("games", {})
    if game_id not in games:
        return JsonResponse({"error": "Game not found"}, status=404)

    game = GameInstance(fen=games[game_id]["fen"])
    return JsonResponse({"is_legal": game.is_move_legal(move)})


def make_move(request, game_id):
    """Processes a move and updates the game state in the session."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    # If received move is correct
    move = request.POST.get("move")
    if not move or not game_id:
        return JsonResponse({"error": "Missing move or game_id"}, status=400)

    # If the game exists
    games = request.session.get("games", {})
    if game_id not in games:
        return JsonResponse({"error": "Game not found"}, status=404)

    # Load the existing game state and apply the move
    game = GameInstance(fen=games[game_id]["fen"])
    updated_game_state = game.make_move(move)

    # Save updated state back to session
    games[game_id] = updated_game_state
    request.session["games"] = games
    request.session.modified = True

    return JsonResponse(updated_game_state)


def make_best_move(request, game_id):
    """Processes the computer's move and updates the game state in the session."""
    games = request.session.get("games", {})
    if game_id not in games:
        return JsonResponse({"error": "Game not found"}, status=404)

    # Load the existing game state and apply the computer's move
    game = GameInstance(fen=games[game_id]["fen"], is_vs_computer=True)
    updated_game_state = game.make_best_move()

    # Save updated state back to session
    games[game_id] = updated_game_state
    request.session["games"] = games
    request.session.modified = True

    return JsonResponse(updated_game_state)



def reset_game(request, game_id):
    """Resets a specific game and assigns a fresh board state."""
    games = request.session.get("games", {})

    if game_id not in games:
        return JsonResponse({"error": "Game not found"}, status=404)

    # Reinitialize the game and store the new state
    game = GameInstance()
    games[game_id] = game.game_state()
    request.session["games"] = games
    request.session.modified = True

    return JsonResponse(games[game_id])


def game_status(request, game_id):
    """Returns the current state of a given game."""
    games = request.session.get("games", {})

    if game_id not in games:
        return JsonResponse({"error": "Game not found"}, status=404)

    return JsonResponse(games[game_id])


# ------------------ Additional Pages ------------------
def blogs(request):
    return render(request, "blogs_page.html", {"elements": elements})


def opened_blog(request):
    return render(request, "opened_blog_page.html", {"blog_data": ...})


def faq(request):
    return render(request, "faq_page.html", {"elements": ...})


def settings(request):
    return render(request, "settings_page.html")


def profile(request):
    return render(request, "profile_page.html")
