import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional


def visualize_search_tree(search_tree: List[Tuple], max_nodes: Optional[int] = None):
    """
    Visualize the search tree from A* search.

    Args:
        search_tree: List of (parent, child) state tuples
        max_nodes: Maximum number of nodes to visualize
    """
    # Create directed graph
    G = nx.DiGraph()

    # Limit nodes if specified
    if max_nodes is not None and max_nodes < len(search_tree):
        search_tree = search_tree[:max_nodes]

    # Add edges to graph
    for parent, child in search_tree:
        # Convert board to string for node labels
        parent_str = str(parent.board.flatten().tolist())
        child_str = str(child.board.flatten().tolist())

        G.add_edge(parent_str, child_str)

    # Draw graph
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G, seed=42)  # For consistent layout

    nx.draw_networkx(
        G, pos,
        with_labels=True,
        node_color='lightblue',
        node_size=1500,
        font_size=8,
        arrows=True
    )

    plt.title(f"A* Search Tree (showing {len(G.nodes())} nodes)")
    plt.tight_layout()
    plt.show()


def create_tree_visualization_function(n):
    """
    Create a function that visualizes a search tree with n nodes.

    Args:
        n: Number of nodes to visualize

    Returns:
        Function that visualizes a search tree with n nodes
    """

    def visualize_n_nodes(search_tree):
        return visualize_search_tree(search_tree, max_nodes=n)

    return visualize_n_nodes