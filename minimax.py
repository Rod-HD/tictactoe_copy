# minimax.py
from typing import List, Tuple, Optional
from board import Board
import random
import math

class MinimaxAI:
    """Minimax AI implementation for Tic Tac Toe with adjustable difficulty."""
    
    def __init__(self, difficulty: str = "medium"):
        self.difficulty = difficulty
        self.max_depth = self._get_max_depth()
        
    def _get_max_depth(self) -> int:
        """Set search depth based on difficulty."""
        if self.difficulty == "easy":
            return 1
        elif self.difficulty == "medium":
            return 2
        else:  # hard
            return 3
    
    def get_best_move(self, board: Board, ai_symbol: str, human_symbol: str) -> Optional[Tuple[int, int]]:
        """Get the best move for the AI player."""
        # Get all legal moves
        legal_moves = []
        for i in range(board.rows):
            for j in range(board.cols):
                if board.is_empty(i, j):
                    legal_moves.append((i, j))
        
        if not legal_moves:
            return None
            
        # Easy mode: sometimes make random moves
        if self.difficulty == "easy" and random.random() < 0.4:
            return random.choice(legal_moves)
        
        # Find best move using minimax
        best_score = -math.inf
        best_move = legal_moves[0]
        
        for move in legal_moves:
            i, j = move
            # Try the move
            board._grid[i][j] = ai_symbol
            board._legal.remove((i, j))
            
            # Get score for this move
            score = self._minimax(board, 0, False, ai_symbol, human_symbol, -math.inf, math.inf)
            
            # Undo the move
            board._grid[i][j] = board.EMPTY
            board._legal.add((i, j))
            
            # Update best move
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def _minimax(self, board: Board, depth: int, is_maximizing: bool, 
                 ai_symbol: str, human_symbol: str, alpha: float, beta: float) -> float:
        """Minimax algorithm with alpha-beta pruning."""
        # Check terminal states
        if board.has_winner(ai_symbol):
            return 10 - depth
        elif board.has_winner(human_symbol):
            return depth - 10
        elif board.is_full() or depth >= self.max_depth:
            return 0
        
        if is_maximizing:
            max_eval = -math.inf
            
            for i in range(board.rows):
                for j in range(board.cols):
                    if board.is_empty(i, j):
                        # Make move
                        board._grid[i][j] = ai_symbol
                        board._legal.remove((i, j))
                        
                        # Recurse
                        eval_score = self._minimax(board, depth + 1, False, ai_symbol, human_symbol, alpha, beta)
                        
                        # Undo move
                        board._grid[i][j] = board.EMPTY
                        board._legal.add((i, j))
                        
                        max_eval = max(max_eval, eval_score)
                        alpha = max(alpha, eval_score)
                        
                        if beta <= alpha:
                            break
                            
            return max_eval
        else:
            min_eval = math.inf
            
            for i in range(board.rows):
                for j in range(board.cols):
                    if board.is_empty(i, j):
                        # Make move
                        board._grid[i][j] = human_symbol
                        board._legal.remove((i, j))
                        
                        # Recurse
                        eval_score = self._minimax(board, depth + 1, True, ai_symbol, human_symbol, alpha, beta)
                        
                        # Undo move
                        board._grid[i][j] = board.EMPTY
                        board._legal.add((i, j))
                        
                        min_eval = min(min_eval, eval_score)
                        beta = min(beta, eval_score)
                        
                        if beta <= alpha:
                            break
                            
            return min_eval
