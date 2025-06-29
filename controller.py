# controller.py
from enum import Enum, auto
from typing import List, Tuple, Protocol, Optional
from kivy.clock import Clock

from board import Board
from minimax import MinimaxAI


class GameState(Enum):
    IN_PROGRESS = auto()
    X_WON = auto()
    O_WON = auto()
    DRAW = auto()


class GameObserver(Protocol):
    """Anything interested in board or state changes implements this."""

    def on_board_change(self, coords: Tuple[int, int], symbol: str) -> None: ...
    def on_state_change(
        self, state: GameState, next_turn: Optional[str]
    ) -> None: ...


class GameController:
    """Link between UI and model; enforces turn flow."""

    def __init__(self, board: Board, mode: str = "friend", difficulty: str = "medium") -> None:
        self._board = board
        self._current = "X"
        self._state = GameState.IN_PROGRESS
        self._observers: List[GameObserver] = []
        self._mode = mode
        self._difficulty = difficulty
        
        # Initialize AI if playing against bot
        if mode == "bot":
            self._ai = MinimaxAI(difficulty)
            self._human_symbol = "X"
            self._ai_symbol = "O"
        else:
            self._ai = None

    # -------- observer glue -----------------------------------------------

    def register(self, obs: GameObserver) -> None:
        self._observers.append(obs)
        # Immediately sync fresh observer with current state
        obs.on_state_change(self._state, self._current)

    def _notify_board(self, coords: Tuple[int, int], symbol: str) -> None:
        for obs in self._observers:
            obs.on_board_change(coords, symbol)

    def _notify_state(self) -> None:
        nxt = None if self._state is not GameState.IN_PROGRESS else self._current
        for obs in self._observers:
            obs.on_state_change(self._state, nxt)

    # -------- public actions ----------------------------------------------

    def play(self, i: int, j: int) -> None:
        if self._state is not GameState.IN_PROGRESS:
            return
            
        # In bot mode, only allow human moves when it's their turn
        if self._mode == "bot" and self._current != self._human_symbol:
            return
            
        if not self._board.place(i, j, self._current):
            return  # illegal move

        self._notify_board((i, j), self._current)

        if self._board.has_winner(self._current):
            self._state = (
                GameState.X_WON if self._current == "X" else GameState.O_WON
            )
        elif self._board.is_full():
            self._state = GameState.DRAW
        else:
            self._current = "O" if self._current == "X" else "X"
            
            # If it's bot's turn, schedule AI move
            if self._mode == "bot" and self._current == self._ai_symbol and self._state == GameState.IN_PROGRESS:
                Clock.schedule_once(self._make_ai_move, 0.5)

        self._notify_state()
    
    def _make_ai_move(self, dt):
        """Make AI move after a short delay."""
        if self._state != GameState.IN_PROGRESS:
            return
            
        move = self._ai.get_best_move(self._board, self._ai_symbol, self._human_symbol)
        if move:
            # Make the move directly on the board
            if self._board.place(move[0], move[1], self._ai_symbol):
                self._notify_board((move[0], move[1]), self._ai_symbol)
                
                # Check win/draw conditions
                if self._board.has_winner(self._ai_symbol):
                    self._state = GameState.O_WON
                elif self._board.is_full():
                    self._state = GameState.DRAW
                else:
                    # Switch back to human turn
                    self._current = self._human_symbol
                
                self._notify_state()

    def getBoard(self) -> Board:
        return self._board
    
    def reset(self) -> None:
        self._board.reset()
        self._current = "X"
        self._state = GameState.IN_PROGRESS
        self._notify_state()
