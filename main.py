import numpy as np
import argparse

from puzzle.state import State
from puzzle.game import PuzzleGame
from algorithm.astar import AStar
from algorithm.heuristics import manhattan_distance, misplaced_tiles
from utils.visualizer import visualize_search_tree, create_tree_visualization_function
from utils.experiment import run_experiment


def print_path(path):
    """Print the solution path."""
    if not path:
        print("No solution found!")
        return

    print(f"Solution found in {len(path) - 1} steps:")
    for i, state in enumerate(path):
        print(f"\nStep {i}:")
        print(state)


def main():
    parser = argparse.ArgumentParser(description="8-Puzzle Solver using A*")
    parser.add_argument('--heuristic', type=str, choices=['manhattan', 'misplaced', 'both'],
                        default='both', help='Heuristic function to use')
    parser.add_argument('--experiment', action='store_true',
                        help='Run experiment comparing heuristics')
    parser.add_argument('--trials', type=int, default=50,
                        help='Number of trials for experiment')
    parser.add_argument('--visualize', type=int, default=20,
                        help='Number of nodes to visualize in search tree')
    parser.add_argument('--random', action='store_true',
                        help='Use random initial state')

    args = parser.parse_args()

    # Create game
    game = PuzzleGame()

    # Create initial state
    if args.random:
        from utils.experiment import generate_solvable_state
        initial_state = generate_solvable_state(game)
        print("Random initial state:")
    else:
        # Example initial state
        initial_board = np.array([
            [1, 2, 3],
            [4, 0, 5],
            [7, 8, 6]
        ])
        initial_state = State(initial_board)
        print("Default initial state:")

    print(initial_state)
    print()

    # Run experiment if requested
    if args.experiment:
        run_experiment(num_trials=args.trials)
        return

    # Run A* with selected heuristic(s)
    if args.heuristic in ['manhattan', 'both']:
        print("\n--- A* with Manhattan Distance ---")
        astar_manhattan = AStar(game, manhattan_distance)
        path_manhattan = astar_manhattan.search(initial_state)

        print_path(path_manhattan)
        print(f"Nodes expanded: {astar_manhattan.nodes_expanded}")
        print(f"Maximum frontier size: {astar_manhattan.max_frontier_size}")

        # Visualize search tree if requested
        if args.visualize > 0:
            visualize_func = create_tree_visualization_function(args.visualize)
            visualize_func(astar_manhattan.get_search_tree())

    if args.heuristic in ['misplaced', 'both']:
        print("\n--- A* with Misplaced Tiles ---")
        astar_misplaced = AStar(game, misplaced_tiles)
        path_misplaced = astar_misplaced.search(initial_state)

        print_path(path_misplaced)
        print(f"Nodes expanded: {astar_misplaced.nodes_expanded}")
        print(f"Maximum frontier size: {astar_misplaced.max_frontier_size}")

        # Visualize search tree if requested
        if args.visualize > 0 and args.heuristic != 'both':
            visualize_func = create_tree_visualization_function(args.visualize)
            visualize_func(astar_misplaced.get_search_tree())


if __name__ == "__main__":
    main()