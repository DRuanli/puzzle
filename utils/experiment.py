import random
import time
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import pandas as pd

from puzzle.state import State
from puzzle.game import PuzzleGame
from algorithm.astar import AStar
from algorithm.heuristics import manhattan_distance, misplaced_tiles


def generate_random_state():
    """
    Generate a random initial state for the 8-puzzle.

    Returns:
        A random State object
    """
    # Generate a random permutation of numbers 0-8
    nums = list(range(9))  # 0-8, where 0 represents the blank
    random.shuffle(nums)

    # Convert to 3x3 grid
    board = np.array(nums).reshape(3, 3)
    return State(board)


def generate_solvable_state(game):
    """
    Generate a random solvable state for the 8-puzzle.

    Args:
        game: PuzzleGame object

    Returns:
        A random solvable State object
    """
    while True:
        state = generate_random_state()
        if game.is_solvable(state):
            return state


def run_experiment(num_trials: int = 100, max_steps: int = 1000):
    """
    Run experiment comparing Manhattan distance and misplaced tiles heuristics.

    Args:
        num_trials: Number of random puzzles to solve
        max_steps: Maximum number of steps to allow before giving up

    Returns:
        Dictionary with results
    """
    game = PuzzleGame()

    # Results for each heuristic
    results = {
        'Manhattan Distance': {'path_lengths': [], 'nodes_expanded': [], 'times': [], 'solved': 0},
        'Misplaced Tiles': {'path_lengths': [], 'nodes_expanded': [], 'times': [], 'solved': 0}
    }

    print(f"Running experiment with {num_trials} random puzzles...")

    for i in range(num_trials):
        if i % 10 == 0:
            print(f"Trial {i}/{num_trials}")

        # Generate a random solvable state
        initial_state = generate_solvable_state(game)

        # Test Manhattan distance
        astar_manhattan = AStar(game, manhattan_distance)
        start_time = time.time()
        path = astar_manhattan.search(initial_state)
        end_time = time.time()

        if path:  # If solution found
            results['Manhattan Distance']['path_lengths'].append(len(path) - 1)
            results['Manhattan Distance']['nodes_expanded'].append(astar_manhattan.nodes_expanded)
            results['Manhattan Distance']['times'].append(end_time - start_time)
            results['Manhattan Distance']['solved'] += 1

        # Test Misplaced tiles
        astar_misplaced = AStar(game, misplaced_tiles)
        start_time = time.time()
        path = astar_misplaced.search(initial_state)
        end_time = time.time()

        if path:  # If solution found
            results['Misplaced Tiles']['path_lengths'].append(len(path) - 1)
            results['Misplaced Tiles']['nodes_expanded'].append(astar_misplaced.nodes_expanded)
            results['Misplaced Tiles']['times'].append(end_time - start_time)
            results['Misplaced Tiles']['solved'] += 1

    # Calculate statistics
    stats = {}
    for heuristic in results:
        if results[heuristic]['solved'] > 0:
            stats[heuristic] = {
                'avg_path_length': np.mean(results[heuristic]['path_lengths']),
                'avg_nodes_expanded': np.mean(results[heuristic]['nodes_expanded']),
                'avg_time': np.mean(results[heuristic]['times']),
                'success_rate': results[heuristic]['solved'] / num_trials * 100
            }
        else:
            stats[heuristic] = {
                'avg_path_length': 0,
                'avg_nodes_expanded': 0,
                'avg_time': 0,
                'success_rate': 0
            }

    # Print results
    print("\nExperiment Results:")
    for heuristic, stat in stats.items():
        print(f"\n{heuristic}:")
        print(f"  Success rate: {stat['success_rate']:.1f}%")
        print(f"  Average path length: {stat['avg_path_length']:.2f}")
        print(f"  Average nodes expanded: {stat['avg_nodes_expanded']:.2f}")
        print(f"  Average time: {stat['avg_time']:.4f} seconds")

    # Visualize results
    visualize_experiment_results(stats)

    return stats


def visualize_experiment_results(stats):
    """
    Visualize experiment results.

    Args:
        stats: Dictionary with experiment statistics
    """
    metrics = ['avg_nodes_expanded', 'avg_path_length', 'avg_time']
    titles = ['Average Nodes Expanded', 'Average Path Length', 'Average Time (seconds)']

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for i, (metric, title) in enumerate(zip(metrics, titles)):
        values = [stats[h][metric] for h in stats]
        heuristics = list(stats.keys())

        axes[i].bar(heuristics, values)
        axes[i].set_title(title)
        axes[i].set_ylabel(title)

        # Add values on top of bars
        for j, v in enumerate(values):
            axes[i].text(j, v + 0.1, f"{v:.2f}", ha='center')

    plt.tight_layout()
    plt.show()