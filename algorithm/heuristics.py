import numpy as np
from typing import List


def manhattan_distance(state, goal_states):
    """
    Manhattan distance heuristic: sum of distances each tile is from its goal position.

    Args:
        state: Current state
        goal_states: List of possible goal states

    Returns:
        Minimum Manhattan distance to any goal state
    """
    min_distance = float('inf')

    for goal in goal_states:
        # Calculate positions in goal state
        goal_positions = {}
        for i in range(3):
            for j in range(3):
                if goal[i, j] != 0:  # Skip the blank
                    goal_positions[goal[i, j]] = (i, j)

        # Calculate Manhattan distance
        distance = 0
        for i in range(3):
            for j in range(3):
                if state.board[i, j] != 0 and state.board[i, j] in goal_positions:
                    gi, gj = goal_positions[state.board[i, j]]
                    distance += abs(i - gi) + abs(j - gj)

        min_distance = min(min_distance, distance)

    return min_distance


def misplaced_tiles(state, goal_states):
    """
    Misplaced tiles heuristic: number of tiles not in their goal position.

    Args:
        state: Current state
        goal_states: List of possible goal states

    Returns:
        Minimum number of misplaced tiles to any goal state
    """
    min_misplaced = float('inf')

    for goal in goal_states:
        # Count misplaced tiles (excluding blank)
        misplaced = sum(
            1 for i in range(3) for j in range(3)
            if state.board[i, j] != 0 and state.board[i, j] != goal[i, j]
        )

        min_misplaced = min(min_misplaced, misplaced)

    return min_misplaced


"""
Admissibility and Consistency Analysis:

1. Manhattan Distance:
   - Admissibility: For each tile, the minimum number of moves needed to reach its goal position
     is at least its Manhattan distance. This never overestimates the actual cost.
   - Consistency: For any move, a tile can only decrease its Manhattan distance by at most 1.
     Since each move costs 1, the heuristic satisfies the triangle inequality h(n) ≤ c(n,n') + h(n').

2. Misplaced Tiles:
   - Admissibility: Each misplaced tile requires at least one move to reach its goal position.
     This never overestimates the actual cost.
   - Consistency: A single move can decrease the number of misplaced tiles by at most 1.
     Since each move costs 1, the heuristic satisfies the triangle inequality h(n) ≤ c(n,n') + h(n').

Both heuristics are admissible and consistent, but Manhattan distance is generally more effective
as it provides a more informed estimate of the actual cost.
"""