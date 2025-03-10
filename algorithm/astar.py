import heapq
from typing import List, Dict, Tuple, Callable, Optional


class AStar:
    """
    A* search algorithm implementation for the 8-puzzle.
    """

    def __init__(self, game, heuristic_func: Callable):
        """
        Initialize A* search algorithm.

        Args:
            game: PuzzleGame object with game rules and goal states
            heuristic_func: Heuristic function to use
        """
        self.game = game
        self.heuristic_func = heuristic_func
        self.nodes_expanded = 0
        self.max_frontier_size = 0
        self.search_tree = []  # For visualization

    def search(self, initial_state):
        """
        Perform A* search from initial state to goal.

        Args:
            initial_state: Starting state of the puzzle

        Returns:
            List of states representing the path from initial state to goal,
            or None if no solution exists
        """
        # Check if the puzzle is solvable
        if not self.game.is_solvable(initial_state):
            return None

        open_set = []  # Priority queue (frontier)
        closed_set = set()  # Explored set

        # For each state, store g value
        g_values = {initial_state: 0}

        # For path reconstruction
        parent = {initial_state: None}

        # Initial heuristic value
        h = self.heuristic_func(initial_state, self.game.goal_states)

        # Add initial state to priority queue: (f, tiebreaker, state)
        # f = g + h, tiebreaker ensures FIFO behavior for equal f values
        counter = 0
        heapq.heappush(open_set, (h, counter, initial_state))

        while open_set:
            # Track maximum frontier size
            self.max_frontier_size = max(self.max_frontier_size, len(open_set))

            # Get state with lowest f value
            _, _, current = heapq.heappop(open_set)

            # Check if goal reached
            if current.is_goal(self.game.goal_states):
                return self._reconstruct_path(parent, current)

            # Skip if already explored
            if current in closed_set:
                continue

            # Add to explored set
            closed_set.add(current)
            self.nodes_expanded += 1

            # Get g value of current state
            current_g = g_values[current]

            # Explore neighbors
            for neighbor in current.get_neighbors(self.game):
                # Skip if already explored
                if neighbor in closed_set:
                    continue

                # Calculate new g value
                new_g = current_g + 1

                # Skip if we've found a better path already
                if neighbor in g_values and new_g >= g_values[neighbor]:
                    continue

                # Record this path
                parent[neighbor] = current
                g_values[neighbor] = new_g

                # Add to search tree for visualization
                self.search_tree.append((current, neighbor))

                # Calculate f value
                h = self.heuristic_func(neighbor, self.game.goal_states)
                f = new_g + h

                # Add to frontier
                counter += 1
                heapq.heappush(open_set, (f, counter, neighbor))

        # No solution found
        return None

    def _reconstruct_path(self, parent, current):
        """
        Reconstruct the path from initial state to goal.

        Args:
            parent: Dictionary mapping states to their parent states
            current: Goal state

        Returns:
            List of states representing the path
        """
        path = [current]
        while parent[current] is not None:
            current = parent[current]
            path.append(current)

        return list(reversed(path))

    def get_search_tree(self, max_nodes=None):
        """Get the search tree for visualization, limited to max_nodes if specified."""
        if max_nodes is not None:
            return self.search_tree[:max_nodes]
        return self.search_tree