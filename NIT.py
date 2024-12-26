import random
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

def get_graph():
    """Function to get the graph input from the user."""
    V = int(input("Enter the number of vertices: "))
    E = int(input("Enter the number of edges: "))
    edges = []
    print("Enter edge (u v): ")
    for _ in range(E):
        u, v = input().split()
        edges.append((u, v))
    
    return V, edges

def build_adjacency_list(V, edges):
    """Function to build an adjacency list from the vertices and edges."""
    adjacency_list = defaultdict(list)
    for u, v in edges:
        adjacency_list[u].append(v)
        adjacency_list[v].append(u)
    return adjacency_list

def get_neighbors_at_distance_2(adjacency_list):
    """Function to get neighbors at distance 2 for each vertex."""
    neighbors_at_distance_2 = {vertex: set() for vertex in adjacency_list}
    for vertex, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            for second_neighbor in adjacency_list[neighbor]:
                if second_neighbor != vertex:
                    neighbors_at_distance_2[vertex].add(second_neighbor)
    return neighbors_at_distance_2

def heuristic_h1(vertices, adjacency_list, neighbors_at_distance_2):
    """Heuristic H1 function to find a hop Italian domination function."""
    f = {vertex: -1 for vertex in vertices}
    
    # Sequence order: Process vertices in a specific order
    sequence_order = sorted(vertices, key=lambda x: len(adjacency_list[x]), reverse=True)
    
    # Step 1: Assign random values of 0 or 1 to all vertices
    for vertex in sequence_order:
        f[vertex] = random.choice([1])
        print(f"Heuristic H1 - Vertex {vertex} assigned value {f[vertex]} randomly.")
    
    # Step 3: Ensure vertices with value 0 have at least two 1s at distance 2
    for vertex in sequence_order:
        if f[vertex] == 0:
            count_0_hop_2 = sum(
                1 for neighbor in neighbors_at_distance_2[vertex]
                if f[neighbor] == 1 and neighbor not in adjacency_list[vertex]
            )
            if count_0_hop_2 < 2:
                candidates = [
                    neighbor for neighbor in neighbors_at_distance_2[vertex]
                    if f[neighbor] != 1 and neighbor != vertex and neighbor not in adjacency_list[vertex]
                ]
                if len(candidates) >= 2:
                    chosen_1, chosen_2 = random.sample(candidates, 2)
                    f[chosen_1] = 1
                    f[chosen_2] = 1
                    print(f"Heuristic H1 - Vertex {chosen_1} and Vertex {chosen_2} assigned value 1 to meet distance 2 requirement.")
                else:
                    for candidate in candidates:
                        f[candidate] = 1
                        print(f"Heuristic H1 - Vertex {candidate} assigned value 1 as fallback.")

    # Step 2: Assign 0 to vertices at distance 2 from multiple 0s
    for vertex in sequence_order:
        if f[vertex] == 1:
            # Get neighbors at distance 2 that are not directly connected to the selected vertex
            candidates = [
                neighbor for neighbor in neighbors_at_distance_2[vertex]
                if f[neighbor] == 1 and neighbor not in adjacency_list[vertex]
            ]
            if len(candidates) >= 2:
                f[vertex] = 0
                print(f"Heuristic H1 - Vertex {vertex} assigned value 0 to meet distance 2 from multiple 0s requirement.")
    return f

def heuristic_h2(vertices, adjacency_list, neighbors_at_distance_2):
    """Heuristic H2 function to find a hop Italian domination function."""
    f = {vertex: -1 for vertex in vertices}  # Initialize all values to -1

    for vertex in vertices:
        if f[vertex] == -1:
            f[vertex] = random.choice([2])
            print(f"Heuristic H2 - Vertex {vertex} assigned value {f[vertex]} randomly.")

    # Step 1: Assign 0 to vertices at distance 2 from multiple 2s
    for vertex in vertices:
        if f[vertex] == 2:
            # Get neighbors at distance 2 that are not directly connected to the selected vertex
            candidates = [
                neighbor for neighbor in neighbors_at_distance_2[vertex]
                if f[neighbor] == 2 and neighbor not in adjacency_list[vertex]
            ]
            if candidates:
                chosen = random.choice(candidates)
                f[chosen] = 0
                print(f"Heuristic H2 - Vertex {chosen} assigned value 0 to meet distance 2 from multiple 2s requirement.")

    return f

def combined_heuristic(vertices, adjacency_list, neighbors_at_distance_2):
    """Combined heuristic function to find a hop Italian domination function."""
    with ThreadPoolExecutor() as executor:
        f_h1_future = executor.submit(heuristic_h1, vertices, adjacency_list, neighbors_at_distance_2)
        f_h2_future = executor.submit(heuristic_h2, vertices, adjacency_list, neighbors_at_distance_2)

        f_h1 = f_h1_future.result()
        f_h2 = f_h2_future.result()

    total_weight_h1 = calculate_total_weight(f_h1)
    total_weight_h2 = calculate_total_weight(f_h2)

    if total_weight_h1 <= total_weight_h2:
        best_heuristic = 'H1'
        best_f = f_h1
        best_weight = total_weight_h1
    else:
        best_heuristic = 'H2'
        best_f = f_h2
        best_weight = total_weight_h2

    return f_h1, total_weight_h1, f_h2, total_weight_h2, best_heuristic, best_f, best_weight

def calculate_total_weight(f):
    """Function to calculate the total weight of the hop Italian domination function."""
    return sum(f.values())

def main():
    print("Enter the graph details:")
    V, edges = get_graph()
    vertices = [str(i+1) for i in range(V)]

    adjacency_list = build_adjacency_list(V, edges)
    neighbors_at_distance_2 = get_neighbors_at_distance_2(adjacency_list)

    f_h1, total_weight_h1, f_h2, total_weight_h2, best_heuristic, best_f, best_weight = combined_heuristic(vertices, adjacency_list, neighbors_at_distance_2)

    print("\nThe hop Italian domination function for H1 is:")
    print(", ".join(f"f({vertex}) = {f_h1[vertex]}" for vertex in vertices))
    print(f"Total weight of H1: {total_weight_h1}\n")
    
    print("The hop Italian domination function for H2 is:")
    print(", ".join(f"f({vertex}) = {f_h2[vertex]}" for vertex in vertices))
    print(f"Total weight of H2: {total_weight_h2}\n")
    
    print(f"Best heuristic: {best_heuristic}")
    print("Best hop Italian domination function is:")
    print(", ".join(f"f({vertex}) = {best_f[vertex]}" for vertex in vertices))
    print(f"Total weight: {best_weight}")

if name == "main":
    main()