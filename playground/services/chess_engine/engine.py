from __future__ import annotations
from django.conf import settings
import chess
import chess.engine


class GameInstance:
    """Represents a chess game, either Player vs Player or Player vs Computer."""
    def __init__(self,
                 fen: str | None = chess.STARTING_FEN,
                 is_vs_computer: bool = False,
                 computer_side: bool | None = None):
        """
        :param fen: Starting position in FEN format. Uses starting position if not specified.
        :param is_vs_computer: Whether the opponent is a chess engine or a player
        """
        self.board = chess.Board(fen)
        self.is_vs_computer: bool = is_vs_computer
        self.computer_side: bool | None = computer_side

    def is_move_legal(self, uci_move: str) -> bool:
        try:
            move = chess.Move.from_uci(uci_move)
            return move in self.board.legal_moves
        except ValueError:
            return False

    def make_move(self, uci_move: str) -> dict:
        """Processes a move, updates the board, and returns the new game state."""
        move = chess.Move.from_uci(uci_move)
        if move not in self.board.legal_moves:
            return {"error": "Illegal move", "fen": self.board.fen()}

        self.board.push(move)
        return self.game_state()

    def make_best_move(self):
        """Handles the chess engine's move."""
        if self.board.is_game_over():
            return self.game_state()

        with chess.engine.SimpleEngine.popen_uci(settings.CHESS_ENGINE_PATH) as engine:
            result = engine.play(self.board, chess.engine.Limit(time=1.0))
            self.board.push(result.move)

        return self.game_state()

    def game_state(self) -> dict:
        """Returns the current game state as a dictionary."""
        return {
            "fen": self.board.fen(),
            "turn": "white" if self.board.turn else "black",
            "castling_rights": self.board.castling_rights,
            "game_outcome": self.board.outcome(),
            "can_claim_draw": self.board.can_claim_draw(),
            "can_en_passant": self.board.has_legal_en_passant(),

            # "move_history": self.board.move_stack,
            "is_check": self.board.is_check(),
            "legal_moves": [move.uci() for move in self.board.legal_moves],

            "is_vs_computer": self.is_vs_computer,
            "computer_side": self.computer_side
        }
