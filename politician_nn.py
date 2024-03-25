import matplotlib.pyplot as plt
from politician_function import cities_define
from politician_function import points_graph
from politician_function import calculate_route_distance
from politician_function import nearest_neighbor
from politician_function import final_path_graph


# Input the data
# start_city_coords is the coordinate of Des Moines, Capital of Iowa
# end_city_coords is the coordinate of Washington D.C.
# other_cities_coords is the coordinate for rest capitals
cities, cities['Coordinates'], start_city_coords, end_city_coords, exclude_cities_coords, other_cities_coords = cities_define('E:/some_files/us-state-capitals.csv')


# Graph the all points
# Red means the start city, Des Moines
# Purple means the end city, D.C.
graph = points_graph(start_city_coords, end_city_coords, other_cities_coords)
plt.show()

# Use defined function to find the total path
path = nearest_neighbor(start_city_coords, end_city_coords,other_cities_coords)

# Change the coordinates to the name of corresponding states
route = [cities.loc[cities['Coordinates'] == coord, 'States'].iloc[0] for coord in path]
print(route)

# Calculate the distance for the path
final_distance = calculate_route_distance(path)
print(final_distance)

# Plot the path
total_path = final_path_graph(path)
plt.show()

