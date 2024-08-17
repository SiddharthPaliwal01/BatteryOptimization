import networkx as nx
import random
import time

# Function to simulate battery consumption based on conditions
def calculate_battery_usage(distance, payload_weight, wind_speed, altitude_change):
    base_consumption = distance * 1.0  # Base consumption per distance unit
    payload_factor = 1.0 + (payload_weight / 10.0)
    wind_factor = 1.0 + (wind_speed / 10.0)
    altitude_factor = 1.0 + (altitude_change / 100.0)
    
    return base_consumption * payload_factor * wind_factor * altitude_factor

# Function to update graph weights in real-time
def update_graph_weights(G, payload_weight, wind_speed, altitude_change):
    for u, v, d in G.edges(data=True):
        distance = d['distance']
        G[u][v]['weight'] = calculate_battery_usage(distance, payload_weight, wind_speed, altitude_change)

# Function to get the optimized path and battery usage
def get_optimized_path(G, start_node, end_node):
    shortest_path = nx.dijkstra_path(G, start_node, end_node, weight='weight')
    battery_consumption = sum(G[start][end]['weight'] for start, end in zip(shortest_path[:-1], shortest_path[1:]))
    return shortest_path, battery_consumption

# Function to calculate battery usage for a non-optimized (default) path
def calculate_non_optimized_path(G, start_node, end_node):
    non_optimized_path = list(G.neighbors(start_node)) + [end_node]  # Simplified non-optimized path
    battery_consumption = sum(G[start][end]['weight'] for start, end in zip(non_optimized_path[:-1], non_optimized_path[1:]))
    return non_optimized_path, battery_consumption

# Step 1: Define waypoints and initial battery consumption model
waypoints = {
    'Warehouse': {'Checkpoint1': 5, 'Checkpoint2': 8},
    'Checkpoint1': {'Warehouse': 5, 'Checkpoint2': 3, 'Customer': 7},
    'Checkpoint2': {'Warehouse': 8, 'Checkpoint1': 3, 'Customer': 4},
    'Customer': {'Checkpoint1': 7, 'Checkpoint2': 4}
}

# Create a directed graph
G = nx.DiGraph()

# Add edges with distances (to be converted to battery usage weights)
for start, ends in waypoints.items():
    for end, distance in ends.items():
        G.add_edge(start, end, distance=distance)

# Initial conditions
payload_weight = 5.0  # kg
wind_speed = 10.0  # m/s
altitude_change = 50.0  # meters

# Update the graph weights based on initial conditions
update_graph_weights(G, payload_weight, wind_speed, altitude_change)

# Step 2: Calculate battery usage for a non-optimized path
start_node = 'Warehouse'
end_node = 'Customer'
non_optimized_path, non_optimized_battery = calculate_non_optimized_path(G, start_node, end_node)

# Real-time optimization loop
while True:
    # Simulate real-time condition changes
    wind_speed = random.uniform(5, 15)  # Changing wind speed
    altitude_change = random.uniform(30, 70)  # Changing altitude
    payload_weight = random.uniform(3, 7)  # Changing payload weight
    
    # Update the graph weights based on real-time conditions
    update_graph_weights(G, payload_weight, wind_speed, altitude_change)
    
    # Step 3: Calculate battery usage for the optimized path
    optimized_path, optimized_battery = get_optimized_path(G, start_node, end_node)
    
    # Comparison Output
    print(f"Real-Time Conditions -> Wind: {wind_speed:.2f} m/s, Altitude Change: {altitude_change:.2f} m, Payload: {payload_weight:.2f} kg")
    print(f"Non-Optimized Path: {non_optimized_path}")
    print(f"Non-Optimized Battery Consumption: {non_optimized_battery:.2f} units")
    print(f"Optimized Path: {optimized_path}")
    print(f"Optimized Battery Consumption: {optimized_battery:.2f} units")
    print(f"Battery Saved: {non_optimized_battery - optimized_battery:.2f} units")
    print("-" * 60)
    
    # Simulate real-time update frequency (e.g., every 10 seconds)
    time.sleep(10)
