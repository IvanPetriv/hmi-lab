from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("play/", views.create_game, name="create_game"),  # Create new game
    path("play/<str:game_id>/", views.play_game, name="play_game"),  # Load existing game
    path("play/<str:game_id>/move/", views.make_move, name="make_move"),  # Make a move
    path("play/<str:game_id>/is_legal/", views.is_move_legal, name="is_move_legal"),  # Check if the move is legal
    path("play/<str:game_id>/best_move/", views.make_best_move, name="make_best_move"),  # Get the best move
    path("play/<str:game_id>/reset_game/", views.reset_game, name="reset_game"),  # Reset game
    path("play/<str:game_id>/status/", views.game_status, name="game_status"),  # Get game status
    path("blogs/", views.blogs, name="blogs"),
    path("blogs<str:game_id>/", views.opened_blog, name="opened_blog"),
    path("settings/", views.settings, name="settings"),
    path("profile/", views.profile, name="profile"),
    path("faq/", views.faq, name="faq"),
]
