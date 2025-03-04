from django.conf import settings
from stockfish import Stockfish


def get_stockfish():
    return Stockfish(settings.STOCKFISH_PATH)
