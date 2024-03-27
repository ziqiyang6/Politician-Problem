import matplotlib.pyplot as plt
import numpy as np
from ant_colony import AntColony
from politician_function import cities_define
from politician_function import points_graph
from politician_function import calculate_route_distance
from politician_function import final_path_graph

# Input the data
# start_city_coords is the coordinate of Des Moines, Capital of Iowa
# end_city_coords is the coordinate of Washington D.C.
# other_cities_coords is the coordinate for rest capitals
cities, cities['Coordinates'], start_city_coords, end_city_coords, exclude_cities_coords, other_cities_coords = cities_define('E:/some_files/us-state-capitals.csv')


# Graph the all points
# Red means the start city, Des Moines
# Purple means the end city, D.C.

# graph = points_graph(start_city_coords, end_city_coords, other_cities_coords)
# plt.show()



distances = np.empty((50,50)) # Replace this with your distances matrix
distances.fill(0)

# distances = distances.
ant_cities = [start_city_coords] + [coords for coords in other_cities_coords]



i = 0
for city in ant_cities:

    for j in range(50):
        city_pair = [ant_cities[i], ant_cities[j]]
        distances[i, j] = calculate_route_distance(city_pair)

    i = i + 1


num_zeros = np.count_nonzero(distances == 0)


distances = (distances + distances.T) / 2  # Make it symmetric
np.fill_diagonal(distances, np.inf)  # Set diagonals to infinity to avoid self-travel

ant_colony = AntColony(distances, 20, 5, 100, 0.95, alpha=1, beta=2)
shortest_path = ant_colony.run()


path_cities = [shortest_path[0][0][0]] + [pair[1] for pair in shortest_path[0]]
path_coords = [ant_cities[index] for index in path_cities]

path_coords.append(end_city_coords)

# Show the final path.
path = [cities.loc[cities['Coordinates'] == coord, 'States'].iloc[0] for coord in path_coords]
print(path)

final_distance = calculate_route_distance(path_coords)
print(final_distance)

