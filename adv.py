from room import Room
from player import Player
from world import World

import random
import time
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()
# Create new player to start world
player = Player(world.starting_room)


# Dictionary to reverse movement of each direction
convert_direction = {
    "n": "s",
    "s": "n",
    "w": "e",
    "e": "w"
}


# Function to retrieve the number of unexplored exits for a room
def get_number_of_unexplored_paths(room):
    unexplored_exits_count = 0

    for direction in room:
        if room[direction] == "?":
            unexplored_exits_count += 1

    return unexplored_exits_count


# Function to build initial visited dict entry. Ex ouput -> visited[room_id] = { "n": ?, "s": ?, "e": ?, "w": ? }
def build_initial_dict_entry_value(visited, room):
    possible_room_exits = room.get_exits()

    visited[room.id] = {}

    for move in possible_room_exits:
        visited[room.id][move] = "?"


# Main function to traverse maze -> output is an array containing the final directions to traverse maze
def get_traversal_directions(maze, player):
    final_directions = []
    reverse_directions = []
    visited = {}
    # Add starting room to visited dict
    build_initial_dict_entry_value(visited, player.current_room)

    while len(visited) < len(room_graph):
        # Traverse as far as possible while unexplored exits are available
        if get_number_of_unexplored_paths(visited[player.current_room.id]) > 0:
            for move in player.current_room.get_exits():
                if visited[player.current_room.id][move] == "?":
                    prev_room_id = player.current_room.id
                    backtrack_move = convert_direction[move]
                    player.travel(move)
                    final_directions.append(move)
                    reverse_directions.append(backtrack_move)
                    visited[prev_room_id][move] = player.current_room.id

                    if player.current_room.id not in visited:
                        build_initial_dict_entry_value(
                            visited, player.current_room)
                    visited[player.current_room.id][backtrack_move] = prev_room_id
                    break
        # Else backtrack to a room with unexplored exits
        else:
            backtrack_move = reverse_directions.pop()
            player.travel(backtrack_move)
            final_directions.append(backtrack_move)

    return final_directions


# traversal_path = ['n', 'n']
traversal_path = get_traversal_directions(world, player)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

start_time = time.time()

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

end_time = time.time()
print("Maze traverse in", end_time - start_time, "seconds.")

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
