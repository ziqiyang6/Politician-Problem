from geopy.distance import great_circle
from itertools import permutations
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# Modify calculate_route_distance function to use coordinates for distance calculation
def calculate_route_distance(route):

    # Set the distance be 0 initially
    total_distance = 0

    # Use FOR LOOP to add the distance one by one, so this function can calculate the distance for a list of coordinates
    for i in range(len(route) - 1):
        total_distance += great_circle(route[i], route[i + 1]).miles
    return total_distance

# Modify shortest_route to calculate coordinates
def shortest_route(cities_coords):

    # Set the initial distance to be infinity, which is a large number
    shortest_distance = float('inf')
    shortest_route = None

    permutation_cities = [city for city in cities_coords]
    for perm in permutations(permutation_cities):

        route =  list(perm)
        current_distance = calculate_route_distance(route)

        # If a shorter distance appears, let it replace the previous shortest distance value
        if current_distance < shortest_distance:
            shortest_distance = current_distance
            shortest_route = route
    return shortest_route, shortest_distance

# Calculate the Center point
def calculate_group_center(coords):
    num_coords = len(coords)

    # If there is not any points in the set, return nothing
    if num_coords == 0:
        return None

    # Calculate the average value
    avg_latitude = sum(coord[1] for coord in coords) / num_coords
    avg_longitude = sum(coord[0] for coord in coords) / num_coords
    return avg_longitude, avg_latitude

def cities_define(path):
    # Setting the display size
    pd.set_option('display.width', 300)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Define the coordinates of the cities
    cities = pd.read_csv(path)

    # Assuming there are 'Latitude' and 'Longitude' columns in your cities DataFrame
    cities['Coordinates'] = list(zip(cities['Latitude'], cities['Longitude']))

    # Define the coordinates for the start and end cities
    start_city_coords = cities.loc[cities['Capital'] == 'Des Moines', 'Coordinates'].iloc[0]
    end_city_coords = cities.loc[cities['Capital'] == 'District of Columbia', 'Coordinates'].iloc[0]  # Adjust based on your data representation
    # Note: Ensure the representation of Washington, D.C. matches your dataset
    # Generating a list of coordinates for other cities
    exclude_cities_coords = [start_city_coords, end_city_coords]
    other_cities_coords = cities[~cities['Coordinates'].isin(exclude_cities_coords)]['Coordinates'].tolist()

    return cities, cities['Coordinates'], start_city_coords, end_city_coords, exclude_cities_coords, other_cities_coords

def points_graph(start_city_coords, end_city_coords, other_cities_coords):
    # Define the longtitudes and latitudes
    other_cities_longitudes = [coord[1] for coord in other_cities_coords]
    other_cities_latitudes = [coord[0] for coord in other_cities_coords]

    # Plot Setting
    fig = plt.figure(figsize=(10, 6))
    plt.scatter(other_cities_longitudes, other_cities_latitudes)
    plt.scatter(start_city_coords[1], start_city_coords[0], color='red', label='Start City')
    plt.scatter(end_city_coords[1], end_city_coords[0], color=(0.7, 0.5, 0.8), label='End City')
    plt.title('US State Capitals')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    return fig

def final_path_graph(total_path):
    total_path_plot = {}
    # Switch the place of longitude and latitude to plot
    total_path_plot = [(longitude, latitude) for latitude, longitude in total_path]

    # Plot path for every cluster
    fig =  plt.figure(figsize=(10, 8))
    arrow_patches = []
    for i in range(len(total_path_plot) - 1):
        start = total_path_plot[i]
        end = total_path_plot[i + 1]
        arrow = FancyArrowPatch(start, end, arrowstyle='-|>', mutation_scale=20)
        plt.gca().add_patch(arrow)
        arrow_patches.append(arrow)

    # Plot setting
    plt.xlim(-160, -70)
    plt.ylim(20, 60)
    plt.title('Total Path')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    return fig

def nearest_neighbor(start_city_coords, end_city_coords,other_cities_coords):
    # Define the rest cities
    rest_cities = other_cities_coords

    # Define the path
    path = [start_city_coords]

    # If rest cities still contain any element, the LOOP will keep running
    while rest_cities:
        shortest_distance = float('inf')
        nearest_city = None
        for city in rest_cities:
            # For all rest cities, find the nearest one for the current city
            distance = calculate_route_distance([path[-1], city])
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_city = city
        # After finding the nearest city, add it to the path and delete it from the rest cities
        path.append(nearest_city)
        rest_cities.remove(nearest_city)
    path.append(end_city_coords)
    return path