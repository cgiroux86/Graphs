from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
import os


# class Queue():
#     def __init__(self):
#         self.queue = []

#     def enqueue(self, value):
#         self.queue.append(value)

#     def dequeue(self):
#         if self.size() > 0:
#             return self.queue.pop(0)
#         else:
#             return None

#     def size(self):
#         return len(self.queue)


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = f"{os.getcwd()}/projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

graph = {}
res = []


def add_edge(direction):
    if direction == 'e':
        return 'w'
    if direction == 'w':
        return 'e'
    if direction == 'n':
        return 's'
    if direction == 's':
        return 'n'


def traverse_maze(starting_room, visited=set(), path=[]):
    if len(visited) == 499:
        res.extend(path)
        return
    exits = starting_room.get_exits()
    curr_room = starting_room.id
    graph[curr_room] = {}
    visited.add(starting_room.id)
    for e in exits:
        graph[curr_room][e] = '?'
        player.travel(e)
        path.append(e)
        graph[curr_room][e] = player.current_room.id
        if player.current_room.id not in visited:
            traverse_maze(player.current_room, visited, path)
            player.travel(add_edge(e))
            path.append(add_edge(e))
        else:
            player.travel(add_edge(e))
            path.append(add_edge(e))


traverse_maze(player.current_room)
traversal_path = res


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
