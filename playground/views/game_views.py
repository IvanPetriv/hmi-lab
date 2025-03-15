import uuid
from django.http import JsonResponse
from django.shortcuts import render, redirect

from playground.services.chess_engine.engine import GameInstance


# ------------------ Game Logic ------------------

def create_game(request):
    """Creates a new game, assigns a unique ID, and stores it in the session."""
    game_id = str(uuid.uuid4())

    request.session.setdefault("games", {})
    request.session["games"][game_id] = GameInstance().game_state()
    request.session.modified = True

    return redirect(f"/playground/play/{game_id}/")


def play_game(request, game_id):
    """Retrieves the game state from the session and renders the game board."""
    game_state = request.session.get("games", {}).get(game_id)

    if not game_state:
        return JsonResponse({"error": "No game with such ID exists"}, status=404)

    return render(request, "play_page.html", {"game_id": game_id, "fen": game_state["fen"]})


def is_move_legal(request, game_id):
    """Checks if a given move is legal."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    move = request.POST.get("move")
    game_state = request.session.get("games", {}).get(game_id)

    if not move or not game_state:
        return JsonResponse({"error": "Missing move or game not found"}, status=400)

    game = GameInstance(fen=game_state["fen"])
    return JsonResponse({"is_legal": game.is_move_legal(move)})


def make_move(request, game_id):
    """Processes a move and updates the game state in the session."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    move = request.POST.get("move")
    games = request.session.get("games", {})

    if not move or game_id not in games:
        return JsonResponse({"error": "Missing move or game not found"}, status=400)

    game = GameInstance(fen=games[game_id]["fen"])
    updated_game_state = game.make_move(move)

    games[game_id] = updated_game_state
    request.session.modified = True

    return JsonResponse(updated_game_state)


def make_best_move(request, game_id):
    """Processes the computer's move and updates the game state."""
    games = request.session.get("games", {})

    if game_id not in games:
        return JsonResponse({"error": "Game not found"}, status=404)

    game = GameInstance(fen=games[game_id]["fen"], is_vs_computer=True)
    games[game_id] = game.make_best_move()
    request.session.modified = True

    return JsonResponse(games[game_id])


def reset_game(request, game_id):
    """Resets a specific game and assigns a fresh board state."""
    games = request.session.get("games", {})

    if game_id not in games:
        return JsonResponse({"error": "Game not found"}, status=404)

    games[game_id] = GameInstance().game_state()
    request.session.modified = True

    return JsonResponse(games[game_id])


def game_status(request, game_id):
    """Returns the current state of a given game."""
    game_state = request.session.get("games", {}).get(game_id)

    if not game_state:
        return JsonResponse({"error": "Game not found"}, status=404)

    return JsonResponse(game_state)
