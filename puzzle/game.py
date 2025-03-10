import numpy as np
from typing import List, Tuple


class PuzzleGame:
    """
    Implements the 8-puzzle game logic including special rules.
    """

    def __init__(self):
        """Initialize the game with the four goal states."""
        self.goal_states = [
            np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]]),  # Goal 1
            np.array([[8, 7, 6], [5, 4, 3], [2, 1, 0]]),  # Goal 2
            np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]]),  # Goal 3
            np.array([[0, 8, 7], [6, 5, 4], [3, 2, 1]])  # Goal 4
        ]

    def apply_special_rules(self, state):
        """
        Apply special swapping rules:
        - Cells 1 and 3 are swapped if adjacent
        - Cells 2 and 4 are swapped if adjacent

        Args:
            state: The State object to apply rules to
        """
        # Find positions of cells 1, 2, 3, 4
        positions = {}
        for i in range(3):
            for j in range(3):
                if state.board[i, j] in [1, 2, 3, 4]:
                    positions[state.board[i, j]] = (i, j)

        # Check if cells 1 and 3 are adjacent
        if 1 in positions and 3 in positions:
            i1, j1 = positions[1]
            i3, j3 = positions[3]

            if self._are_adjacent(i1, j1, i3, j3):
                # Swap cells 1 and 3
                state.board[i1, j1], state.board[i3, j3] = state.board[i3, j3], state.board[i1, j1]

        # Check if cells 2 and 4 are adjacent
        if 2 in positions and 4 in positions:
            i2, j2 = positions[2]
            i4, j4 = positions[4]

            if self._are_adjacent(i2, j2, i4, j4):
                # Swap cells 2 and 4
                state.board[i2, j2], state.board[i4, j4] = state.board[i4, j4], state.board[i2, j2]

    def _are_adjacent(self, i1: int, j1: int, i2: int, j2: int) -> bool:
        """Check if two cells are adjacent horizontally or vertically."""
        return (abs(i1 - i2) == 1 and j1 == j2) or (abs(j1 - j2) == 1 and i1 == i2)

    def is_solvable(self, state) -> bool:
        """
        Check if the puzzle is solvable.

        With multiple goal states and special swapping rules, traditional
        solvability checks aren't reliable. We'll assume all puzzles are solvable
        and let the A* algorithm determine if a solution exists.
        """
        # With multiple goal states and special swapping rules,
        # standard inversion counting isn't applicable
        return True