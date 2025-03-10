import numpy as np
from typing import List, Tuple, Optional


class State:
    """
    Represents a state in the 8-puzzle game.
    """

    def __init__(self, board: List[List[int]], blank_pos: Optional[Tuple[int, int]] = None):
        """
        Initialize a state with a board configuration.

        Args:
            board: 3x3 grid representing the puzzle state (0 represents blank)
            blank_pos: Position of the blank space (optional, will be found if not provided)
        """
        self.board = np.array(board, dtype=int)
        self.blank_pos = blank_pos or self._find_blank()

    def _find_blank(self) -> Tuple[int, int]:
        """Find the position of the blank space (0) in the board."""
        blank_pos = np.where(self.board == 0)
        return (blank_pos[0][0], blank_pos[1][0])

    def get_neighbors(self, game):
        """
        Generate all possible next states from the current state.

        Args:
            game: The PuzzleGame object containing game rules

        Returns:
            List of neighboring states
        """
        neighbors = []
        i, j = self.blank_pos

        # Possible moves: up, down, left, right
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for di, dj in moves:
            new_i, new_j = i + di, j + dj

            # Check if the move is valid
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                # Create a new board with the tile moved
                new_board = self.board.copy()
                new_board[i, j] = new_board[new_i, new_j]
                new_board[new_i, new_j] = 0

                # Create new state
                new_state = State(new_board, (new_i, new_j))

                # Apply special rules (automatic swaps)
                game.apply_special_rules(new_state)

                neighbors.append(new_state)

        return neighbors

    def is_goal(self, goal_states) -> bool:
        """Check if this state matches any of the goal states."""
        for goal in goal_states:
            if np.array_equal(self.board, goal):
                return True
        return False

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return np.array_equal(self.board, other.board)

    def __hash__(self):
        return hash(self.board.tobytes())

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.board])