import networkx as nx
from tkinter import *
import turtle
import heapq
import math

# Create a graph
graph = nx.Graph()
# Created edges between different places in Deerfield
# Found weight by plugging in locations into Google Earth (https://earth.google.com/web/@42.17199443,-87.86462034,198.58246414a,1195.04953889d,35y,357.42319088h,0t,0r/data=OgMKATA) and finding distance between them
graph.add_edge('Deerfield High School', 'Midtown Athletic Club', weight=0.65)
graph.add_edge('Deerfield High School', 'Waukegan Curve1', weight=0.36)
graph.add_edge('Waukegan Curve1', 'Waukegan Curve2', weight=0.27)
graph.add_edge('Waukegan Curve2', 'Waukegan Curve3', weight=0.57)
graph.add_edge('Waukegan Curve3', 'Deerfield Bakery', weight=0.14)
graph.add_edge('Deerfield Bakery', 'Deerfield/Waukegan Intersection', weight=0.05)
graph.add_edge('Deerfield/Waukegan Intersection', 'Walgreens', weight=0.1136)
graph.add_edge('Deerfield/Waukegan Intersection', 'Deerfield/Wilmot Intersection', weight=1.1)
graph.add_edge('Deerfield/Wilmot Intersection', 'Wilmot Elementary', weight=0.07)
graph.add_edge('Deerfield/Wilmot Intersection', 'Jaycee', weight=0.3)
graph.add_edge('Waukegan Curve2', 'Waukegan/Greenwood Intersection', weight=0.22)
graph.add_edge('Greenwood/Wilmot Intersection', 'Waukegan/Greenwood Intersection', weight=0.91)
graph.add_edge('Jaycee', 'Greenwood/Wilmot Intersection', weight=0.2)
graph.add_edge("Deerfield/Waukegan Intersection", "Briarwood Country Club", weight = 0.43)
graph.add_edge("Hazel/Waukegan Intersection", 'Waukegan/Greenwood Intersection', weight = 0.27)
graph.add_edge("Hazel/Waukegan Intersection", 'Waukegan Curve3', weight = 0.05)
graph.add_edge("Hazel/Waukegan Intersection", 'Hazel/Wilmot Intersection', weight = 1.03)
graph.add_edge("Jaycee", 'Hazel/Wilmot Intersection', weight = 0.06)
graph.add_edge("Walgreens", 'Deerfield/Wilmot Intersection', weight = 1)





# Dijkstra's algorithm implementation
# Used a combination of https://gist.github.com/kachayev/5990802 and https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-greedy-algo-7/ while fixing for my code
def dijkstra(g, start, end):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start, [start]))

    distances = {node: float('inf') for node in g}
    distances[start] = 0

    while priority_queue:
        current_distance, current_node, path = heapq.heappop(priority_queue)

        if current_node == end:
            return current_distance, path

        if current_distance > distances[current_node]:
            continue

        for neighbor in g.neighbors(current_node):
            weight = g[current_node][neighbor]['weight']
            new_distance = current_distance + weight
            new_path = path + [neighbor]

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(priority_queue, (new_distance, neighbor, new_path))

    return float('inf'), []

# Nodes to exclude from the dropdown menus, (intersections and curves)
exclude_nodes = {
    "Waukegan Curve1", "Waukegan Curve2", "Waukegan Curve3",
    "Deerfield/Waukegan Intersection", "Deerfield/Wilmot Intersection",
    "Waukegan/Greenwood Intersection", "Greenwood/Wilmot Intersection",
    "Hazel/Waukegan Intersection", "Hazel/Wilmot Intersection"
}

# Filtered list of nodes for dropdowns (kick out the excluded nodes)
filtered_nodes = [node for node in graph.nodes if node not in exclude_nodes]

# Initialize GUI
root = Tk()
root.title("Maps")
root.geometry('700x690')
root.configure(background='blue')
root.resizable(False, False)

l = Label(root, text = "Welcome to MapQuest Deerfield\n On the left choose your starting location \n On the right choose your destination \n Then finally, click on the find shortest route button to find the shortest route")
l.pack()

#set default options shown in the dropdown menus
start = StringVar()
start.set("Deerfield High School")
end = StringVar()
end.set("Midtown Athletic Club")

#Initialize Dropdown menus
drop = OptionMenu(root, start, *filtered_nodes)
drop.pack(side=LEFT)
drop1 = OptionMenu(root, end, *filtered_nodes)
drop1.pack(side=RIGHT)

# Coordinates for locations
# used https://www.mobilefish.com/services/record_mouse_coordinates/record_mouse_coordinates.php online image editor to find png coordinates of each location on the image
locations_dictionary = {
    "Deerfield High School": (362, 274),
    "Midtown Athletic Club": (311, 130),
    "Deerfield Bakery": (491, 573),
    "Walgreens": (462, 586),
    "Jaycee": (217, 516),
    "Wilmot Elementary": (216, 619),
    "Waukegan Curve1": (389, 360),
    "Waukegan Curve2": (425, 413),
    "Waukegan Curve3": (482, 533),
    "Deerfield/Waukegan Intersection": (492, 585),
    "Deerfield/Wilmot Intersection": (216,583),
    "Waukegan/Greenwood Intersection": (447,460),
    "Greenwood/Wilmot Intersection": (218,458),
    "Briarwood Country Club": (608,587),
    "Hazel/Waukegan Intersection": (476, 522),
    "Hazel/Wilmot Intersection": (217,521)

}

# Command that activates when button is pressed to convert image coordinates to turtle graphics coordinates
def convert_to_turtle_coords(x_image, y_image):
    x_turtle = x_image - 700 / 2
    y_turtle = 690 / 2 - y_image
    return x_turtle, y_turtle

# Button to trigger shortest path calculation
def find_shortest_path():
    shortest_distance, shortest_path = dijkstra(graph, start.get(), end.get())

    # Initialize Turtle graphics
    turtle_screen = turtle.Screen()
    turtle_screen.setup(width=700, height=690)
    turtle_screen.bgpic("output-onlinepngtools.png")

    bob = turtle.Turtle()
    bob.speed(1)
    bob.penup()

    # Draw the path using Turtle graphics
    for i in range(len(shortest_path) - 1):
        current_location = shortest_path[i]
        next_location = shortest_path[i + 1]

        current_x, current_y = convert_to_turtle_coords(locations_dictionary[current_location][0], locations_dictionary[current_location][1])
        next_x, next_y = convert_to_turtle_coords(locations_dictionary[next_location][0], locations_dictionary[next_location][1])

        # Calculate angle to next location so arrow is facing next location at all times
        angle = math.degrees(math.atan2(next_y - current_y, next_x - current_x))

        # Move to next location
        bob.goto(current_x, current_y)
        bob.setheading(angle)
        bob.pendown()
        bob.goto(next_x, next_y)

    # Display the shortest distance and path
    bob.penup()
    bob.speed(1000)
    bob.hideturtle()
    bob.goto(-150, 0)
    bob.color("white")
    bob.width(15)
    bob.pendown()
    bob.write(f"Total distance: {round(shortest_distance, 4)} miles", font=("Arial", 20, "normal"))

    # Close the turtle graphics window on button click
    turtle_screen.exitonclick()

# Button to activate finding the shortest route
button = Button(root, text="Find Shortest Route", command=find_shortest_path)
button.pack()

root.mainloop()

