from django.urls import path
from .views import other_views, game_views, blog_views

urlpatterns = [
    path("home/", other_views.home, name="home"),
    path("play/", game_views.create_game, name="create_game"),  # Create new game
    path("play/<str:game_id>/", game_views.play_game, name="play_game"),  # Load existing game
    path("play/<str:game_id>/move/", game_views.make_move, name="make_move"),  # Make a move
    path("play/<str:game_id>/is_legal/", game_views.is_move_legal, name="is_move_legal"),  # Check if the move is legal
    path("play/<str:game_id>/best_move/", game_views.make_best_move, name="make_best_move"),  # Get the best move
    path("play/<str:game_id>/reset_game/", game_views.reset_game, name="reset_game"),  # Reset game
    path("play/<str:game_id>/status/", game_views.game_status, name="game_status"),  # Get game status
    path("blogs/", blog_views.blogs, name="blogs"),
    path("blogs/<str:blog_id>/", blog_views.opened_blog, name="opened_blog"),
    path("settings/", other_views.settings, name="settings"),
    path("profile/", other_views.profile, name="profile"),
    path("faq/", other_views.faq, name="faq"),
]
